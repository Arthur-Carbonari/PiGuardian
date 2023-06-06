import configparser
from pi_guardian.mock_camera import MockCamera


class PiGuardian:

    def __init__(self, debug=False) -> None:
        self.camera = MockCamera()

        self.camera.start_capture()
        
        # Create a ConfigParser object
        self.config = configparser.ConfigParser()

        # Load the .ini file
        self.config.read('pi_guardian/config.ini')

    def generate_stream(self):
        while True:
            frame = self.camera.get_frame()

            if frame:
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    def take_picture(self):
        self.camera.save_frame('test')

    def get_flask_config(self):
        return dict(self.config.items('Flask'))