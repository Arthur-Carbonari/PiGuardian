import threading
from picamera2 import Picamera2, MappedArray
from picamera2.encoders import JpegEncoder, H264Encoder
from picamera2.outputs import FileOutput
from libcamera import Transform

from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import pickle
import time
import cv2
from pi_guardian.face_recognition_handler import FaceRecognitionHandler

from pi_guardian.streaming_output import StreamingOutput

#Determine faces from encodings.pickle file model created from train_model.py
encodingsP = "encodings.pickle"

# load the known faces and embeddings along with OpenCV's Haar
# cascade for face detection
print("[INFO] loading encodings + face detector...")
data = pickle.loads(open(encodingsP, "rb").read())


time.sleep(2.0)


class Camera:

    colour = (0, 255, 0)
    origin = (0, 30)
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.5
    thickness = 2

    def __init__(self, pi_guardian):
        picam2 = Picamera2()
        self.pi_guardian = pi_guardian

        self.recording_lock = threading.Lock()

        cam_config = picam2.create_video_configuration(main={"size": (640, 480)}, 
                                                       lores={"size": (320, 240), "format": "YUV420"}, 
                                                       transform=Transform(hflip=1,vflip=1))        
        
        picam2.configure(cam_config)

        picam2.post_callback = self.post_callback

        (self.w0, self.h0) = picam2.stream_configuration("main")["size"]
        (self.w1, self.h1) = picam2.stream_configuration("lores")["size"]
        self.s1 = picam2.stream_configuration("lores")["stride"]

        self.face_locations = []

        self.boxes = []
        self.names = []

        self.streaming_output = StreamingOutput()

        encoder = JpegEncoder()

        temp_output = FileOutput(self.streaming_output)
        self.save_file_output = FileOutput()

        encoder.output = [temp_output, self.save_file_output]

        picam2.start_encoder(encoder)
        picam2.start()

        temp_output.start()

        self.picam2 = picam2

        threading.Thread(target=self.detect_faces).start()
            
    def get_frame(self):
        return self.streaming_output.frame
            
    def take_photo(self, path):
        self.picam2.capture_file(path)
        
    # this functon is used to drawn the square and name in the face, must be called after boxes and names initialization 
    def draw_faces(self, request):
        with MappedArray(request, "main") as m:
            for ((top, right, bottom, left), name) in zip(self.boxes, self.names):
                # draw the predicted face name on the image - color is in BGR
                cv2.rectangle(m.array, (left* 2, top * 2), (right* 2, bottom* 2),
                    (0, 255, 225), 2)
                y = top - 15 if top - 15 > 15 else top + 15
                cv2.putText(m.array, name, (left * 2, y * 2), cv2.FONT_HERSHEY_SIMPLEX,
                    .5, (0, 255, 255), 2)

    def apply_timestamp(self, request):
        timestamp = time.strftime("%Y-%m-%d %X")
        with MappedArray(request, "main") as m:
            cv2.putText(m.array, timestamp, self.origin, self.font, 
                        self.scale, self.colour, self.thickness)
            
    def post_callback(self, request):
        self.draw_faces(request)
        self.apply_timestamp(request)

    def get_rgb_image(self):
            buffer = self.picam2.capture_buffer('lores')
            frame = buffer[:self.s1 * self.h1].reshape((self.h1, self.s1))
            
            # frame = imutils.resize(frame, width=500)
            # Detect the fce boxes
            return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
         

    def detect_faces(self):

        while True:

            rgb_image = self.get_rgb_image()
            self.boxes, self.names = self.pi_guardian.face_recognition_handler.look_for_faces(rgb_image)

            if 'Unknown' in self.names:
                threading.Thread(target=self.pi_guardian.stranger_spotted).start()
                    



