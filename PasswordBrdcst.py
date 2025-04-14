import socket
import random

def GenPassword():
    return random.randint(1, 1000000)

def send_password(password, port=12345):
    message = (str(password)).encode('utf-8')
    broadcast_ip = '255.255.255.255'
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sendto(message, (broadcast_ip, port))

def recv_password(port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(('', port))
        data, addr = s.recvfrom(1024)
        return data.decode('utf-8')

