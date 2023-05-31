from flask import Flask, Response, render_template, request
from flask_bootstrap import Bootstrap

class FlaskServer:
    def __init__(self, camera):
        app = Flask(__name__)
        bootstrap = Bootstrap(app)

        @app.route('/')
        def index():
            return render_template('index.html')

        # Define routes
        @app.route('/start_camera', methods=['POST'])
        def start_camera():
            return self.handle_start_camera()

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
        self.app.run(host='0.0.0.0', port=5000)
