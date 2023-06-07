import configparser
import os

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

        self.get_profiles()

    def generate_stream(self):
        while True:
            frame = self.camera.get_frame()

            if frame:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    def take_picture(self):
        self.camera.save_frame('dataset/marina_cury/pic1')

    def get_flask_config(self):
        return dict(self.config.items('Flask'))
    
    def update_flask_config(self, option, value):
        self.config.set('Flask', option, value)
        # Save the changes back to the .ini file
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

    def authenticate_user(self, entered_username, entered_password):
        username = self.config.get('User', 'username')
        password = self.config.get('User', 'password')

        if not password and entered_password == 'password' and entered_username == username:
            return True
        
        return bcrypt.checkpw(entered_password.encode('utf-8'), password.encode('utf-8')) and entered_username == username

    def get_profiles(self):
        dataset_path = 'dataset'  # Path to the "dataset" folder

        profiles = []
        
        for folder_name in os.listdir(dataset_path):
            folder_path = os.path.join(dataset_path, folder_name)
            if os.path.isdir(folder_path):
                files = os.listdir(folder_path)
                if files:  # Check if the folder contains any files
                    path_to_file = folder_name + '/' + files[0]
                    profile_name = folder_name.replace('_', ' ')

                    profiles.append([profile_name, path_to_file])

        return profiles
    

            