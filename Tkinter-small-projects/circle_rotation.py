"""
Animation - circle move
Madipoupou
13/05/2020
"""

import tkinter as tk
from math import cos, sin, acos, asin
from WindowCanvas import WindowCanvas

# --- Class ---
class Item:
    def __init__(self, x, y, r, speed, color, wc, sign=1):
        self.add = win.circle(x, y, r, color)
        self.dist = int(((x - wc.xcenter)**2 + (y - wc.ycenter)**2) ** 0.5)
        if (x - wc.xcenter >= 0):
            self.angle = asin((wc.ycenter - y) / self.dist)
        else:
            self.angle = acos((x - wc.xcenter) / self.dist)
        self.speed = speed
        self.r = r
        self.color = color
        self.moving = False
        self.dx = sign * 3.14159 / 128
        self.wc = wc

    def circle_move(self):
        self.angle += self.dx
        self.x = int(self.wc.xcenter + self.dist * cos(self.angle))
        self.y = int(self.wc.ycenter - self.dist * sin(self.angle))
        self.wc.can.coords(self.add, self.x-self.r, self.y-self.r, self.x+self.r, self.y+self.r)
        if (self.moving):
            self.wc.win.after(self.speed, self.circle_move)
            
    def start_move(self):
        if (not self.moving):
            self.moving = True
            self.circle_move()

    def stop_move(self):
        self.moving = False

# --- Functions ---
def start(items):
    for item in items:
        item.start_move()

def stop(items):
    for item in items:
        item.stop_move()

# --- Main program ---
win = WindowCanvas('Circle Animation', 800, 800, 'white')
frame_but = tk.Frame(win.win, highlightbackground='gray', highlightthickness=2, bg='light gray')
frame_but.grid(row=0, column=1, padx=5, pady=5, sticky=tk.N)
start_but = tk.Button(frame_but, text='Start', command=lambda: start(items), bg='blue', fg='white')
start_but.grid(row=0, padx=5, pady=5)
stop_but = tk.Button(frame_but, text='Stop', command=lambda: stop(items), bg='red', fg='white')
stop_but.grid(row=1, padx=5, pady=5)

items = []
items.append(Item(147, 136, 8, 15, 'yellow', win, -1))
items.append(Item(255, 312, 15, 25, 'cyan', win))
items.append(Item(100, 100, 50, 35, 'blue', win, -1))
items.append(Item(200, 300, 30, 10, 'green', win))
win.circle(400, 400, 5, 'dark gray')

win.start_win()