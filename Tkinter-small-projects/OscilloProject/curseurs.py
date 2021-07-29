"""
Python book oscillo
Madipoupou
14/07/2020
"""

import tkinter as tk
from math import pi

# CLASS DEFINITION

class ChoixVibration(tk.Frame):
    """ Curseurs pour choisir fréquence, phase et amplitude d'une vibration """
    def __init__(self, boss=None, color='red'):
        tk.Frame.__init__(self)
        self.configure(bd=2, relief=tk.GROOVE)
        # Init attributs objets
        self.freq, self.phase, self.ampl, self.color = 0, 0, 0, color
        # Variable etat checkbox et checkbox
        self.chk = tk.IntVar() #objet-variable tkinter
        tk.Checkbutton(
            self, text='Afficher', variable=self.chk, fg='black',
            command=self.set_curve
        ).pack(side=tk.LEFT, padx=5, pady=5)
        # Definition des curseurs
        tk.Scale(
            self, length=200, orient=tk.HORIZONTAL, sliderlength=25,
            label='Fréquence (Hz):', from_=1., to=9., tickinterval=2,
            resolution=0.25, showvalue=1, command=self.set_frequency, troughcolor='dark grey'
        ).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Scale(
            self, length=200, orient=tk.HORIZONTAL, sliderlength=15,
            label='Phase (degrés):', from_=-180, to=180, tickinterval=90,
            showvalue=1, command=self.set_phase, troughcolor='dark grey'
        ).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Scale(
            self, length=200, orient=tk.HORIZONTAL, sliderlength=25,
            label='Amplitude:', from_=1, to=9, tickinterval=2,
            showvalue=1, command=self.set_amplitude, troughcolor='dark grey'
        ).pack(side=tk.LEFT, padx=5, pady=5)
    
    def set_curve(self):
        self.event_generate('<Control-Z>')
    
    def set_frequency(self, f):
        self.freq = float(f)
        self.event_generate('<Control-Z>')
    
    def set_phase(self, p):
        self.phase = float(p)
        self.event_generate('<Control-Z>')
    
    def set_amplitude(self, a):
        self.ampl = float(a)
        self.event_generate('<Control-Z>')
    
    def get_values(self):
        return ((self.freq, self.phase, self.ampl))
