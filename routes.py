from flask import flash, redirect, render_template, request, url_for
from forms import LoginForm, RegisterForm
from models import User, Customer, Part, Order, OrderItem
from flask_bcrypt import Bcrypt
from flask_login import login_manager, login_required, login_user, logout_user, current_user
from sqlalchemy.orm import joinedload

bcrypt = Bcrypt()

def register_routes(app, db):
    
    @app.login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    @app.route("/")
    def home():
        return redirect(url_for("login"))

    # -------- AUTH ---------------
    #@app.route("/login", methods=['GET', 'POST'])
    #def login():
        if request.method == "POST":
            input_username = request.form['username']
            input_password = request.form['password']

            user = User.query.filter_by(username=input_username).first()

            if user and bcrypt.check_password_hash(user.password, input_password):
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid username or password", "danger")

        return render_template('login.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid username or password", "danger")
        return render_template('login.html', form=form)

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('login'))

    #@app.route("/register", methods=['GET', 'POST'])
    #def register():
        form = RegisterForm()
        if request.method == "POST":
            new_user = User(
                username=request.form['username'], 
                password=bcrypt.generate_password_hash(request.form['password']).decode('utf-8'), 
                role="Software Developer", 
                description="Makes the software!"
                )
            try:
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for("login"))
            except:
                flash("Error when registering")
                return redirect(url_for("register"), form=form)
            
        return render_template('register.html', form=form)
    
    @app.route("/register", methods=['GET', 'POST'])
    def register():
        form = RegisterForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                # Check if user already exists
                existing_user = User.query.filter_by(username=form.username.data).first()
                if existing_user:
                    flash("Email already registered. Please log in or use a different email.", "warning")
                    return redirect(url_for("register"))

                # Create new user
                new_user = User(
                    username=form.username.data,
                    password=bcrypt.generate_password_hash(form.password.data).decode('utf-8'),
                    role="Software Developer",
                    description="Makes the software!"
                )
                try:
                    db.session.add(new_user)
                    db.session.commit()
                    flash("Registration successful! Please log in.", "success")
                    return redirect(url_for("login"))
                except Exception as e:
                    flash("An error occurred during registration. Please try again.", "danger")
                    return render_template('register.html', form=form)
        return render_template('register.html', form=form)


    # ---------- DASHBOARD ---------------------
    @app.route("/dashboard")
    @login_required 
    def dashboard():
        orders = Order.query.options(
                joinedload(Order.customer),
                joinedload(Order.order_items).joinedload(OrderItem.part)
            ).all()
        
        total_orders = Order.query.count()
        total_user = User.query.count()
        total_revenue = 0
        for order in orders:
            for item in order.order_items:
                total_revenue += item.quantity * item.part.price
        total_revenue = round(total_revenue,2)
        return render_template("dashboard.html", total_orders=total_orders, total_user=total_user, total_revenue=total_revenue)
    
    # ---------- ORDERS ---------------------
    @app.route("/orders")
    @login_required
    def orders():
        customer_id = request.args.get("customer_id", type=int)
        
        orders = Order.query.options(
                joinedload(Order.customer),
                joinedload(Order.order_items).joinedload(OrderItem.part)
            ).all()
        
        if customer_id:
            orders = Order.query.filter_by(customer_id=customer_id).all()
            selected_customer = Customer.query.filter_by(id=customer_id).first()
        else:
            selected_customer = None
                
        for order in orders:
            # Total price
            order.total_price = round(sum(item.quantity * item.part.price for item in order.order_items), 2)
            
            # Number of parts (sum of quantities, e.g. 3x filters + 2x pads = 5 parts total)
            order.total_parts = sum(item.quantity for item in order.order_items)

            # OR: Count distinct line items
            order.item_count = len(order.order_items)

        customers = Customer.query.all()
        parts = Part.query.all()
        return render_template("orders.html", orders=orders, customers=customers, selected_customer=selected_customer, parts=parts)
    
    
    @app.route("/orders/<int:id>")
    @login_required
    def order_details(id):
        order = Order.query.get(id)
        customer = order.customer
        order_items = OrderItem.query.filter(OrderItem.order_id == id).all()
        total = sum(item.part.price * item.quantity for item in order_items)
        return render_template("order_details.html", customer=customer, order=order, order_items=order_items, total=total)
    
    @app.route("/new_order")
    @login_required
    def new_order():
        return "NEW ORDER MADE!"

    # ---------- RETURNS ---------------------
    @app.route("/returns")
    @login_required
    def returns():
        return render_template("returns.html")
    
    # ---------- REPORTING ---------------------
    @app.route("/reporting")
    @login_required
    def reporting():
        return render_template("reporting.html")
    
    # ---------- USER PROFILE ---------------------
    @app.route("/profile")
    @login_required
    def profile():
        return render_template("profile.html")

    # ----------- ERROR HANDLING ------------------
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    
    # ------ TEMPLATE FILTERS -------
    @app.template_filter('currency')
    def currency_format(value):
        return "${:,.2f}".format(value)

    # ---------- OTHER --------------
    @app.route('/update_user/<int:id>')
    def update_user(id):
        user = User.query.filter(User.uid == id).first()
        firstName = request.args.get('firstName')
        lastName = request.args.get('lastName')
        user.first_name = firstName
        user.last_name = lastName
        try:
            db.session.commit()
        except:
            return "Error when updating user profile!"
        return redirect(url_for('dashboard'))
    
    @app.route('/add_customers')
    def add_customers():
        customers = [
            Customer(name="Alice Doe"),
            Customer(name="John Doe"),
            Customer(name="Random Guy"),
            Customer(name="Alex Jones"),
            Customer(name="John Cena")
            ]
        try:
            db.session.add_all(customers)
            db.session.commit()
        except:
            return "Error when saving new customers!"
        return "Successfully created new customers!"
    

    @app.route("/plumsail")
    def plumsail():
        return render_template("plumsail.html")