from flask import Blueprint, redirect, render_template, url_for
import flask_login

views_blueprint = Blueprint('views_blueprint', __name__)


@views_blueprint.route('/')
@flask_login.login_required
def index():
    return render_template('index.html')
