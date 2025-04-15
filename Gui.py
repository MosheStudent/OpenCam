import tkinter as tk
from Peer import Peer
import socket

def get_local_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # Connect to an external IP (doesn't actually send data)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]

class StartWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("300x200+100+100")
        self.root.title("Security Camera")

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

        connectButton = tk.Button(self.root, text="Connect", command=self.connect)
        connectButton.pack()

        self.root.mainloop()

    def connect(self):
        remote_ip = self.entryIP.get()
        camera_index = int(self.entryCameraIndex.get())

        if remote_ip:
            self.root.destroy()
            peer = Peer(remote_ip=remote_ip, camera_index=camera_index)
            peer.start()
        else:
            self.show_error("Please enter a valid IP address.")

    def show_error(self, message):
        error_window = tk.Toplevel(self.root)
        error_window.geometry("200x100")
        error_window.title("Error")
        label = tk.Label(error_window, text=message)
        label.pack()
        close_button = tk.Button(error_window, text="Close", command=error_window.destroy)
        close_button.pack()
