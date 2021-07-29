"""
Python - Game of life with tkinter
06/06/2020
Madipoupou
"""

import tkinter as tk
import tkinter.font as font
from .GridCanvas import GridCanvas

class Interface(tk.Tk):
    """ This class creates and configure the GUI of the app """
    def __init__(self, app):
        """ Class constructor which initializes the main window """
        tk.Tk.__init__(self)
        self.app = app
        self.icon = tk.PhotoImage(file='./images/ck.png')
        self.my_font = font.Font(family='system', size=15, weight='bold')
        self.iconphoto(False, self.icon)
        self.geometry('1200x700')
        self.geometry('+0+0')
        self.configure(bg='dark slate gray')
        self.resizable(False, False)
        self.title('Conway\'s GAME OF LIFE')
        self.option_add('*Background', 'dark slate gray')

        # Buttons binding
        self.bind('<Escape>', lambda event: self.quit())

        # Preparing file browser (hide hidden files from it)
        self.init_file_browser()
    
    def init_file_browser(self):
        """
        Call a dummy dialog with an impossible option to initialize the file
        dialog without really getting a dialog window; this will throw a
        TclError, so we need a try...except :
        """
        try:
            try:
                self.tk.call('tk_getOpenFile', '-foobarbaz')
            except tk.TclError:
                pass
            # now set the magic variables accordingly
            self.tk.call('set', '::tk::dialog::file::showHiddenBtn', '1')
            self.tk.call('set', '::tk::dialog::file::showHiddenVar', '0')
        except:
            pass
    
    def welcome_menu(self, func_ref):
        """ Displays the first menu of the application """
        # Creating the welcome interface
        self.w_frame = tk.Frame(
            self, bg='slate gray',
            highlightbackground="black", highlightthickness=2
        )
        self.w_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        self.w_but_mode1 = self.default_button(
            self.w_frame, 'PREDEFINED SHAPES', lambda: func_ref(1), width=50
        )
        self.w_but_mode1.pack(padx=15, pady=10)
        self.w_but_mode2 = self.default_button(
            self.w_frame, 'CREATE SHAPES', lambda: func_ref(2), width=50
        )
        self.w_but_mode2.pack(padx=15, pady=10)
        return [self.w_frame, self.w_but_mode1, self.w_but_mode2]
    
    def wip(self):
        """ Just temporary function to display work in progress message """
        self.wip_frame = tk.Frame(
            self, bg='slate gray',
            highlightbackground="black", highlightthickness=2
        )
        self.wip_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.wip_label = tk.Label(
            self.wip_frame, text="Work in progress...",
            font=self.my_font, fg='white', bg='slate gray'
        )
        self.wip_label.pack(padx=55, pady=20)
    
    def main_win(self):
        """ Just a window to test my canvas and the functionalities """

        # Frame which contains all the window -> full window container
        self.container = tk.Frame(self)
        self.container.pack(fill=tk.BOTH, expand=True)

        # Canvas part
        self.can = GridCanvas(boss=self.container)
        self.can.grid(row=0, column=0, padx=5, pady=5)

        # Right panel
        self.right_frame = tk.Frame(
            self.container, bg='slate gray',
            width=175, height=600,
        )
        self.right_frame.grid(row=0, column=1, padx=5, pady=5)
        self.right_frame.grid_propagate(0)
        self.right_frame.columnconfigure(0, weight=1)
        self.start_button = self.default_button(
            self.right_frame, 'START', self.app.start_anim, width=60
        )
        self.start_button.grid(row=0, padx=5, pady=10)

        # Adding create button
        self.create_button = self.default_button(
            self.right_frame, 'CREATE: OFF', self.app.create, width=60
        )
        self.create_button.grid(row=1, padx=5, pady=10)

        # Adding save/reload buttons
        self.default_button(
            self.right_frame, 'SAVE', self.app.grid.save_cells, width=60
        ).grid(row=2, padx=5, pady=10)
        self.default_button(
            self.right_frame, 'LOAD', lambda: self.app.grid.load_cells(self.can) or self.cycle_label.configure(text=f'CYCLE: {self.app.grid.cycle_num}'), width=60
        ).grid(row=3, padx=5, pady=10)

        # Adding speed frame and buttons
        self.speed_frame = tk.Frame(
            self.right_frame, bg='dark slate gray',
            width=170, height=80,
        )
        self.speed_frame.grid(row=4, padx=5, pady=10)
        self.speed_frame.grid_propagate(0)
        self.speed_frame.columnconfigure(0, weight=1)
        tk.Label(
            self.speed_frame, text='SPEED',
            fg='white', font=self.my_font
        ).grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        self.default_button(
            self.speed_frame, '-', lambda: self.app.change_speed(10), bg='slate gray', width=1, height=1
        ).grid(row=1, column=0, padx=5, pady=5, sticky='W')
        self.default_button(
            self.speed_frame, '+', lambda: self.app.change_speed(-10), bg='slate gray', width=1, height=1
        ).grid(row=1, column=1, padx=5, pady=5)

        # Speed and cycle info
        self.speed_label = tk.Label(
            self.right_frame, text='SPEED: 100%',
            bg='slate gray', fg='midnight blue', font=self.my_font
        )
        self.speed_label.grid(row=5, padx=5, pady=(60, 5))
        self.cycle_label = tk.Label(
            self.right_frame, text='CYCLE: 0',
            bg='slate gray', fg='midnight blue', font=self.my_font
        )
        self.cycle_label.grid(row=6, padx=5, pady=5)

        # Bottom panel
        self.bottom_frame = tk.Frame(self.container)
        self.bottom_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        self.default_button(
            self.bottom_frame, 'CLEAR CANVAS', self.app.reset, bg='slate gray'
        ).grid(row=0, column=0, padx=5, pady=15)
        self.default_button(
            self.bottom_frame, 'HELP', lambda: self.app.change_speed(-10), bg='slate gray'
        ).grid(row=0, column=1, padx=5, pady=15)
        self.default_button(
            self.bottom_frame, 'EXPORT GRID', self.app.export_to_file, bg='slate gray'
        ).grid(row=0, column=2, padx=5, pady=15)
        self.default_button(
            self.bottom_frame, 'IMPORT FROM FILE', self.app.import_from_file, bg='slate gray'
        ).grid(row=0, column=3, padx=5, pady=15)
        self.default_button(
            self.bottom_frame, 'EXIT', self.destroy, bg='gray23'
        ).grid(row=0, column=4, padx=5, pady=15)
        return self.can
    
    def default_button(self, parent, text, command_func, bg='dark slate gray', width=15, height=2):
        """
        This creates a default type of button inside parent
        command_func is set as button command
        the button reference is returned
        """
        return (tk.Button(
            parent,
            fg='white', bg=bg, highlightthickness=0,
            font=self.my_font, width=width, height=height,
            text=text, command=command_func
        ))

    def start_anim(self):
        """ Starts the animation """
        self.start_button.configure(
            text='STOP',
            command=self.app.stop_anim,
            bg='slate gray'
        )
    
    def stop_anim(self):
        """ Stops the animation """
        self.start_button.configure(
            text='START',
            command=self.app.start_anim,
            bg='dark slate gray'
        )
    
    def top_error(self, my_str="ERROR"):
        """ A toplevel pops to annouce that an error occured """
        error_win = tk.Toplevel(self)
        error_win.grab_set()
        error_win.geometry('500x400')
        error_win.iconphoto(False, self.icon)
        error_win.geometry('+100+100')
        error_win.resizable(False, False)
        error_win.title('ERROR')
        error_win.bind('<Escape>', lambda event: error_win.destroy())