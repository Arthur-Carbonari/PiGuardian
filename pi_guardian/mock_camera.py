import cv2

class MockCamera:

    def generate_stream(self):
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()

            if not ret:
                print("Failed to read frame from the webcam")
                break

            # Resize the frame to a smaller size if needed
            # frame = cv2.resize(frame, (640, 480))

            # Convert the frame to bytes
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

        cap.release()
