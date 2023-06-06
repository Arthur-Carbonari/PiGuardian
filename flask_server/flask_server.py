from flask import Flask, Response
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager

from flask_server.models import User
from flask_server.auth_blueprint import auth_blueprint
from flask_server.views_blueprint import views_blueprint


class FlaskServer:

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'darkly'

    login_manager = LoginManager()

    def __init__(self, camera):

        self.camera = camera

        self.login_manager.init_app(self.app)
        self.login_manager.login_view = 'auth_blueprint.auth'

        Bootstrap5(self.app)

        self.app.register_blueprint(views_blueprint, url_prefix="/")
        self.app.register_blueprint(auth_blueprint, url_prefix="/auth")

    @login_manager.user_loader
    def user_loader(username):
        user = User()
        user.id = username
        return user

    @login_manager.request_loader
    def request_loader(request):

        username = request.form.get('username')

        if not username:
            return

        user = User()
        user.id = username
        return user

    @app.route('/video_feed')
    def video_feed():
        return "something"
        return Response(self.camera.generate_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

    def start(self, debug=False):
        self.app.run(host='0.0.0.0', port=5000, debug=debug)
