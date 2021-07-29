from .Hand import Hand

class Player:
    def __init__(self):
        self.name = 'PLAYER'
        self.hand = Hand()
        self.bet = 0
        self.money = 0
        self.init_money = 0
    
    def __str__(self):
        return (f'Name: {self.name} - Money: {self.money}$')  

    def make_bet(self, amount):
        if (0 <= amount <= self.money):
            self.bet += amount
            self.money -= amount
    
    def print_hand(self):
        print(f'{self.name}\'s hand:')
        print(self.hand)

class Dealer(Player):
    def __init__(self):
        super().__init__()
        self.name = 'DEALER'
        self.money = 1000000

    def deal(self, num, hand, hidden, deck):
        if (not deck or not hand or num == 0):
            return
        for _ in range(num):
            temp_card = deck.deal_one()
            if (hidden):
                temp_card.hide_card()
            else:
                temp_card.reveal_card()
            hand.add_card(temp_card)
