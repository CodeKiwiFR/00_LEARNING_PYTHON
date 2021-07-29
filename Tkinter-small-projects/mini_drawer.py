"""
Mouth detector
Madipoupou
09/05/2020
"""

import tkinter as tk

# --- FUNCTIONS ---
def circle(x, y, r, can, color='black'):
    """
    Draw a circle...
    """
    return (can.create_oval(x-r, y-r, x+r, y+r, outline=color, width=3))

def pointer(event, label, can, pressed):
    label.configure(text=f'Click on x = {event.x} - y = {event.y}')
    if pressed:
        circle(event.x, event.y, 1, can, color='red')

def draw_manager(event, state):
    global pressed
    pressed = state


# --- MAIN PROGRAM ---
if __name__ == '__main__':
    pressed = False
    win = tk.Tk()
    can = tk.Canvas(win, width=400, height=400, bg='white')
    can.bind('<Motion>', lambda event: pointer(event, my_str, can, pressed))
    can.bind('<Button-1>', lambda event: draw_manager(event, True))
    can.bind('<ButtonRelease-1>', lambda event: draw_manager(event, False))
    can.pack(side=tk.TOP, padx=5, pady=5)
    my_str = tk.Label(win)
    my_str.pack(side=tk.LEFT, padx=5, pady=5)
    exit_but = tk.Button(win, text='Exit', command=win.quit)
    exit_but.pack(side=tk.RIGHT, padx=5, pady=5)

    win.mainloop()
