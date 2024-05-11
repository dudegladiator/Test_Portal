from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'jbgcgyvgvgvyu5487354'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)
    from .models import User
    
    with app.app_context():
        db.create_all()
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    from .auth import auth_page
    app.register_blueprint(auth_page)
    
    from .main import dashboard
    app.register_blueprint(dashboard)
    
    from .test import test
    app.register_blueprint(test)
    
    from .admin import admin
    app.register_blueprint(admin, url_prefix='/admin')
    
    return app

