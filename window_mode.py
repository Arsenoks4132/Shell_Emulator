from tkinter import Tk, Entry, Button, Text
import tkinter as tk


class Window:
    def __init__(self, terminal):
        self.terminal = terminal

        self.window = Tk()
        self.window.geometry('854x480')
        self.window.resizable(False, False)
        self.window.title("Danov Shell Emulator")

        self.console = Text(width=105, height=25, borderwidth=1, relief='solid')
        self.console.configure(state=tk.DISABLED)

        self.enter = Entry(width=100)

        self.butn = Button(text="Enter")
        self.butn.bind('<Button-1>', self.read_command)
        self.enter.bind('<Return>', self.read_command)

        self.console.pack(pady=10)
        self.enter.pack()
        self.butn.pack()

        self.terminal.attach(self)
        self.window.mainloop()

    def write(self, message):
        self.console.configure(state=tk.NORMAL)
        self.console.insert(tk.END, message)
        self.console.configure(state=tk.DISABLED)

    def read_command(self, event):
        command = self.enter.get()
        self.terminal.command_dispatcher(command)
        self.enter.delete(0, tk.END)