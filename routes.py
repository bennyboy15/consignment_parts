from flask import flash, redirect, render_template, request, url_for
from models import User, Customer, Part, Order, OrderItem
from flask_bcrypt import Bcrypt
from flask_login import login_manager, login_required, login_user, logout_user

bcrypt = Bcrypt()

def register_routes(app, db):
    
    @app.login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    @app.route("/")
    def home():
        return redirect(url_for("login"))

    # -------- AUTH ---------------
    @app.route("/login", methods=['GET', 'POST'])
    def login():
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
    
    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @app.route("/register", methods=['GET', 'POST'])
    def register():
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
                return redirect(url_for("register"))
            
        return render_template('register.html')
    
    @app.route("/dashboard")
    @login_required 
    def dashboard():
        return render_template("dashboard.html")
    
    @app.route("/orders")
    @login_required
    def orders():
        orders = Order.query.all()
        return render_template("orders.html", orders=orders)
    
    @app.route("/orders/<int:id>")
    @login_required
    def order_details(id):
        order = Order.query.get(id)
        customer = order.customer
        order_items = OrderItem.query.filter(OrderItem.order_id == id).all()
        total = sum(item.part.price * item.quantity for item in order_items)
        return render_template("order_details.html", customer=customer, order=order, order_items=order_items, total=total)

    
    @app.route("/returns")
    @login_required
    def returns():
        return render_template("returns.html")
    
    @app.route("/reporting")
    @login_required
    def reporting():
        return render_template("reporting.html")
    
    # ----------- ERROR HANDLING ------------------
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    