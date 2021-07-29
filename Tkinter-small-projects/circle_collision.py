"""
Animation 2
Madipoupou
09/08/2020
"""

import tkinter as tk
from random import randrange

# --- FUNCTIONS ---
def circle(x, y, r, can, color='black'):
    """
    Draw a circle...
    """
    return (can.create_oval(x-r, y-r, x+r, y+r, fill=color))

class Token:
    colors = ['blue', 'red', 'yellow', 'purple', 'white', 'gray', 'green', 'light green', 'light gray', 'cyan', 'salmon', 'dark blue', 'orange']
    tokens_list = []
    def __init__(self, x1, y1, can, win, radius, speed):
        self.x1, self.y1 = x1, y1
        self.radius = radius
        self.can = can
        self.max_speed = 15
        self.min_speed = 5
        self.add = circle(x1, y1, radius, can, Token.colors[randrange(len(self.colors))])
        self.moving = False
        self.win = win
        self.dx, self.dy = randrange(speed-2, speed), randrange(speed-2, speed)
        self.tokens_list.append(self)
    
    def move(self):
        self.x1 += self.dx
        self.y1 += self.dy
        for item in Token.tokens_list:
            if (item.add == self.add):
                continue
            min_dist = self.radius + item.radius
            if (self.dist(item) <= 0.8 * min_dist):
                self.x1 = item.x1 + min_dist if (self.x1 > item.x1) else item.x1 - min_dist
                self.y1 = item.y1 + min_dist if (self.y1 > item.y1) else item.y1 - min_dist
            elif (self.dist(item) < min_dist):
                self.dx *= -1
                self.dy *= -1
        if (self.x1 >= 600 - self.radius):
            self.dx = -randrange(self.min_speed, self.max_speed)
            self.can.itemconfig(self.add, fill = Token.colors[randrange(len(self.colors))])
        if (self.y1 >= 600 - self.radius):
            self.dy = -randrange(self.min_speed, self.max_speed)
            self.can.itemconfig(self.add, fill = Token.colors[randrange(len(self.colors))])
        if (self.x1 < self.radius):
            self.dx = randrange(self.min_speed, self.max_speed)
            self.can.itemconfig(self.add, fill = Token.colors[randrange(len(self.colors))])
        if (self.y1 < self.radius):
            self.dy = randrange(self.min_speed, self.max_speed)
            self.can.itemconfig(self.add, fill = Token.colors[randrange(len(self.colors))])
        self.can.coords(self.add, self.x1-self.radius, self.y1-self.radius, self.x1+self.radius, self.y1+self.radius)
        if (self.moving):
            self.win.after(15, lambda: self.move())

    def start_move(self):
        if not self.moving:
            self.moving = True
            self.move()

    def stop_move(self):
        self.moving = False
    
    def dist(self, item):
        d1 = self.x1 - item.x1
        d2 = self.y1 - item.y1
        return int((d1**2 + d2**2) ** 0.5)

def start_all(items):
    for item in items:
        item.start_move()

def stop_all(items):
    for item in items:
        item.stop_move()

# --- MAIN PROGRAM ---
if __name__ == '__main__':
    win = tk.Tk()
    win.title('ANIMATION #1')

    can = tk.Canvas(win, width=600, height=600, bg='black')
    can.grid(row=0, column=0, padx=5, pady=5)

    # Circle variables
    items = []
    items.append(Token(300, 300, can, win, 40, 10))
    items.append(Token(100, 100, can, win, 15, 5))
    items.append(Token(100, 500, can, win, 25, -3))
    items.append(Token(500, 500, can, win, 50, -6))
    items.append(Token(400, 400, can, win, 10, -6))
    items.append(Token(200, 200, can, win, 10, -6))
    items.append(Token(550, 350, can, win, 10, -6))
    frame_but = tk.Frame(win, highlightbackground='gray', highlightthickness=2, bg='light gray')
    frame_but.grid(row=0, column=1, padx=5, pady=5, sticky=tk.N)
    start_but = tk.Button(frame_but, text='Start', command=lambda: start_all(items), bg='blue', fg='white')
    start_but.grid(row=0, padx=5, pady=5)
    stop_but = tk.Button(frame_but, text='Stop', command=lambda: stop_all(items), bg='red', fg='white')
    stop_but.grid(row=1, padx=5, pady=5)
    tk.Button(win, text='Exit', command=win.quit).grid(row=1, columnspan=2, padx=5, pady=5, sticky=tk.S)

    win.mainloop()
