import socket  # for connections
import cv2  # for video camera access
import pickle  # file handling
import threading  # for threading

CONSTANT_VIDEO_PORT = 9999
CAESAR_SHIFT = 3  # Shift value for Caesar cipher


def caesar_encrypt(data, shift):
    """Encrypt data using Caesar cipher."""
    return bytes((byte + shift) % 256 for byte in data)


def caesar_decrypt(data, shift):
    """Decrypt data using Caesar cipher."""
    return bytes((byte - shift) % 256 for byte in data)


class Sender:
    def __init__(self, remote_ip, camera_index):
        self.remote_ip = remote_ip
        self.remote_port = CONSTANT_VIDEO_PORT
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

            # Encrypt the data using Caesar cipher
            encrypted_data = caesar_encrypt(data, CAESAR_SHIFT)

            try:
                self.sock.sendto(encrypted_data, (self.remote_ip, self.remote_port))
            except Exception as e:
                print("Send Video Error: ", e)
                break

        cap.release()
        self.sock.close()

    def start(self):
        video_thread = threading.Thread(target=self.send_video)
        video_thread.daemon = True
        video_thread.start()
        video_thread.join()


class Receiver:
    def __init__(self):
        self.local_port = CONSTANT_VIDEO_PORT
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP protocol
        self.sock.bind(('', self.local_port))
        self.running = True

        # Video capture setup
        self.video_writer = None
        self.frame_width = 320
        self.frame_height = 240
        self.output_file = "captured_video.avi"
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')

    def receive_video(self):
        self.video_writer = cv2.VideoWriter(self.output_file, self.fourcc, 20.0, (self.frame_width, self.frame_height))

        while self.running:
            try:
                encrypted_data, addr = self.sock.recvfrom(65535)

                # Decrypt the data using Caesar cipher
                data = caesar_decrypt(encrypted_data, CAESAR_SHIFT)

                frame = pickle.loads(data)
                frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

                if frame is not None:
                    # Show the received video in the main window
                    cv2.imshow("Received Video", frame)

                    # Write the frame to the video file
                    self.video_writer.write(frame)

                # Check if the OpenCV window "X" button is clicked
                if cv2.getWindowProperty("Received Video", cv2.WND_PROP_VISIBLE) < 1:
                    self.running = False
                    break

                if cv2.waitKey(1) == ord('q'):
                    self.running = False
                    break

            except Exception as e:
                print("Receive Video Error: ", e)
                break

        self.video_writer.release()
        cv2.destroyAllWindows()
        self.sock.close()

    def start(self):
        receive_thread = threading.Thread(target=self.receive_video)
        receive_thread.daemon = True
        receive_thread.start()
        receive_thread.join()

