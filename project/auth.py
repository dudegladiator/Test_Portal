from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from .models import User
from . import db
from flask_login import login_user as user_login, logout_user, login_required, current_user

auth_page = Blueprint('auth', __name__)
admin_list = ['harsh90731@gmail.com']

@auth_page.route('/login')
def login():
    return render_template('login.html')

@auth_page.route('/login_user', methods=['POST'])
def login_user():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) 
    
    user_login(user, remember=remember)
    return redirect(url_for('dashboard.dashboard1'))

@auth_page.route('/signup_user', methods=['POST'])
def signup_user():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    if(email in admin_list):
        role = 'admin'
    else:
        role = 'user'
        
    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists. Please login')
        return redirect(url_for('auth.login'))
    
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    new_user = User(email=email, name=name, pwd_hash=hashed_password, urole=role)
    db.session.add(new_user)
    db.session.commit()
    
    return redirect(url_for('auth.login'))

@auth_page.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('dashboard.index'))

@auth_page.route('/signup')
def signup():
    return render_template('signup.html')
