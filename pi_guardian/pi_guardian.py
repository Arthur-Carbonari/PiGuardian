from asyncio import sleep
import configparser
import os
import re
import threading
import unicodedata

import bcrypt

from pi_guardian.camera import Camera
from pi_guardian.email_handler import EmailHandler
from pi_guardian.face_recognition_handler import FaceRecognitionHandler

class PiGuardian:

    def __init__(self) -> None:
        self.face_recognition_handler = FaceRecognitionHandler()
        self.camera = Camera(self)
        self.email_handler = EmailHandler()
        

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

    def stranger_spotted(self):

        email = self.config.get('User', 'email')

        if email:
            image = self.camera.get_frame()
            self.email_handler.send_email(email, image)

        # record and save video


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
    
    def add_profile(self, profile_name, files):
                    # Remove leading/trailing whitespaces
            profile_name = profile_name.strip()

            # Replace spaces and special characters with underscores
            profile_name = re.sub(r'\s+', '_', profile_name)
            profile_name = re.sub(r'[^a-zA-Z0-9_]', '', profile_name)

            # Normalize Unicode characters
            profile_name = unicodedata.normalize('NFKD', profile_name).encode('ascii', 'ignore').decode('utf-8')

            # Convert to lowercase
            profile_name = profile_name.lower()

            os.makedirs('dataset/' + profile_name, exist_ok=True)

            for filename, filedata in files:
                file_path = os.path.join('dataset/' + profile_name, filename)
                with open(file_path, 'wb') as file:
                    file.write(filedata)

            # waits for the first file to be created to proceed
            while not os.path.exists('dataset/' + profile_name + '/' + files[0][0]):
                sleep(0.1)

            