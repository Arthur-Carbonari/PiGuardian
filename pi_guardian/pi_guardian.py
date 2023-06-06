import configparser

import bcrypt
from pi_guardian.mock_camera import MockCamera


class PiGuardian:

    def __init__(self, debug=False) -> None:
        self.camera = MockCamera()

        self.camera.start_capture()

        # Create a ConfigParser object
        self.config = configparser.ConfigParser()

        # Load the .ini file
        self.config.read('config.ini')

    def generate_stream(self):
        while True:
            frame = self.camera.get_frame()

            if frame:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    def take_picture(self):
        self.camera.save_frame('dataset/arthur_martins/pic1')

    def get_flask_config(self):
        return dict(self.config.items('Flask'))

    def authenticate_user(self, entered_username, entered_password):
        username = self.config.get('User', 'username')
        password = self.config.get('User', 'password')

        if not password and entered_password == 'password' and entered_username == username:
            return True
        
        return bcrypt.checkpw(entered_password.encode('utf-8'), password.encode('utf-8')) and entered_username == username
