from flask import flash, redirect, render_template, request, url_for
from models import User, Customer, Part, Order, OrderItem
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def register_routes(app, db):
    

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
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid username or password", "danger")

        return render_template('login.html')
    
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
    def dashboard():
        return render_template("dashboard.html")
    
    @app.route("/orders")
    def orders():
        return render_template("orders.html")
    
    @app.route("/returns")
    def returns():
        return render_template("returns.html")
    
    @app.route("/reporting")
    def reporting():
        return render_template("reporting.html")
    
    # ----------- ERROR HANDLING ------------------
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404