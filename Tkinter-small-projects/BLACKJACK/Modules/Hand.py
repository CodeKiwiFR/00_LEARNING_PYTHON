class Hand:
    def __init__(self):
        self.content = []
        self.score = 0
    
    def __str__(self):
        temp_str = ''
        if (self.content):
            for card in self.content:
                temp_str += str(card) + '\n'
        else:
            temp_str += 'EMPTY HAND'
        return (temp_str)
    
    def add_card(self, card):
        self.content.append(card)
        self.update_score()
    
    def update_score(self):
        score = 0
        ace = 0
        for card in self.content:
            if (card.hidden):
                self.score = -1
                return
            if (card.name == '1'):
                ace += 1
                score += 11
            elif (card.name in ('2', '3', '4', '5', '6', '7', '8', '9', '10')):
                score += int(card.name)
            elif (card.name in ('j', 'q', 'k')):
                score += 10
        if (score > 21 and ace > 0):
            for _ in range(ace):
                if (score > 21):
                    score -= 10
                else:
                    break
        self.score = score
    
    def ace_first(self):
        return (len(self.content) == 2 and not self.content[0].hidden and self.content[0].name == '1')
    
    def clean(self):
        self.content.clear()
        self.update_score()

    def reveal_hand(self):
        for card in self.content:
            card.reveal_card()
            self.update_score()