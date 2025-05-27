from flask import redirect, render_template, request, url_for

def register_routes(app, db):
    
    @app.route("/")
    def home():
        return "I am working!"
    
    @app.route("/orders")
    def orders():
        return ""
    
    @app.route("/order/<uid>")
    def order_details(uid):
        return ""