import socket  # for connections
import cv2  # for video camera access
import pickle  # file handling
import threading  # for bi-directional video chat

CONSTANT_PORT = 9999

class Peer:
    def __init__(self, remote_ip, camera_index):
        self.local_port = CONSTANT_PORT
        self.remote_ip = remote_ip
        self.remote_port = CONSTANT_PORT
        self.camera_index = camera_index

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
                    cv2.imshow("Remote Video", frame)

                # Check if the OpenCV window "X" button is clicked
                if cv2.getWindowProperty("Remote Video", cv2.WND_PROP_VISIBLE) < 1:
                    self.running = False
                    break

                if cv2.waitKey(1) == ord('q'):
                    self.running = False
                    break

            except Exception as e:
                print("Receive Error: ", e)
                break

        cv2.destroyAllWindows()

    def start(self):
        t = threading.Thread(target=self.receive_video)
        t.daemon = True  # Allow the thread to exit when the main program exits
        t.start()

