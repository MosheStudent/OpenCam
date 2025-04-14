import tkinter as tk
import random
from Peer import Peer  # Import the Peer class
import PasswordBrdcst
import socket
import threading

class HostWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("300x300+100+100")
        self.root.title("Host Meeting")
        
        self.PASSWORD = PasswordBrdcst.GenPassword()  # Generate a random password

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)  # Handle "X" button
        self.displayWin()

    def displayWin(self):
        label = tk.Label(self.root, text=f'password: {self.PASSWORD}')
        label.pack()

        label2 = tk.Label(self.root, text="Waiting for connection...")
        label2.pack()

        startButton = tk.Button(self.root, text="Start Meeting", command=self.startMeeting)
        startButton.pack()

        self.root.mainloop()

    def startMeeting(self):
        PasswordBrdcst.send_password(self.PASSWORD)  # Send the password to the network

        # Wait for connection confirmation
        threading.Thread(target=self.wait_for_confirmation_and_start).start()

    def wait_for_confirmation_and_start(self):
        if self.wait_for_confirmation():
            self.root.destroy()
            # Start the Peer instance for hosting
            peer = Peer(remote_ip="127.0.0.1", camera_index=0)  # Use localhost for hosting
            peer.start()
        else:
            self.show_error("Connection confirmation failed!")

    def wait_for_confirmation(self, port=12346):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind(('', port))
            s.settimeout(30)  # Wait for 30 seconds for confirmation
            try:
                data, addr = s.recvfrom(1024)
                return data.decode('utf-8') == "CONFIRMED"
            except socket.timeout:
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

        threading.Thread(target=self.validate_and_start, args=(password, ip)).start()

    def validate_and_start(self, password, ip):
        realPass = PasswordBrdcst.recv_password()
        
        if password == realPass:  
            self.send_confirmation(ip)
            self.root.destroy()
            # Start the Peer instance for joining
            peer = Peer(remote_ip=ip, camera_index=0)  # Use the entered IP
            peer.start()
        else:
            self.show_error("Password is incorrect!")

    def send_confirmation(self, ip, port=12346):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
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
