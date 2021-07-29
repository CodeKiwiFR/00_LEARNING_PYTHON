"""
Small snake game
Madipoupou
14/05/2020

TODOS:
- Fix direction bug: if we press two buttons consecutively we can chose an invalid position
- Create blocks around the grid like rocks the snake has to avoid
- Create the gameover overlay
- Create a starting menu
- Add fruits and fun
- Manage the score
- Deal with snake "autocollison"
- Do some funny things to make an atypical snake game
"""

import tkinter as tk
from WindowCanvas import WindowCanvas
from random import randrange


# --- CLASSES ---
class Grid:
    """
    Manages the grid
    """
    def __init__(self, width, height, cell_size=10, color='pink', bg='white', outline='gray'):
        """
        Creating the window, the canvas, setting all the variables and binding buttons
        """
        self.wc = WindowCanvas('SNAKE', width, height, bg)
        self.width = width
        self.height = height
        self.cells = {
            'size': cell_size,
            'width': self.width // cell_size,
            'height': self.height // cell_size
        }
        self.snake = None
        self.pause = False
        self.color = color
        self.can = self.wc.can
        self.win = self.wc.win
        self.win.bind('<Left>', lambda event: self.move('L'))
        self.win.bind('<Right>', lambda event: self.move('R'))
        self.win.bind('<Up>', lambda event: self.move('U'))
        self.win.bind('<Down>', lambda event: self.move('D'))
        self.win.bind('<Escape>', lambda event: self.manage_pause())
    
    def start_game(self):
        """
        Initializing the game: creating the snake, launching fruits creation and event loop
        """
        self.snake = Snake(self.cells, self.color, 30, self.can, self.win, self)
        self.fruits = Fruit(self.cells, self, self.win)
        self.win.after(2500, lambda: Fruit.create_apple(self.snake.head_position(), self.cells, self))
        self.wc.start_win()

    def manage_pause(self):
        """
        If the player presses escape the game is paused
        """
        if (not self.snake):
            return
        if (not self.pause):
            self.pause = True
            self.snake.moving = False
        else:
            self.pause = False
            self.snake.moving = True
            self.snake.start_snake()

    def move(self, char, event=None):
        """
        Setting the snake direction
        """
        if (self.snake):
            self.snake.set_direction(char)

    def draw_cell(self, row, col, color):
        """
        Drawing a cell - the cell is a square
        """
        half_size = self.cells['size'] // 2
        y = row * self.cells['size'] + half_size
        x = col * self.cells['size'] + half_size
        return (self.can.create_rectangle(x-half_size, y-half_size, x+half_size, y+half_size, fill=color, outline='gray'))
    
    def draw_circle(self, row, col, color):
        """
        Drawing a circle on a cell
        """
        half_size = self.cells['size'] // 2
        y = row * self.cells['size'] + half_size
        x = col * self.cells['size'] + half_size
        return (self.can.create_oval(x-half_size, y-half_size, x+half_size, y+half_size, fill=color))

class Snake:
    """
    Manages the snake
    """
    def __init__(self, cells, color, speed, can, win, grid):
        """
        Initializing the snake - calculating its position - drawing the initial snake
        """
        row0 = cells['height'] // 2
        col0 = cells['width'] // 2
        self.grid = grid
        self.game_over = False
        self.cells = cells
        self.moving = False
        self.can = can
        self.win = win
        self.speed = speed
        self.color = color
        self.size = cells['size']
        self.direction = None
        self.body = [self.create_block(row0, col0), self.create_block(row0 + 1, col0)]
    
    def create_block(self, row, col):
        """
        Creating a block which will be part of the snake
        """
        return ({
            'add': self.grid.draw_cell(row, col, self.color),
            'row': row,
            'col': col
        })

    def update_coord(self, add, row, col):
        """
        Moving a drawn cell to (row,col) position. Calculates the (x,y) corresponding coordinates
        """
        half_size = self.size // 2
        y = row * self.size + half_size
        x = col * self.size + half_size
        self.can.coords(add, x-half_size, y-half_size, x+half_size, y+half_size)

    def set_direction(self, dir):
        """
        Updating the snake direction according to game constraints
        Dealing with position initial setting
        """
        if (not self.direction):
            self.direction = dir
            self.moving = True
            self.win.after(self.speed, self.start_snake)
            return
        if ((not self.moving) or (self.direction == 'U' and dir == 'D') or (self.direction == 'D' and dir == 'U') or (self.direction == 'L' and dir == 'R') or (self.direction == 'R' and dir == 'L')):
            return
        self.direction = dir

    def start_snake(self):
        """
        Managing the snake moving loop
        Dealing with eating fruits
        Dealing with moving state and game over
        """
        eaten = self.check_fruit()
        index = len(self.body) - 1
        if (eaten):
            temp = self.create_block(self.body[index]['row'], self.body[index]['col'])
            self.body.append(temp)
            self.speed -= 1
        while (index > 0):
            self.body[index]['row'] = self.body[index - 1]['row']
            self.body[index]['col'] = self.body[index - 1]['col']
            self.update_coord(self.body[index]['add'], self.body[index]['row'], self.body[index]['col'])
            index -= 1
        if (self.direction in ('U', 'D')):
            self.body[index]['row'] += 1 if self.direction == 'D' else -1
        else:
            self.body[index]['col'] += 1 if self.direction == 'R' else -1
        self.update_coord(self.body[index]['add'], self.body[index]['row'], self.body[index]['col'])
        if (not self.game_over and self.moving):
            self.win.after(self.speed, self.start_snake)
    
    def head_position(self):
        """
        Returning the snake's head position
        """
        return (self.body[0]['row'], self.body[0]['col'])

    def check_fruit(self):
        """
        Checking if the snake is eating a fruit (head's position = fruit's position)
        """
        snake_pos = self.head_position()
        fruit_pos = Fruit.get_pos()
        if (fruit_pos and fruit_pos == snake_pos):
            Fruit.delete_apple(snake_pos, self.cells, self.grid)
            return 1
        return 0

class Fruit:
    """
    Manages the Fruits
    """
    def __init__(self, cells, grid, win):
        Fruit.apple = {}
    
    @classmethod
    def create_apple(self, snake_pos, cells, grid):
        """
        Creates an apple on the given grid
        Position is randomly generated but has to be far from the given snake
        """
        if (not Fruit.apple):
            row = randrange(cells['height'])
            while (abs(row - snake_pos[0]) < cells['height'] // 4):
                row = randrange(cells['height'])
            col = randrange(cells['width'])
            while (abs(col - snake_pos[0]) < cells['width'] // 4):
                col = randrange(cells['width'])
            add = grid.draw_circle(row, col, 'red')
            Fruit.apple = {
                'add': add,
                'row': row,
                'col': col
            }
    
    @classmethod
    def delete_apple(self, snake_pos, cells, grid):
        """
        Delete a fruit from the grid and generating another one after 2.5sec
        """
        grid.can.delete(Fruit.apple['add'])
        Fruit.apple = {}
        grid.win.after(2500, lambda: Fruit.create_apple(snake_pos, cells, grid))

    @classmethod
    def get_pos(self):
        """
        Returns a tuple for the postion of the fruit
        """
        if (Fruit.apple):
            return ((Fruit.apple['row'], Fruit.apple['col']))
        return {}

    
# --- MAIN PROGRAM ---
if (__name__ == '__main__'):
    grid = Grid(1000, 800, 20, color='blue', bg='light gray', outline='black')
    grid.start_game()