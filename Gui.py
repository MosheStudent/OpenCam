import tkinter as tk

class InputWindow:
    def __init__(self):   
        self.REMOTE_IP = ''
        self.window = tk.Tk()

    def getInput(self):
        self.REMOTE_IP = self.entry.get()
        self.window.destroy()

    def display(self):
        self.window.geometry("300x100+100+100")
        self.window.title("Enter Remote IP")

        label = tk.Label(self.window, text="Enter Remote IP:")
        label.pack()

        self.entry = tk.Entry(self.window)
        self.entry.pack()

        enterButton = tk.Button(self.window, text="ENTER", command=self.getInput)
        enterButton.pack()

        self.window.mainloop()

        return self.REMOTE_IP
