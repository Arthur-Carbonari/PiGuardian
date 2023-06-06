from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user

from flask_server.forms import LoginForm
from flask_server.models import User


auth_blueprint = Blueprint('auth_blueprint', __name__)


@auth_blueprint.route('/', methods=['GET', 'POST'])
def auth():

    if current_user.is_authenticated:
        return redirect(url_for('views_blueprint.index'))

    login_form: LoginForm = LoginForm()

    if login_form.validate_on_submit():
        username, password = login_form.username.data, login_form.password.data
        print(username, password)
        user = User()
        user.id = username
        login_user(user)
        return redirect(url_for('views_blueprint.index'))

    return render_template('auth.html', login_form=login_form)

@auth_blueprint.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_blueprint.auth'))