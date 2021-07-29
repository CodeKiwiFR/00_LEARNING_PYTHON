"""
Python - Game of life with tkinter
06/06/2020
Madipoupou
"""

from tkinter import filedialog
from .GridCanvas import GridCanvas
from .CellGrid import CellGrid
from .Interface import Interface

class App(object):
    """ Class which manages all the application """
    def __init__(self):
        """ Class constructor """
        self.gui = Interface(self)
        self.anim_speed = 100
        self.is_animated = False
        self.create_mode = False
        
        # Initialize grid
        self.grid = CellGrid([])

        self.welcome_menu()

    def main_win(self):
        """ Just a window to test my canvas and the functionalities """
        self.can = self.gui.main_win()

    def reset(self):
        """ Reset all the canvas, cleans all existing cells """
        self.grid.reset(self.can)
        self.gui.cycle_label.configure(text=f'CYCLE: {self.grid.cycle_num}')
        self.anim_speed = 100
        speed = int(1/self.anim_speed * 10000)
        self.gui.speed_label.configure(text=f'SPEED: {speed}%')

    def start_anim(self):
        """ Starts the animation """
        if (not self.is_animated and not self.create_mode):
            self.is_animated = True
            self.animate_game()
            self.gui.start_anim()

    def stop_anim(self):
        """ Stops the animation """
        self.is_animated = False
        self.gui.stop_anim()

    def animate_game(self):
        """ Manages the game animation: clean can, launch cycle, render """
        for rect in self.grid.rectangle_ref:
            self.can.delete(rect)
        self.grid.activate_cycle()
        self.grid.render_cells(self.can)
        self.gui.cycle_label.configure(text=f'CYCLE: {self.grid.cycle_num}')
        if (self.is_animated and not self.create_mode):
            self.gui.after(self.anim_speed, self.animate_game)
        
    def change_speed(self, coeff):
        """ Change animation speed """
        if (coeff < 0):
            self.anim_speed = max(self.anim_speed + coeff, 10)
        else:
            self.anim_speed = min(self.anim_speed + coeff, 1000)
        speed = int(1/self.anim_speed * 10000)
        self.gui.speed_label.configure(text=f'SPEED: {speed}%')

    def create(self):
        """ Manage create mode """
        if (self.create_mode):
            self.create_mode = False
            self.can.unbind('<Button-1>')
            self.gui.create_button.configure(text='CREATE: OFF', bg='dark slate gray')
        else:
            self.stop_anim()
            self.create_mode = True
            self.can.bind('<Button-1>', lambda event: self.grid.add_remove_cell(self.can.get_cell_click(event), self.can))
            self.gui.create_button.configure(text='CREATE: ON', bg='red')

    def welcome_menu(self):
        """ Displays the first menu of the application """

        # Inner function which closes the welcome overlay
        def close_welcome(mode):
            self.destroy_overlay(w_list)
            if (mode == 1):
                self.wip()
            else:
                self.main_win()
        
        w_list = self.gui.welcome_menu(close_welcome)
        self.gui.mainloop()
    
    def wip(self):
        """ Just temporary function to display work in progress message """
        self.gui.wip()

    def destroy_overlay(self, ref_list):
        """ Destroys ref but can be added to welcome_menu method """
        for ref in ref_list:
            ref.destroy()

    def export_to_file(self):
        """ Exports the grid to a file by opening OS explorer """
        if (not self.grid.alive_cells):
            self.gui.top_error('ERROR - The grid is empty')
            return
        filename = filedialog.asksaveasfile(
            parent=self.gui, mode='w', title='Export a pattern'
        )
        if (not filename):
            self.gui.top_error('ERROR - The pattern has not been saved')
            return
        try:
            for cell in self.grid.alive_cells:
                cell_str = f'{cell[0]},{cell[1]}-'
                filename.write(cell_str)
        except:
            self.gui.top_error('ERROR - Writing into the file was not possible')
        finally:
            filename.close()

    def import_from_file(self):
        """ Import a saved grid from a file, opening the explorer """
        filename = filedialog.askopenfilename(title = "Select A File")
        if (not filename):
            return
        try:
            fd = open(filename, 'r')
        except:
            self.gui.top_error('ERROR - Impossible to open the file')
            return
        file_content = fd.read()
        cell_list = file_content.split('-')
        final_cell_list = []
        for cell in cell_list:
            temp = cell.split(',')
            try:
                x = int(temp[0])
                y = int(temp[1])
            except:
                continue
            final_cell_list.append((x, y))
        fd.close()
        if (final_cell_list == []):
            self.gui.top_error('ERROR - The file is not well formatted')
            return
        self.reset()
        self.grid.replace_current_cells(final_cell_list, self.can)
