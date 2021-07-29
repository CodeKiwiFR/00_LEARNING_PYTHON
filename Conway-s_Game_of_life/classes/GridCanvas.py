"""
Python - Game of life with tkinter
06/06/2020
Madipoupou
"""

import tkinter as tk

class GridCanvas(tk.Canvas):
    """
    Class which manages a specific canvas designed to be a grid
    """
    def __init__(self, boss, width=1000, height=600, cell_size=20):
        """ GridCanvas constructor """
        tk.Canvas.__init__(self, boss)
        self.configure(width=width, height=height, bg='white')
        self.cell_size = cell_size
        self.width = width
        self.height = height
        self.origin = (0, 0)
        self.lines = []
        self.render_grid()
        self.focus_set()
        self.obj = None # If an object is put on canvas it can be saved
        self.bind('<Control_L>', lambda event: self.zoom(2))
        self.bind('<Control_R>', lambda event: self.zoom(-2))
        self.bind('<Up>', lambda event: self.move(0, 1))
        self.bind('<Down>', lambda event: self.move(0, -1))
        self.bind('<Left>', lambda event: self.move(-1, 0))
        self.bind('<Right>', lambda event: self.move(1, 0))

    def render_grid(self):
        """ Draws the grid on the canvas """
        self.delete('all')
        for x in range(0, self.width, self.cell_size):
            self.lines.append(self.create_line(x, 0, x, self.height))
        for y in range(self.height, 0, -self.cell_size):
            self.lines.append(self.create_line(0, y, self.width, y))
    
    def zoom(self, coeff):
        """ Zoom in or zoom out in Canvas """
        # Calculating the middle cell coord
        xmiddle = self.origin[0] + (self.width // 2) // self.cell_size
        ymiddle = self.origin[1] + (self.height // 2) // self.cell_size
        
        # Saving new cell size
        self.cell_size += coeff
        if (self.cell_size <= 1):
            self.cell_size = 1

        # Finding new origin and saving it
        xor = xmiddle - (self.width // 2) // self.cell_size
        yor = ymiddle - (self.height // 2) // self.cell_size
        self.origin = (xor, yor)
        self.render_grid()
        if (self.obj):
            self.obj.refresh(self)
    
    def move(self, xmove, ymove):
        """ Move on the canvas """
        self.origin = (self.origin[0] + xmove, self.origin[1] + ymove)
        self.render_grid()
        if (self.obj):
            self.obj.refresh(self)
    
    def get_cell_click(self, event):
        return ((
            event.x // self.cell_size + self.origin[0], 
            (self.height - event.y) // self.cell_size + self.origin[1]
        ))