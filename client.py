import socket
import pickle
import cv2

SERVER_IP = 'your_server_ip_address'  # Replace with the actual server IP address
SERVER_PORT = 5555

def create_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP protocol
    return client_socket

def send_video(client_socket):
    cap = cv2.VideoCapture(0)  # Capture video from the default camera

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        _, buffer = cv2.imencode('.jpg', frame)
        frame_data = pickle.dumps(buffer)

        client_socket.sendto(frame_data, (SERVER_IP, SERVER_PORT))

        cv2.imshow("Sending Video", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

client_socket = create_client()
send_video(client_socket)
