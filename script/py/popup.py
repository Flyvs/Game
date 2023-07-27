import tkinter as tk
from tkinter import messagebox

class Error():
    def __init__(self, error_message: str):
        self.error_message = error_message
        self.show()

    def show(self):
        root = tk.Tk()
        root.withdraw()

        messagebox.showerror("An error occured", self.error_message)

        root.destroy()