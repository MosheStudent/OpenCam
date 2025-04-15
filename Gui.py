import tkinter as tk
from Peer import Sender, Receiver
import socket

def get_local_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # Connect to an external IP (doesn't actually send data)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]

def is_valid_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

class StartWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("300x200+100+100")
        self.root.title("Security Camera")

        self.displayWin()

    def displayWin(self):
        label = tk.Label(self.root, text="Choose Mode:")
        label.pack()

        senderButton = tk.Button(self.root, text="Send Video", command=self.start_sender)
        senderButton.pack()

        receiverButton = tk.Button(self.root, text="Receive Video", command=self.start_receiver)
        receiverButton.pack()

        self.root.mainloop()

    def start_sender(self):
        self.root.destroy()
        SenderWindow()

    def start_receiver(self):
        self.root.destroy()
        ReceiverWindow()


class SenderWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("300x200+100+100")
        self.root.title("Send Video")

        self.displayWin()

    def displayWin(self):
        label = tk.Label(self.root, text="Enter the remote device's IP:")
        label.pack()

        self.entryIP = tk.Entry(self.root)
        self.entryIP.pack()

        label2 = tk.Label(self.root, text="Enter your camera index (default is 0):")
        label2.pack()

        self.entryCameraIndex = tk.Entry(self.root)
        self.entryCameraIndex.insert(0, "0")  # Default camera index
        self.entryCameraIndex.pack()

        connectButton = tk.Button(self.root, text="Start Sending", command=self.start_sending)
        connectButton.pack()

        self.root.mainloop()

    def start_sending(self):
        remote_ip = self.entryIP.get()
        camera_index = int(self.entryCameraIndex.get())

        if not is_valid_ip(remote_ip):
            self.show_error("Invalid IP address.")
            return

        self.root.destroy()
        sender = Sender(remote_ip=remote_ip, camera_index=camera_index)
        sender.start()

    def show_error(self, message):
        error_window = tk.Toplevel(self.root)
        error_window.geometry("200x100")
        error_window.title("Error")
        label = tk.Label(error_window, text=message)
        label.pack()
        close_button = tk.Button(error_window, text="Close", command=error_window.destroy)
        close_button.pack()


class ReceiverWindow:
    def __init__(self):
        # Automatically start receiving video
        self.start_receiving()

    def start_receiving(self):
        receiver = Receiver()
        receiver.start()
