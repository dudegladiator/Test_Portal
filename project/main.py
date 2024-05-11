from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from . import db

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard1'))
    return render_template('index.html')

@dashboard.route('/dashboard')
@login_required
def dashboard1():
    return render_template('dashboard.html', current_user = current_user)




