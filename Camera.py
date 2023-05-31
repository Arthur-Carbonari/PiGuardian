import io
from threading import Condition

from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput


class Camera:

    def __init__(self):
        picam2 = Picamera2()
        picam2.configure(picam2.create_video_configuration( main={"size": (640, 480)} ))
        self.output = StreamingOutput()
        picam2.start_recording(JpegEncoder(), FileOutput(self.output))


class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()
