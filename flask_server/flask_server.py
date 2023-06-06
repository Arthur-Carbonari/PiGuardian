from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager

from flask_server.models import User
from flask_server.auth_blueprint import auth_blueprint
from flask_server.views_blueprint import views_blueprint
from flask_server.api_blueprint import api_blueprint
from pi_guardian.pi_guardian import PiGuardian


class FlaskServer:

    app = Flask(__name__)

    login_manager = LoginManager()

    def __init__(self, pi_guardian: PiGuardian):

        self.pi_guardian = pi_guardian
        self.app.pi_guardian = pi_guardian

        # Setup login manager
        self.login_manager.init_app(self.app)
        self.login_manager.login_view = 'auth_blueprint.auth'

        # Add Bootstrap5 to the app
        Bootstrap5(self.app)

        # Configure the app
        self.config  = self.pi_guardian.get_flask_config()
        self.app.config['SECRET_KEY'] = self.config['secret_key']
        self.app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'darkly' if self.config['dark_mode'] else 'lumen'

        # Register routes
        self.app.register_blueprint(views_blueprint, url_prefix="/")
        self.app.register_blueprint(auth_blueprint, url_prefix="/auth")
        self.app.register_blueprint(api_blueprint, url_prefix='/api')
        

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

    def start(self, debug=False):
        self.app.run(host='0.0.0.0', port=5000, debug=debug)
