# Blackjack, the game, by Virat Singh

# This game is written entirely in Python and utilizes the simplegui module 
# developed by Scott Rixner, professor of Computer Science at Rice University.  
# To most easily launch my Asteroids game, utilize his CodeSkulptor IDE, 
# which implements the simplegui module and can be launched via browser
# (Chrome or Firefox highly recommended. CodeSkulptor will NOT work on 
# Internet Explorer).

# Blackjack game: http://www.codeskulptor.org/#user16_kjRQMfpYLy_127.py
# To launch game, press the play button (right-facing triangle) at the
# top left of the CodeSkulptor window.

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
card_spacing = 50

deck = None

player_hand_value = 0
dealer_hand_value = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.hand = []
        
    def __str__(self):
        # return a string representation of a hand
        hand_string = ""
        for i in range(len(self.hand)):
            hand_string += str(self.hand[i]) + " "
        return "Hand contains %s" % hand_string
            
    def add_card(self, card):
        # add a card object to a hand
        self.hand.append(card)    

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        hand_value = 0
        num_of_aces = 0
        
        # traverse through Hand object
        # and sum the values of its cards
        for value in self.hand:
            hand_value += VALUES[Card.get_rank(value)]
   
        # loop through Hand and check if there are
        # any aces in it.  If there are aces,
        # increment the num_of_aces variable by 1
        for card in self.hand:
          if card.get_rank() == 'A':
                num_of_aces += 1
        
        # if the hand has no aces, return hand value
        # else if there are aces, add 10 to the hand
        # value as long as adding 10 doesn't make the 
        # hand bust
        if num_of_aces == 0:
            return hand_value
        else:
            if hand_value + 10 <= 21:
                return hand_value + 10
            else:
                return hand_value
            
    # helper method that returns true if the hand has 
    # busted
    def busted(self):
        if self.get_value() > 21:
            return True
        else:
            return False
            
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
 
        for card in self.hand:
            card.draw(canvas, pos)
            pos[0] += 20
# define deck class 
class Deck:
    def __init__(self):
        self.reset_deck()
              
    def reset_deck(self):
        self.deck = []
        
        for i in SUITS: # traverse through SUITS list
            for j in RANKS: # traverse through RANKS list
                self.deck.append(Card(i, j)) # add Card object to list

    def shuffle(self):
        # use random.shuffle() to shuffle the deck
        self.reset_deck() # add cards back to deck and shuffle
        
        random.shuffle(self.deck)

    def deal_card(self):
        # deal a card object from the deck

        return self.deck.pop()
    
    def __str__(self):
        # return a string representing the deck 
        deck_string = ""
        
        for i in range(len(self.deck)):
            deck_string += str(self.deck[i]) + " "
        return "Deck contains %s" % str(deck_string)

#define event handlers for buttons
def deal():
    global outcome, in_play
    global deck, player_hand, dealer_hand
    
    deck = Deck()
    deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()
    
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())

    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    
    in_play = True

def hit():
    global player_hand
    global in_play, outcome, score
    # if the hand is in play, hit the player
    # if busted, assign a message to outcome, 
    # update in_play and score
    
    if in_play == True:
        player_hand.add_card(deck.deal_card())
        if player_hand.busted() == True:
            outcome = "You have busted."
            in_play = False
            score -= 1
       
def stand():
    global dealer_hand, player_hand
    global outcome, score, in_play
    # if hand is in play, repeatedly hit 
    # dealer until his hand has value 17 or more
    if in_play == True:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
        if dealer_hand.busted() == True:
            outcome = "You win!"
            in_play = False
            score += 1     
        else:
            if dealer_hand.get_value() >= player_hand.get_value():
                outcome = "You lose."
                in_play = False
                score -= 1
            else:
                outcome = "You win!"
                in_play = False
                score += 1
        # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global player_hand, dealer_hand
    global outcome, score
    
    player_hand.draw(canvas, [250, 400])
    canvas.draw_text("BLACKJACK", [25, 75], 36, "Blue", "sans-serif")
    canvas.draw_text("Score: " + str(score), [25,575], 30, "Black", "sans-serif")
    
    if in_play == True:
        canvas.draw_text("Hit or Stand?", [200, 300], 30, "Blue", "sans-serif")
        canvas.draw_text("Dealer", [250, 75], 30, "Black", "sans-serif")
        canvas.draw_text("Player", [250, 550], 30, "Black", "sans-serif")
        
        dealer_hand.draw(canvas, [250, 100])
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [305, 150], CARD_SIZE)
    else:    
        canvas.draw_text(outcome + " New deal?", [200, 300], 30, "Black", "sans-serif")        
        dealer_hand.draw(canvas, [250, 100])
        
        # card = Card("S", "A")
    # card.draw(canvas, [300, 300])


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
frame.start()
player_hand = Hand()
dealer_hand = Hand()

# remember to review the gradic rubric        
