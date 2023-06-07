
import pickle
import time
import face_recognition
from pi_guardian.train_model import parse_dataset



class FaceRecognitionHandler:
    
    encodingsP = "encodings.pickle"

    def __init__(self) -> None:

        parse_dataset()
        #Determine faces from encodings.pickle file model created from train_model.py

        # load the known faces and embeddings along with OpenCV's Haar
        # cascade for face detection
        print("[INFO] loading encodings + face detector...")
        self.data = pickle.loads(open(self.encodingsP, "rb").read())
        time.sleep(2.0)

    def look_for_faces(self, rgb_image):
        boxes = face_recognition.face_locations(rgb_image)
        # compute the facial embeddings for each face bounding box
        encodings = face_recognition.face_encodings(rgb_image, boxes)
        names = []

        currentname = "Unknown" #if face is not recognized, then print Unknown


        # loop over the facial embeddings
        for encoding in encodings:
                # attempt to match each face in the input image to our known
                # encodings
                matches = face_recognition.compare_faces(self.data["encodings"], encoding)
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
                                name = self.data["names"][i]
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
                names.append(name.replace('_', ' '))
                print("current faces > ", names)

        return boxes, names

