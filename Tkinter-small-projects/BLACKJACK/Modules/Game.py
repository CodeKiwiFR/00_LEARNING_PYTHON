from os import system
from .Deck import Deck
from .Player import Player
from .Player import Dealer

class InputError(Exception):
    pass

class TooMuchMoney(Exception):
    pass

class InsufficientFunds(Exception):
    pass

class BadChoice(Exception):
    pass

class Game:
    def __init__(self):
        self.deck = Deck()
        self.deck.hide_deck()
        self.deck.shuffle_deck()
        self.player = Player()
        self.dealer = Dealer()
        self.round = 0
    
    def __del__(self):
        print('\n\n(: GAME OVER :)\n')

    def start(self):
        end = False
        self.print_start()
        self.clean_screen()
        print('Let\'s start palying!\n')
        while not end:
            self.print_round()
            self.ask_bet()
            self.first_deal()
            if (self.player.hand.score == 21 and not self.dealer.hand.ace_first()):
                amount = self.player.bet * 1.5
                print(f'\nBLACKJACK! You earn {amount}$ !')
                input('Press ENTER to end this round...')
                self.round += 1
                self.end_round(win = True, amount = amount)
                continue
            res = self.play()
            self.print_round()
            if (res == 'lost'):
                self.end_round(win = False)
            elif (res == 'tied'):
                self.end_round(win = True, amount = 0)
            else:
                self.end_round(win = True, amount = self.player.bet)
            if (self.player.money <= 0):
                print('\nSorry, you have lost all your money...')
                print('Please come back later!')
                break
            end = not self.replay()
            self.round += 1
        money_gap = self.player.init_money - self.player.money
        if (money_gap < 0):
            print(f'This time, you earned {abs(money_gap)}$, congratulations!')
        elif (money_gap > 0):
            print(f'This time, you lost {abs(money_gap)}$, sorry about this...!')
        else:
            print(f'You did not win, you did not lose. Like Switzerland during WW2!')

    def replay(self):
        while True:
            try:
                replay = input('\nDo you want to keep playing? (y/n) ')
                if (replay != 'y' and replay != 'n'):
                    raise InputError
            except:
                print('ERROR - Possible answers: y/n')
            else:
                break
        if (replay == 'y'):
            return True
        return False

    def ask_bet(self):
        while True:
            try:
                bet = int(input('\nHow much do you want to bet? '))
                if (bet < 0):
                    raise InputError
                elif (bet > self.player.money):
                    raise InsufficientFunds
            except InsufficientFunds:
                print('ERROR - Looks like you do not have enough money...')
            except:
                print('ERROR - Please enter a correct value...')
            else:
                self.player.make_bet(bet)
                break
        self.clean_screen()
        self.print_round()

    def first_deal(self):
        input('\nPress ENTER when you are ready for dealing...')
        self.dealer.deal(num = 2, hand = self.player.hand, hidden = False, deck = self.deck)
        self.dealer.deal(num = 1, hand = self.dealer.hand, hidden = False, deck = self.deck)
        self.dealer.deal(num = 1, hand = self.dealer.hand, hidden = True, deck = self.deck)
        self.print_round()

    def end_round(self, win, amount = 0):
        if (win):
            self.player.money += self.player.bet + amount
            self.player.bet = 0
            self.dealer.money -= amount
        else:
            self.dealer.money += self.player.bet
            self.player.bet = 0
        self.player.hand.clean()
        self.dealer.hand.clean()

    def print_start(self):
        self.clean_screen()
        print('*******************************')
        print('*    $$$   BLACKJACK   $$$    *')
        print('*******************************')
        input('\nPress ENTER to start the game')
        self.clean_screen()
        while True:
            try:
                player_name = input('Player, what is your name: ')
                if (len(player_name) == 0 or len(player_name) > 12):
                    raise InputError
            except:
                print('ERROR - Invalid name (max 12 char)\n')
            else:
                temp_len = len(player_name) - len('DEALER')
                if (temp_len < 0):
                    for _ in range(abs(temp_len)):
                        player_name += ' '
                else:
                    for _ in range(temp_len):
                        self.dealer.name += ' '
                self.player.name = player_name.upper()
                break
        while True:
            try:
                player_money = int(input(f'{player_name}, how much money do you have for the game? '))
                if (player_money < 0):
                    raise InputError
                elif (player_money > 1000000):
                    raise TooMuchMoney
            except TooMuchMoney:
                print('JESUS! We do not have enough money to play with you...\n')
            except:
                print('ERROR - The amount should be a positive number.\n')
            else:
                self.player.money = player_money
                self.player.init_money = player_money
                break
        self.round = 1

    def print_round(self):
        self.clean_screen()
        print(f'ROUND {self.round}')
        print(' _______________________________________________________________')
        print('|                               |                               |')
        print(f'|  {self.player.name}\t\t\t|  {self.dealer.name}\t\t\t|')
        print('|                               |                               |')
        print('|_______________________________|_______________________________|')
        print('| CARDS:                        | CARDS:                        |')
        if (not self.player.hand):
            print('|   Empty hand\t\t\t|   Empty hand\t\t\t|')
        else:
            len_handplayer = len(self.player.hand.content)
            len_handdealer = len(self.dealer.hand.content)
            max_len = max(len_handplayer, len_handdealer)
            for i in range(max_len):
                card_player = ''
                card_dealer = ''
                if (i < len_handplayer):
                    card_player += str(self.player.hand.content[i])
                else:
                    card_player += '           '
                if (i < len_handdealer):
                    card_dealer += str(self.dealer.hand.content[i])
                else:
                    card_dealer += '           '
                print(f'|   {card_player}\t\t\t|   {card_dealer}\t\t\t|')
        print('|_______________________________|_______________________________|')
        print(f'| SCORE: {self.eval_score(self.player)}\t\t\t| SCORE: {self.eval_score(self.dealer)}\t\t\t|')
        '''
        print('|_______________________________|_______________________________|')
        print('| STATUS:                       | STATUS:                       |')
        if (not self.player.hand):
            print('|   none\t\t\t|   none\t\t\t|')
        '''
        print('|_______________________________|_______________________________|')
        print(f'| BET: {self.player.bet}\t\t\t|')
        print(f'| MONEY: {self.player.money}\t\t\t|')
        print('|_______________________________|')

    def eval_score(self, player):
        if (not player.hand):
            return 0
        score = player.hand.score
        if (score == -1):
            return ('?')
        return (score)

    def play(self):
        stop = False
        while (not stop):
            while True:
                try:
                    print('\nPOSSIBILITIES:')
                    print('\t1 - Hit (ask for one more card)')
                    print('\t2 - Stand (stop asking for more cards)')
                    choice = int(input('What do you want to do? '))
                    if (choice != 1 and choice != 2):
                        raise BadChoice
                except BadChoice:
                    print('Your choice is not available')
                except:
                    print('Your choice should be a numbers')
                else:
                    break
            if (choice == 1):
                self.dealer.deal(1, self.player.hand, False, self.deck)
                self.print_round()
                if (self.player.hand.score > 21):
                    print('\nBUST... You lose, sorry about this!')
                    input('Press ENTER to see dealer\'s hand...')
                    self.dealer.hand.reveal_hand()
                    self.print_round()
                    input('\nPress ENTER to end this round...')
                    return ('lost')
            elif (choice == 2):
                stop = True
        self.print_round()
        input('\nPress ENTER to see dealer\'s hand...')
        self.dealer.hand.reveal_hand()
        self.print_round()
        while (self.dealer.hand.score < 17):
            print('\nThe dealer will take another card...')
            input('Press ENTER to continue...')
            self.dealer.deal(1, self.dealer.hand, False, self.deck)
            self.print_round()
        if (self.dealer.hand.score > 21 or (21 - self.dealer.hand.score > 21 - self.player.hand.score)):
            print(f'\nYou win {self.player.bet}$ !')
            input('Press ENTER to continue...')
            return ('won')
        elif (self.dealer.hand.score == self.player.hand.score):
            print(f'\nGame is tied! No winner, no loser this time!')
            input('Press ENTER to continue...')
            return ('tied')
        else:
            print(f'\nYou lose {self.player.bet}$ !')
            input('Press ENTER to continue...')
            return ('lost')

    def clean_screen(self):
        system('clear')
        '''
        for _ in range(100):
            print('')
        '''
