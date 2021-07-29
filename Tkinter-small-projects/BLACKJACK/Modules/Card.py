class CardError(Exception):
    pass

class Card:
    possible_colors = ('clubs', 'diamonds', 'hearts', 'spades')
    possible_names = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'j', 'q', 'k')

    def __init__(self, color, name):
        self.check_error(color, name)
        self.color = color
        self.name = name.lower()
        self.hidden = False

    def __str__(self):
        if (not self.hidden):
            return (f'{self.color[0].upper()} - {self.name.upper()}     ')
        return ('HIDDEN CARD')

    def check_error(self, color, name):
        if (color.lower() not in Card.possible_colors or name.lower() not in Card.possible_names):
            raise CardError
    
    def hide_card(self):
        self.hidden = True

    def reveal_card(self):
        self.hidden = False
        