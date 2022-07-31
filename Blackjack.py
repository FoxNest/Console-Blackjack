'''
Dylan Fox 10-28-21

To play a hand of Blackjack the following steps must be followed:

    []Create a deck of 52 cards
    []Shuffle the deck
    []Ask the Player for their bet
    []Make sure that the Player's bet does not exceed their available chips
    []Deal two cards to the Dealer and two cards to the Player
    []Show only one of the Dealer's cards, the other remains hidden
    []Show both of the Player's cards
    []Ask the Player if they wish to Hit, and take another card
    []If the Player's hand doesn't Bust (go over 21), ask if they'd like to Hit again.
    []If a Player Stands, play the Dealer's hand. The dealer will always Hit until the Dealer's value meets or exceeds 17
    []Determine the winner and adjust the Player's chips accordingly
    []Ask the Player if they'd like to play again
    
COPY PASTA:
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}
         
ASCII CARD ART: https://www.asciiart.eu/miscellaneous/playing-cards
'''

import random # used to shuffle deck
import os     # used to clear console screen on Windows


# Global playing variable
playing = True # controls when it's the players turn

# Global Card Variables
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}
         
# CLASS DECLARATIONS
class Card: # cards
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return f'{self.rank} of {self.suit}'

class Deck: # builds and manages deck - deal() shuffle()
    
    def __init__(self):
    
        self.deck = []
        
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))
    
    def __str__(self):
        deck_print = ''
        
        for card in self.deck:
            deck_print += '\n'+card.__str__()
        return deck_print
    
    # shuffles deck
    def shuffle(self):
        return random.shuffle(self.deck)
    
    # deals card
    def deal(self):
        return self.deck.pop()

class Hand: # keeps track of card in play (hand)
    
    def __init__(self):
        self.cards = [] # cards in hand
        self.value = 0  # keeps track up current hand value
        self.aces = 0   # keeps track of number of aces
    
    # iterates through cards and prints 
    def __str__(self):
        cards_in_hand = '\nHand contains: '
        
        for card in self.cards:
            cards_in_hand += '\n'+card.__str__()
        return cards_in_hand
    
    # adds card to hand and tracks value & aces
    def add_card(self, deck): 
        new_card = deck.deal()          # gets new card  
        self.cards.append(new_card)     # adds card to hand
        self.value += values[new_card.rank] # adds card value 
        if new_card.rank == 'Ace':
            self.aces += 1
    
    # changes ace from 11 to 1 if hand value > 21
    def adjust_for_ace(self): 
        if self.value > 21 and self.aces >= 1:
            self.value -= 10
            self.aces -= 1
        
class Chips: # handles player chips and bet
    
    def __init__(self):
        self.chips = 100
        self.bet = 0
    
    def __str__(self):
        return f'Total chips: {self.chips} \nCurrent bet: {self.bet}'
    
    def win_bet(self):
        self.chips += self.bet
    
    def lose_bet(self):
        self.chips -= self.bet
        
# GAME PLAY METHODS
def show_some(player, dealer, chips): # shows cards on table with 1 dealer card hidden
    os.system('cls') # clears screen on windows
    print('\nDealers Hand:')
    print(' <Card Facedown>')
    print(' ',dealer.cards[1])
    print('\nPlayers Hand:', *player.cards, sep='\n ')
    print('\nHand value: {}    Current chips: {}    Current bet: {}'.format(player.value, chips.chips, chips.bet))

def show_all(player, dealer, chips): # shows all cards on table
    os.system('cls') # clears screen on windows
    print('\nDealers Hand:', *dealer.cards, sep='\n ')
    print('\nPlayers Hand:', *player.cards, sep='\n ')
    print('\nHand value: {}    Current chips: {}    Current bet: {}'.format(player.value, chips.chips, chips.bet))

def take_bet(chips): # takes and stores bet
    while True:
        try:
            bet = int(input('How much would you like to bet? '))
        except:
            print('\nYou can only bet a whole number.')
        else:
            if bet > chips.chips or bet <= 0:
                print('You cannot bet 0 or more than your total chips: ', chips.chips)
            else:
                chips.bet = bet
                break

def hit(hand, deck): # processes a 'hit'
    hand.add_card(deck)
    hand.adjust_for_ace()
    return hand

def hit_or_stand(player_hand, dealer_hand, chips, deck, playing): # prompts use to hit/stand
    stand = False
    while stand == False:
        choice = input("\nWould you like to hit 'h' or stand 's'? ").lower()
        if choice == 'h':
            hit(player_hand, deck)
            show_some(player_hand, dealer_hand, chips)
            if player_hand.value > 21: # watches for bust
                stand = True
        elif choice == 's':
            playing = False 
            stand = True
        else:
            print("Enter a valid option.")    

def player_bust(chips):
    print('\nPlayer Bust!\n')
    chips.lose_bet()

def dealer_bust(chips):
    print('\nDealer Bust!\n')
    chips.win_bet()

def player_win(chips):
    print('\nPlayer Wins!\n')
    chips.win_bet()

def dealer_win(chips):
    print('\nDealer Wins!\n')
    chips.lose_bet()

def push(): # AKA tie/draw
    print('\nPUSH!\nNo win or loss!')

def check_blackjack(hand, chips): # checks for player drawn blackjack (Ace + Face = win_bet*1.5)
    # seperates two player cards
    card_one = hand.cards[0]
    card_two = hand.cards[1]
    
    # checks for a combination of a Face card & an Ace (blackjack)
    if card_one.rank == 'Ace' and (card_two.rank == 'Jack' or card_two.rank == 'Queen' or card_two.rank == 'King'):
        print('\nBLACKJACK 1.5x bet!')
        chips.chips += chips.bet * 1.5       
        if chips.bet%2 != 0: # gives player addition .5 chip if type is float
            chips.chips += .5
        return True
        
    elif card_two.rank == 'Ace' and (card_one.rank == 'Jack' or card_one.rank == 'Queen' or card_one.rank == 'King'):
        print('\nBLACKJACK 1.5x bet!')
        chips.chips += chips.bet * 1.5 # adds win for blackjack    
        if chips.bet%2 != 0: # gives player addition .5 chip if type is float
            chips.chips += .5            
        return True
        
    else:
        return False        
        
def game_logic(): # controls main game logic        
    print('Welcome to my BlackJack game! Your goal is to get as close to 21 without going over. The dealer will keep hitting until they are over 17\n You start with 100 chips ($100). Pulling a Face card and an Ace results in BLACKJACK and you will win 1.5x your bet! Enjoy!\n')
    input('Press any enter to play!\n\n')
    
    playing = True 
    
    # creates chips
    chips = Chips()
    
    while True:
        while playing:
            blackjack = False # initialize & resets blackjack bool var at new hand
            
            # creates deck and shuffles
            deck = Deck()
            deck.shuffle()

            # creates player hand and deals cards
            player_hand = Hand()
            player_hand.add_card(deck)
            player_hand.add_card(deck)
            
            # creates dealer hand and deals cards
            dealer_hand = Hand()
            dealer_hand.add_card(deck)
            dealer_hand.add_card(deck)
        
            take_bet(chips)
            show_some(player_hand, dealer_hand, chips)
            
            # checks for blackjack on intial draw and goes to hit/stand phase
            if not check_blackjack(player_hand, chips):
                hit_or_stand(player_hand, dealer_hand, chips, deck, playing)
            else:
                blackjack = True
                
            playing = False
        
        # dealer turn
        while playing == False:
            while dealer_hand.value <= 17 or dealer_hand.aces >= 1: # dealer hits while hand < 17 or has 1+ aces
                hit(dealer_hand, deck)
            
            # tests win conditions after dealer hits
            while blackjack == False:
                show_all(player_hand, dealer_hand, chips) 
                if player_hand.value > 21:
                    player_bust(chips)
                    break
                elif dealer_hand.value > 21:
                    dealer_bust(chips)
                    break
                elif dealer_hand.value > player_hand.value:
                    dealer_win(chips)
                    break
                elif dealer_hand.value < player_hand.value:
                    player_win(chips) 
                    break                       
                elif dealer_hand.value == player_hand.value:
                    push()
                    break
            
            # checks to make sure you have chips to bet
            print(f'\nCurrent chip total: {chips.chips}')
            if chips.chips == 0:
                print('\nYou have no more chips to bet!')
                input('\nPress any key to exit!')
                exit()
            
            # controls 'play again' loop
            while True:
                x = input("\nWould you like to play another hand? 'y' or 'n' ").lower()
                if x == 'y':
                    playing = True
                    # deletes current objects to get ready for next hand
                    del player_hand
                    del dealer_hand
                    del deck
                    break
                elif x == 'n':
                    exit()
                else:
                    print('Enter a valid option.\n')

game_logic()