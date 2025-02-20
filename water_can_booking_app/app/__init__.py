from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from app import db
from flask_jwt_extended import JWTManager
# from flask_login import LoginManager
db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    app.secret_key = '441c57d296fa7518e19c580629b2f709'  
    db.init_app(app)
    jwt.init_app(app)
   
    # Register blueprints
    from app.routes import register
    app.register_blueprint(register.bp)
    # app.register_blueprint(products.bp)
    # app.register_blueprint(orders.bp)

    return app
