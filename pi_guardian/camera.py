from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
from libcamera import Transform
from pi_guardian.streaming_output import StreamingOutput


class Camera:

    def __init__(self):
        picam2 = Picamera2()

        cam_config = picam2.create_video_configuration(
            main={"size": (640, 480)}, transform=Transform(hflip=1, vflip=1))
        picam2.configure(cam_config)

        encoder = JpegEncoder()
        self.streaming_output = StreamingOutput()
        encoder.output = [FileOutput(self.streaming_output)]

        picam2.start_encoder(encoder)
        picam2.start()

        self.picam2 = picam2

    def generate_stream(self):
        while True:
            with self.streaming_output.condition:
                self.streaming_output.condition.wait()
                frame = self.streaming_output.frame
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            
    def take_photo(self):
        self.picam2.capture_file('test.jpg')


