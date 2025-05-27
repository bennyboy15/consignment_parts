from flask import redirect, render_template, request, url_for

def register_routes(app, db):
    
    @app.route("/")
    def home():
        return redirect(url_for("login"))

    @app.route("/login")
    def login():
        return render_template('login.html')
    
    @app.route("/register")
    def register():
        return render_template('register.html')
    
