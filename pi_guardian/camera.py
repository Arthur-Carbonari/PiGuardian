import threading
from picamera2 import Picamera2, MappedArray
from picamera2.encoders import JpegEncoder, H264Encoder
from picamera2.outputs import FileOutput
from libcamera import Transform

from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time
import cv2
import numpy as np

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

    def __init__(self):
        picam2 = Picamera2()

        cam_config = picam2.create_video_configuration(main={"size": (640, 480)}, 
                                                       lores={"size": (320, 240), "format": "YUV420"}, 
                                                       transform=Transform(hflip=1,vflip=1))        
        
        picam2.configure(cam_config)

        picam2.post_callback = self.post_callback

        (self.w0, self.h0) = picam2.stream_configuration("main")["size"]
        (self.w1, self.h1) = picam2.stream_configuration("lores")["size"]
        self.s1 = picam2.stream_configuration("lores")["stride"]

        self.boxes = []
        self.names = []

        self.streaming_output = StreamingOutput()
        picam2.start_recording(JpegEncoder(), FileOutput(self.streaming_output))

        self.picam2 = picam2

        threading.Thread(target=self.detect_faces).start()


    def generate_stream(self):
        while True:
            with self.streaming_output.condition:
                self.streaming_output.condition.wait()
                frame = self.streaming_output.frame
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            
    def get_frame(self):
        return self.streaming_output.frame
            
    def take_photo(self):
        self.picam2.capture_file('test.jpg')

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


    def get_face_recognition_frame(self):
        # grab the buffer from the current stream
        buffer = self.picam2.capture_buffer('lores')
        frame = buffer[:self.s1 * self.h1].reshape((self.h1, self.s1))
        
        # frame = imutils.resize(frame, width=500)
        # Detect the fce boxes
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
         

    def detect_faces(self):

        currentname = "unknown"

        while True:

            # Resets names
            self.names = []

            output = self.get_face_recognition_frame()
            self.boxes = face_recognition.face_locations(output)
            # compute the facial embeddings for each face bounding box
            encodings = face_recognition.face_encodings(output, self.boxes)

            # loop over the facial embeddings
            for encoding in encodings:
                    
                    # attempt to match each face in the input image to our known
                    # encodings
                    matches = face_recognition.compare_faces(data["encodings"], encoding)
                    name = "Unknown" #if face is not recognized, then print Unknown

                    # check to see if we have found a match
                    if True in matches:
                            # find the indexes of all matched faces then initialize a
                            # dictionary to count the total number of times each face
                            # was matched
                            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                            counts = {}

                            # loop over the matched indexes and maintain a cout for
                            # each recognized face face
                            for i in matchedIdxs:
                                    name = data["names"][i]
                                    counts[name] = counts.get(name, 0) + 1

                            # determine the recognized face with the largest number
                            # of votes
                            name = max(counts, key=counts.get)

                            if currentname != name:
                                    currentname = name
                                    print(name)
                        
                    # update the list of names
                    self.names.append(name.replace('_', ' '))

                    print("current faces > ",self.names)



