import Gui
import Peer

class Main:
    def __init__(self):
        self.REMOTE_IP = ''
        self.local_peer = Peer(self.REMOTE_IP, 0)

        self.inputWin = Gui.InputWindow()
        

    def setUp(self):
        self.REMOTE_IP = self.inputWin.display()
    
    def connect(self):
        self.local_peer.start()


"""if __name__ == "__main__":
    main()"""
    