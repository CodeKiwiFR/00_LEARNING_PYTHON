"""
Python book oscillo
Madipoupou
14/07/2020
"""

import tkinter as tk
from math import sin, pi

class OscilloGraphe(tk.Canvas):
    """ Canvas adapted to physics graphs """
    def __init__(self, boss=None, width=200, height=150):
        """ Constructor of the graph """
        tk.Canvas.__init__(self)
        self.margin = 40
        self.configure(width=width, height=height, bg='blue')
        self.width, self.height = width, height
        stepx = (width - self.margin) / 8.
        for t in range(0, 9):
            stx = t * stepx  + self.margin/2
            self.create_line(stx, self.margin/2, stx, height-self.margin/2, fill='lightgray')
        stepy = (height - self.margin) / 10
        for h in range(0, 11):
            self.create_line(self.margin/2, h*stepy+self.margin/2, width-self.margin/2, h*stepy+self.margin/2, fill='lightgray')
        self.create_line(self.margin/2, height/2, width, height/2, arrow=tk.LAST)
        self.create_line(self.width/2, height-5, self.width/2, 5, arrow=tk.LAST)
    
    def plot_curve(self, freq=1, phase=0, ampl=10, color='red'):
        """ Plot a curve on the canvas """
        curve = []
        step = (self.width - (self.margin)) / 1000
        for t in range(0, 1001, 5):
            e = ampl * sin(2*pi * freq * t / 1000 - phase)
            x = self.margin/2 + t * step
            y = self.height / 2 - e * self.height / 25
            curve.append((x, y))
        n = self.create_line(curve, fill=color, smooth=1)
        return n
