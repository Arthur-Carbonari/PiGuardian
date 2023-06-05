from flask import Flask, Response, request, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
import flask_login

from forms import LoginForm


class FlaskServer:
    def __init__(self, camera):
        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'your_secret_key'
        app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'darkly'

        login_manager = LoginManager()
        login_manager.init_app(app)

        bootstrap = Bootstrap5(app)

        @app.route('/')
        @flask_login.login_required
        def index():
            return render_template('index.html')

        # Define routes
        @app.route('/start_camera', methods=['POST'])
        def start_camera():
            return self.handle_start_camera()

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

        @login_manager.unauthorized_handler
        def unauthorized():
            # Redirect the user to the auth page
            return redirect(url_for('auth'))

        @app.route('/logout', methods=['GET', 'POST'])
        @login_required
        def logout():
            logout_user()
            return redirect('auth')

        @app.route('/stop_camera', methods=['POST'])
        def stop_camera():
            return self.handle_stop_camera()

        @app.route('/save_file', methods=['POST'])
        def save_file():
            return self.handle_save_file()

        @app.route('/video_feed')
        def video_feed():
            return Response(camera.generate_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

        self.app = app

    def handle_start_camera(self):
        # Logic for starting the camera
        return "Camera started"

    def handle_stop_camera(self):
        # Logic for stopping the camera
        return "Camera stopped"

    def handle_save_file(self):
        file_data = request.files['file']
        # Logic for saving the file
        return "File saved"

    def start(self):
        self.app.run(host='0.0.0.0', port=5000, debug=True)


class User(UserMixin):
    pass


if __name__ == "__main__":
    fs = FlaskServer({})
    fs.start()
