from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_required

views_blueprint = Blueprint('views_blueprint', __name__)


@views_blueprint.route('/')
@login_required
def home():
    return render_template('home.html')
