from tkinter import Tk, Entry, Label, Button, Text
import tkinter as tk


class Window:
    def __init__(self):
        self.window = Tk()
        self.window.geometry('854x480')
        self.window.resizable(False, False)
        self.window.title("Danov Shell Emulator")
        self.window.mainloop()

        self.console = Text(width=105, height=25, borderwidth=1, relief='solid')
        self.console.configure(state=tk.DISABLED)
        self.enter = Entry(width=100)
        self.butn = Button(text="Enter")

        self.console.pack(pady=10)
        self.enter.pack()
        self.butn.pack()

    def write(self, message):
        self.console.configure(state=tk.NORMAL)
        self.console.insert(tk.END, message + '\n')
        self.console.configure(state=tk.DISABLED)

