import socket  # for connections
import cv2  # for video camera access
import pickle  # file handling
import threading  # for threading

CONSTANT_PORT = 9999

class Sender:
    def __init__(self, remote_ip, camera_index):
        self.remote_ip = remote_ip
        self.remote_port = CONSTANT_PORT
        self.camera_index = camera_index

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP protocol
        self.running = True

    def send_video(self):
        cap = cv2.VideoCapture(self.camera_index)

        while self.running and cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Resize frame for sending
            frame = cv2.resize(frame, (320, 240))
            _, buffer = cv2.imencode('.jpg', frame)
            data = pickle.dumps(buffer)

            try:
                self.sock.sendto(data, (self.remote_ip, self.remote_port))
            except Exception as e:
                print("Send Error: ", e)
                break

        cap.release()
        self.sock.close()

    def start(self):
        send_thread = threading.Thread(target=self.send_video)
        send_thread.daemon = True
        send_thread.start()
        send_thread.join()


class Receiver:
    def __init__(self):
        self.local_port = CONSTANT_PORT
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP protocol
        self.sock.bind(('', self.local_port))
        self.running = True

    def receive_video(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(65535)
                frame = pickle.loads(data)
                frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

                if frame is not None:
                    # Show the received video in the main window
                    cv2.imshow("Received Video", frame)

                # Check if the OpenCV window "X" button is clicked
                if cv2.getWindowProperty("Received Video", cv2.WND_PROP_VISIBLE) < 1:
                    self.running = False
                    break

                if cv2.waitKey(1) == ord('q'):
                    self.running = False
                    break

            except Exception as e:
                print("Receive Error: ", e)
                break

        cv2.destroyAllWindows()
        self.sock.close()

    def start(self):
        receive_thread = threading.Thread(target=self.receive_video)
        receive_thread.daemon = True
        receive_thread.start()
        receive_thread.join()

