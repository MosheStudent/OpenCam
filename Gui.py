import tkinter as tk
import random
from Peer import Peer  # Import the Peer class
import PasswordBrdcst
import socket
import threading
import time

def get_local_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # Connect to an external IP (doesn't actually send data)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]

class HostWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("300x300+100+100")
        self.root.title("Host Meeting")
        
        self.PASSWORD = PasswordBrdcst.GenPassword()  # Generate a random password
        self.running = True  # Flag to control threads

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)  # Handle "X" button
        self.displayWin()

    def displayWin(self):
        label = tk.Label(self.root, text=f'password: {self.PASSWORD} \n IP: {get_local_ip()}')
        label.pack()

        label2 = tk.Label(self.root, text="Waiting for connection...")
        label2.pack()

        # Start broadcasting the password and checking for confirmation in separate threads
        threading.Thread(target=self.broadcast_password, daemon=True).start()
        threading.Thread(target=self.wait_for_confirmation_and_start, daemon=True).start()

        self.root.mainloop()

    def broadcast_password(self):
        while self.running:
            print(f"Broadcasting password: {self.PASSWORD}")  # Debug log
            PasswordBrdcst.send_password(self.PASSWORD)
            time.sleep(10)  # Broadcast every 10 seconds

    def wait_for_confirmation_and_start(self):
        print("Waiting for confirmation...")  # Debug log
        if self.wait_for_confirmation():
            print("Confirmation received!")  # Debug log
            self.running = False  # Stop broadcasting
            self.root.destroy()
            # Start the Peer instance for hosting
            peer = Peer(remote_ip="127.0.0.1", camera_index=0)  # Use localhost for hosting
            peer.start()
        else:
            print("Connection confirmation failed!")  # Debug log
            self.show_error("Connection confirmation failed!")

    def wait_for_confirmation(self, port=12346):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Allow the socket to reuse the address
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('', port))
            s.settimeout(30)  # Wait for 30 seconds for confirmation
            try:
                data, addr = s.recvfrom(1024)
                print(f"Received confirmation from {addr}: {data.decode('utf-8')}")  # Debug log
                return data.decode('utf-8') == "CONFIRMED"
            except socket.timeout:
                print("Timeout while waiting for confirmation.")  # Debug log
                return False

    def show_error(self, message):
        error_window = tk.Toplevel(self.root)
        error_window.geometry("200x100")
        error_window.title("Error")
        label = tk.Label(error_window, text=message)
        label.pack()
        close_button = tk.Button(error_window, text="Close", command=error_window.destroy)
        close_button.pack()

    def on_close(self):
        self.running = False  # Stop broadcasting
        self.root.destroy()

class JoinWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("300x300+100+100")
        self.root.title("Join Meeting")

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)  # Handle "X" button
        self.displayWin()

    def displayWin(self):
        label = tk.Label(self.root, text="Enter password:")
        label.pack()

        self.entryPass = tk.Entry(self.root)
        self.entryPass.pack()

        label2 = tk.Label(self.root, text="Enter IP:")
        label2.pack()

        self.entryIP = tk.Entry(self.root)
        self.entryIP.pack()

        connectButton = tk.Button(self.root, text="Connect", command=self.connect)
        connectButton.pack()
        
        self.root.mainloop()
    
    def connect(self):
        password = self.entryPass.get()
        ip = self.entryIP.get()

        # Validate and start in a separate thread
        threading.Thread(target=self.validate_and_start, args=(password, ip)).start()

    def validate_and_start(self, password, ip):
        realPass = PasswordBrdcst.recv_password()
        print(f"Received password: {realPass}")  # Debug log
        
        if password == realPass:  
            print("Password is correct. Sending confirmation...")  # Debug log
            self.send_confirmation(ip)
            self.root.destroy()
            # Start the Peer instance for joining
            peer = Peer(remote_ip=ip, camera_index=0)  # Use the entered IP
            peer.start()
        else:
            print("Password is incorrect!")  # Debug log
            self.show_error("Password is incorrect!")

    def send_confirmation(self, ip, port=12346):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            print(f"Sending confirmation to {ip}:{port}")  # Debug log
            s.sendto(b"CONFIRMED", (ip, port))

    def show_error(self, message):
        error_window = tk.Toplevel(self.root)
        error_window.geometry("200x100")
        error_window.title("Error")
        label = tk.Label(error_window, text=message)
        label.pack()
        close_button = tk.Button(error_window, text="Close", command=error_window.destroy)
        close_button.pack()

    def on_close(self):
        self.root.destroy()

class StartWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("300x100+100+100")
        self.root.title("Start WebCall")

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)  # Handle "X" button
        self.displayWin()

    def displayWin(self):
        hostButton = tk.Button(self.root, text="Host", command=self.hostWin)
        hostButton.pack()

        joinButton = tk.Button(self.root, text="Join", command=self.joinWin)
        joinButton.pack()

        self.root.mainloop()

    def hostWin(self):
        self.root.destroy()
        HostWindow()

    def joinWin(self):
        self.root.destroy()
        JoinWindow()

    def on_close(self):
        self.root.destroy()
