#! /usr/bin/env python
import Tkinter as tk

def say_hello():
    print("hello")

r = tk.Tk()
r.title('Hello World')

fBtn = tk.Button(r, text='Forward', width = 15, height = 10, command=say_hello)
fBtn.pack()
lBtn = tk.Button(r, text='Left', width = 15, height = 10, command=say_hello)
lBtn.pack()

r.mainloop()
