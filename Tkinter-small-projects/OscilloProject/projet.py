"""
Python oscillo and cursor project
Madipoupou
15/07/2020
"""

import tkinter as tk
from oscillo import OscilloGraphe
from curseurs import ChoixVibration

# CLASS DEFINITION
class ShowVibrations(tk.Frame):
    """ Demo de mouvements vibratoires harmoniques """
    def __init__(self, boss=None):
        # Init
        tk.Frame.__init__(self)
        self.color = ['dark green', 'red', 'purple', 'yellow']
        self.trace = [0]*4
        self.ctrl = [0]*4

        # Canvas creation
        self.graph = OscilloGraphe(self, width=800, height=400)
        self.graph.configure(bg='white', bd=2, relief=tk.SOLID)
        self.graph.pack(side=tk.TOP, padx=10, pady=10)

        # Cursors panel
        for i in range(4):
            self.ctrl[i] = ChoixVibration(self, self.color[i])
            self.ctrl[i].pack(padx=10, pady= 10)
        
        # Define the display manager event
        self.master.bind('<Control-Z>', self.montrer_courbes)
        self.master.title('Mouvements vibratoires harmoniques')
        self.pack(padx=10, pady=10)

        self.montrer_courbes(None)
    
    def montrer_courbes(self, event):
        """ Displaying our three graphs """
        for i in range(4):
            # Cleaning previous curve if necessary
            self.graph.delete(self.trace[i])

            # Drawing the new curve
            if (self.ctrl[i].chk.get()):
                freq, phase, ampl = self.ctrl[i].get_values()
                self.trace[i] = self.graph.plot_curve(
                    color=self.color[i],
                    freq=freq,
                    phase=phase,
                    ampl=ampl,
                )

# MAIN PROGRAM
if (__name__ == '__main__'):
    main = tk.Tk()
    ShowVibrations(main).pack()
    main.bind('<Escape>', lambda event: main.destroy())
    main.mainloop()