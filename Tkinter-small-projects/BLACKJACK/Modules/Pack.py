from random import shuffle
from .Card import Card

class Pack:
    def __init__(self):
        self.pack_content = []
        for color in Card.possible_colors:
            for name in Card.possible_names:
                self.pack_content.append(Card(color, name))
    
    def __str__(self):
        pack_str = ""
        for card in self.pack_content:
            pack_str += str(card) + '\n'
        return (pack_str)

    def shuffle_pack(self):
        shuffle(self.pack_content)

    def hide_pack(self):
        for card in self.pack_content:
            card.hide_card()

    def reveal_pack(self):
        for card in self.pack_content:
            card.reveal_card()

    def deal_all(self):
        return (self.pack_content)