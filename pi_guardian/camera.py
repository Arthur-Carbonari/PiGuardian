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

#Initialize 'currentname' to trigger only when a new person is identified.
currentname = "unknown"
#Determine faces from encodings.pickle file model created from train_model.py
encodingsP = "encodings.pickle"

# load the known faces and embeddings along with OpenCV's Haar
# cascade for face detection
print("[INFO] loading encodings + face detector...")
data = pickle.loads(open(encodingsP, "rb").read())


# use the grey cascate for cv2 recognise face
face_box = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")


time.sleep(2.0)

boxes = []
names = []

# this functon is used to drawn the square and name in the face, must be called after boxes and names initialization 
def draw_faces(request):
    with MappedArray(request, "main") as m:
        for (top, right, bottom, left), name in zip(boxes, names):

            # draw the predicted face name on the image - color is in BGR
            cv2.rectangle(m.array, (left, top), (right, bottom),(0, 255, 225), 2) 
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(m.array, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,0.75, (0, 255, 255), 2)

class Camera:

    def __init__(self):
        picam2 = Picamera2()

        cam_config = picam2.create_video_configuration(main={"size": (640, 480)}, 
                                                       lores={"size": (320, 240), "format": "YUV420"}, 
                                                       transform=Transform(hflip=1,vflip=1))        
        
        picam2.configure(cam_config)

        encoder = JpegEncoder()
        self.streaming_output = StreamingOutput()
        encoder.output = [FileOutput(self.streaming_output)]

        picam2.start_encoder(encoder)
        picam2.start()

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

    def detect_faces(self):
        (w0, h0) = self.picam2.stream_configuration("main")["size"]
        (w1, h1) = self.picam2.stream_configuration("lores")["size"]
        s1 = self.picam2.stream_configuration("lores")["stride"]

        while True:
            # grab the frame from the threaded video stream and resize it
            # to 500px (to speedup processing)
            frame = self.picam2.capture_array()
            frame = imutils.resize(frame, width=500)
            # Detect the fce boxes
            output = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            boxes = face_recognition.face_locations(output)
            # compute the facial embeddings for each face bounding box
            encodings = face_recognition.face_encodings(output, boxes)
            names = []

            # variables to draw_faces
            self.picam2.post_callback = draw_faces
            buffer = self.picam2.capture_buffer("lores")
            grey = buffer[:s1 * h1].reshape((h1, s1))
            face_locations = face_box.detectMultiScale(grey, 1.1, 3)


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
                # of votes (note: in the event of an unlikely tie Python
                # will select first entry in the dictionary)
                            name = max(counts, key=counts.get)

                #If someone in your dataset is identified, print their name on the screen
                            if currentname != name:
                                    currentname = name
                                    print(currentname)


            # update the list of names
                    names.append(name)
                    print(name)
                    print("current faces > ",names)



