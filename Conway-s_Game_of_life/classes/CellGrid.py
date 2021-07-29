"""
Python - Game of life with tkinter
06/06/2020
Madipoupou
"""

class CellGrid(object):
    """
    Class which manages the cell grid
    Registers the active cells into a list
    Deals with lifecycle of cells
    """
    def __init__(self, alive_cells=[]):
        """ CellGrid constructor """
        self.alive_cells = alive_cells
        self.rectangle_ref = []
        self.saved_cells = None
        self.cycle_num = 0
    
    def __str__(self):
        """ CellGrid string converter """
        res = ''
        for cell in self.alive_cells:
            res += str(cell) + '\n'
        return res
    
    def replace_current_cells(self, cell_lst, can):
        """
        Replace the current alive cells by the given list and render
        If the reset hasn't been made we make it
        """
        if (self.alive_cells or self.rectangle_ref):
            self.reset(can)
        self.alive_cells = cell_lst.copy()
        self.render_cells(can)

    def refresh(self, can):
        """ If a canvas calls it we refresh the display """
        self.render_cells(can)

    def activate_cycle(self):
        """
        Does one cycle -> updates the cell list from previous round to the next
        """
        new_cells = []
        cells_to_check = self.get_cells_to_check()
        for cell in cells_to_check:
            if (self.check_next_status(cell)):
                new_cells.append(cell)
        self.alive_cells = new_cells
        self.cycle_num += 1
    
    def get_cells_to_check(self):
        """ Returns a list of the cells which needs to be checked """
        cells_to_check = []
        for cell in self.alive_cells:
            for i in range(cell[0] - 1, cell[0] + 2):
                for j in range(cell[1] - 1, cell[1] + 2):
                    if ((i, j) not in cells_to_check):
                        cells_to_check.append((i, j))
        return cells_to_check

    def check_next_status(self, cell):
        """
        Checks the status of cell arg for the next round
        True if alive, False if dead
        """
        alive_neighbor = 0
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if ((i, j) == cell):
                    continue
                elif ((i, j) in self.alive_cells):
                    alive_neighbor += 1
                if (alive_neighbor > 3):
                    return False
        if (alive_neighbor not in (2, 3)):
            return False
        if (cell in self.alive_cells):
            return True
        return (alive_neighbor == 3)
    
    def render_cells(self, can):
        """ Renders the cells on the given canvas """
        if (not can.obj):
            can.obj = self
        can_xstart = can.origin[0]
        can_xend = can.origin[0] + can.width // can.cell_size + 1
        can_ystart = can.origin[1]
        can_yend = can.origin[1] + can.height // can.cell_size + 1
        cells_to_render = []
        for cell in self.alive_cells:
            if (cell[0] in range(can_xstart, can_xend+1) and cell[1] in range(can_ystart, can_yend)):
                cells_to_render.append(cell)
        # Deleting the old rectangles from canvas
        for rect in self.rectangle_ref:
            can.delete(rect)
            del self.rectangle_ref
            self.rectangle_ref = []
        # Draw each cell
        for cell in cells_to_render:
            self.draw_cell(can, cell)
    
    def draw_cell(self, can, cell):
        """ Draws a cell onto the canvas -> black square """
        new_coord = (cell[0] - can.origin[0], cell[1] - can.origin[1])
        xstart = new_coord[0] * can.cell_size
        ystart = can.height - new_coord[1] * can.cell_size
        self.rectangle_ref.append(can.create_rectangle(
            xstart, ystart, xstart + can.cell_size, ystart - can.cell_size,
            fill='black', outline='white'
        ))
    
    def add_remove_cell(self, cell, can):
        """ Add or remove cell from alive_cells """
        if (cell in self.alive_cells):
            self.alive_cells.remove(cell)
        else:
            self.alive_cells.append(cell)
        self.render_cells(can)
    
    def save_cells(self):
        """ Save current cells """
        del self.saved_cells
        self.saved_cells = self.alive_cells.copy()
    
    def load_cells(self, can):
        """ Come back to saved configuration (does nothing if nothing saved """
        if (self.saved_cells):
            del self.alive_cells
            self.alive_cells = self.saved_cells.copy()
            self.cycle_num = 0
            self.render_cells(can)
        
    def reset(self, can):
        """
        Remove everything from the grid and deleting the element on given canvas
        """
        for rect in self.rectangle_ref:
            can.delete(rect)
        self.alive_cells = []
        self.cycle_num = 0
        self.render_cells(can)
