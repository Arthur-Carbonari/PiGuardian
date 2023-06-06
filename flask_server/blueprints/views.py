from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_required

views_blueprint = Blueprint('views_blueprint', __name__)

@views_blueprint.before_request
@login_required
def require_login():
    pass

@views_blueprint.route('/')
def home():
    return render_template('home.html')

@views_blueprint.route('/profiles')
def profiles():
    return render_template('profiles.html')
