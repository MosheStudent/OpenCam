import socket
import pickle
import cv2


def get_IP():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    print(local_ip)
    return local_ip


SERVER_PORT = 5555
SERVER_IP = get_IP()



def create_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP protocol
    server_socket.bind((SERVER_IP, SERVER_PORT))
    return server_socket

def receive_video(server_socket):
    while True:
        #recv data from client:
        frame_data, addr = server_socket.recvfrom(65536) #64k max
        frame = pickle.loads(frame_data) 

        frame = cv2.imdecode(frame, 1)
        cv2.imshow("Recived Video", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

server_socket = create_server()
receive_video(server_socket)


