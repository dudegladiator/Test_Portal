from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'jbgcgyvgvgvyu5487354'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'


    
# login_manager = LoginManager()
# login_manager.login_view = 'auth.login'
# login_manager.init_app(app)

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

if __name__ == '__main__':
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'jbgcgyvgvgvyu5487354'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db1.sqlite'

    db.init_app(app)
    from models import User
    
    with app.app_context():
        db.create_all()
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    from auth import auth_page
    app.register_blueprint(auth_page)
    
    from main import dashboard
    app.register_blueprint(dashboard)
    
    app.run(debug=True, port=5054)