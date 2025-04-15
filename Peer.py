import socket  # for connections
import cv2  # for video camera access
import pickle  # file handling
import threading  # for threading
import pyaudio  # for audio streaming

CONSTANT_VIDEO_PORT = 9999
CONSTANT_AUDIO_PORT = 10000

class Sender:
    def __init__(self, remote_ip, camera_index):
        self.remote_ip = remote_ip
        self.remote_video_port = CONSTANT_VIDEO_PORT
        self.remote_audio_port = CONSTANT_AUDIO_PORT
        self.camera_index = camera_index

        self.video_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP for video
        self.audio_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP for audio
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
                self.video_sock.sendto(data, (self.remote_ip, self.remote_video_port))
            except Exception as e:
                print("Send Video Error: ", e)
                break

        cap.release()
        self.video_sock.close()

    def send_audio(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

        while self.running:
            try:
                data = stream.read(1024, exception_on_overflow=False)
                self.audio_sock.sendto(data, (self.remote_ip, self.remote_audio_port))
            except Exception as e:
                print("Send Audio Error: ", e)
                break

        stream.stop_stream()
        stream.close()
        audio.terminate()
        self.audio_sock.close()

    def start(self):
        video_thread = threading.Thread(target=self.send_video)
        audio_thread = threading.Thread(target=self.send_audio)

        video_thread.daemon = True
        audio_thread.daemon = True

        video_thread.start()
        audio_thread.start()

        video_thread.join()
        audio_thread.join()


class Receiver:
    def __init__(self):
        self.local_video_port = CONSTANT_VIDEO_PORT
        self.local_audio_port = CONSTANT_AUDIO_PORT

        self.video_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP for video
        self.video_sock.bind(('', self.local_video_port))

        self.audio_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP for audio
        self.audio_sock.bind(('', self.local_audio_port))

        self.running = True

    def receive_video(self):
        while self.running:
            try:
                data, addr = self.video_sock.recvfrom(65535)
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
                print("Receive Video Error: ", e)
                break

        cv2.destroyAllWindows()
        self.video_sock.close()

    def receive_audio(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True, frames_per_buffer=1024)

        while self.running:
            try:
                data, addr = self.audio_sock.recvfrom(1024)
                stream.write(data)
            except Exception as e:
                print("Receive Audio Error: ", e)
                break

        stream.stop_stream()
        stream.close()
        audio.terminate()
        self.audio_sock.close()

    def start(self):
        video_thread = threading.Thread(target=self.receive_video)
        audio_thread = threading.Thread(target=self.receive_audio)

        video_thread.daemon = True
        audio_thread.daemon = True

        video_thread.start()
        audio_thread.start()

        video_thread.join()
        audio_thread.join()

