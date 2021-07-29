from random import shuffle
from .Pack import Pack

class Deck:
    def __init__(self):
        self.deck_content = []
        self.deck_garbage = []
        deck_packs = []
        for _ in range(6):
            deck_packs.append(Pack())
        for pack in deck_packs:
            self.deck_content += pack.deal_all()
    
    def __str__(self):
        return (f'The deck contains {len(self.deck_content)} cards.')

    def __len__(self):
        return (len(self.deck_content))
    
    def shuffle_deck(self):
        shuffle(self.deck_content)
    
    def hide_deck(self):
        for card in self.deck_content:
            card.hide_card()

    def reveal_deck(self):
        for card in self.deck_content:
            card.reveal_card()

    def deal_one(self):
        if (self.deck_content):
            temp_card = self.deck_content.pop()
            self.deck_garbage.append(temp_card)
            return (temp_card)
        else:
            self.deck_content = self.deck_garbage
            self.deck_garbage = []
            self.shuffle_deck()
            return (self.deal_one())