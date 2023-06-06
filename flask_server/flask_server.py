from flask import Flask, Response, request, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
import flask_login

from flask_server.forms import LoginForm


class FlaskServer:

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'darkly'

    login_manager = LoginManager()

    def __init__(self, camera):

        self.login_manager.init_app(self.app)
        self.login_manager.login_view = 'auth'

        Bootstrap5(self.app)

        self.camera = camera

    @app.route('/')
    @flask_login.login_required
    def index():
        return render_template('index.html')

    # Define routes
    @app.route('/auth', methods=['GET', 'POST'])
    def auth():

        if current_user.is_authenticated:
            return redirect(url_for('index'))

        login_form: LoginForm = LoginForm()

        if login_form.validate_on_submit():
            username, password = login_form.username.data, login_form.password.data
            print(username, password)
            user = User()
            user.id = username
            login_user(user)
            return redirect(url_for('index'))

        return render_template('auth.html', login_form=login_form)

    @login_manager.user_loader
    def user_loader(email):
        user = User()
        user.id = email
        return user

    @login_manager.request_loader
    def request_loader(request):

        email = request.form.get('email')

        if not email:
            return

        user = User()
        user.id = email
        return user

    @app.route('/logout', methods=['GET', 'POST'])
    @login_required
    def logout():
        logout_user()
        return redirect('auth')

    @app.route('/video_feed')
    def video_feed(self):
        return Response(self.camera.generate_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

    def start(self, debug=False):
        self.app.run(host='0.0.0.0', port=5000, debug=debug)


class User(UserMixin):
    pass
