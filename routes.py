from flask import flash, redirect, render_template, request, url_for
from models import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def register_routes(app, db):
    
    @app.route("/")
    def home():
        return redirect(url_for("login"))

    @app.route("/login", methods=['GET', 'POST'])
    def login():
        if request.method == "POST":
            input_username = request.form['username']
            input_password = request.form['password']

            user = User.query.filter_by(username=input_username).first()

            if user and bcrypt.check_password_hash(user.password, input_password):
                return "Successful login!"
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
    
