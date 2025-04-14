import tkinter as tk
import random
from Peer import Peer  # Import the Peer class

class HostWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("300x300+100+100")
        self.root.title("Host Meeting")
        self.passGen()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)  # Handle "X" button
        self.displayWin()

    def displayWin(self):
        label = tk.Label(self.root, text=f'password: {self.password}')
        label.pack()

        label2 = tk.Label(self.root, text="Waiting for connection...")
        label2.pack()

        startButton = tk.Button(self.root, text="Start Meeting", command=self.startMeeting)
        startButton.pack()

        self.root.mainloop()

    def passGen(self):
        self.password = str(random.randint(1, 1000000))  # Generate a random password

    def startMeeting(self):
        self.root.destroy()
        # Start the Peer instance for hosting
        peer = Peer(remote_ip="127.0.0.1", camera_index=0)  # Use localhost for hosting
        peer.start()

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

        # Simulate password validation (replace with actual logic if needed)
        if password == "123456":  # Replace "123456" with the actual host password
            self.root.destroy()
            # Start the Peer instance for joining
            peer = Peer(remote_ip=ip, camera_index=0)  # Use the entered IP
            peer.start()
        else:
            self.show_error()

    def show_error(self):
        error_window = tk.Toplevel(self.root)
        error_window.geometry("200x100")
        error_window.title("Error")
        label = tk.Label(error_window, text="Password is incorrect!")
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
