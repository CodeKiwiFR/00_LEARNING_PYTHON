'''
Blackjack console project
Main file
Started: 20/04/2020 at 23:00
Ended:
'''

from Modules import Game

def main():
    game = Game()
    game.start()
    del game

if __name__ == '__main__':
    main()
