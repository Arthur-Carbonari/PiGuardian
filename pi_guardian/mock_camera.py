import cv2
import threading
from threading import Condition

from pi_guardian.streaming_output import StreamingOutput

class MockCamera:
    def __init__(self):
        self.output = StreamingOutput()
        self.stop_event = threading.Event()
        self.capture_thread = None

    def start_capture(self):
        self.capture_thread = threading.Thread(target=self._capture_frames)
        self.capture_thread.start()

    def stop_capture(self):
        self.stop_event.set()
        if self.capture_thread:
            self.capture_thread.join()

    def _capture_frames(self):
        cap = cv2.VideoCapture(0)
        while not self.stop_event.is_set():
            ret, frame = cap.read()
            if not ret:
                print("Failed to read frame from the webcam")
                break

            # Convert the frame to bytes
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            
            self.output.write(frame_bytes)

        cap.release()

    def get_frame(self):
        return self.output.frame

    def save_frame(self, filename):
        frame_bytes = self.output.frame
        if frame_bytes:
            with open(filename + ".jpg", 'wb') as f:
                f.write(frame_bytes)
            print(f"Frame saved as {filename}")
        else:
            print("No frame available to save.")