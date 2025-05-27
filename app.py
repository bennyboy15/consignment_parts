from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

db = SQLAlchemy()
load_dotenv()

# FACTORY DESIGN PATTERN
def create_app():
    app = Flask(__name__, template_folder='application/templates', static_folder='application/static', static_url_path='/')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./consignment.db'
    app.secret_key = os.getenv("SECRET_KEY")
    db.init_app(app)

    from routes import register_routes
    register_routes(app, db)

    migrate = Migrate(app, db)
    
    return app