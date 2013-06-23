# Memory, the game, by Virat Singh

# This game is written entirely in Python and utilizes the simplegui module 
# developed by Scott Rixner, professor of Computer Science at Rice University.  
# To most easily launch my Asteroids game, utilize his CodeSkulptor IDE, 
# which implements the simplegui module and can be launched via browser
# (Chrome or Firefox highly recommended. CodeSkulptor will NOT work on 
# Internet Explorer).

# Memory game: http://www.codeskulptor.org/#user16_LVQY2a5ZnH_47.py
# To launch game, press the play button (right-facing triangle) at the
# top left of the CodeSkulptor window.

import simplegui
import random

# globals for user interface
WIDTH = 800
HEIGHT = 100
CARD_WIDTH = 50
CARD_HEIGHT = 100
COLUMNS = 16

# globals for memory deck
deck = range(8) * 2 # this is the main deck
exposed = [False] * 16 # list of boolean values to check if a given card is selected

# helper function to initialize globals
def init():
    global deck, moves, state, index, card1, card2
    global exposed
    for i in range(len(deck)):
        exposed[i] = False
    
    state = 0 # variable to manage the game state/logic
    index = 0 # represents index of selected card
    card1 = 0 # variable to store index of first selected card
    card2 = 0 # index of second selected card
    moves = 0 # counter for number of moves
    random.shuffle(deck) # shuffle the deck!
     
# define event handlers
def mouseclick(pos):
    global state, index
    global card1, card2
    global moves
    
    index = pos[0] // 50
    
    # select the first card
    if state == 0:
        if exposed[index] == False:
            exposed[index] = True
            card1 = index
            state = 1
            moves += 1
        else:
            exposed[index] = True
            state = 1
    # select the second card
    elif state == 1:
        if exposed[index] == False:
            exposed[index] = True
            state = 2
            card2 = index
            
        elif exposed[index] == False:
            exposed[index] = True
            state = 2
    # once both cards have been selected, check if 
    # they are the same value
    elif state == 2:
        if deck[card1] == deck[card2]:
            exposed[card1] = True
            exposed[card2] = True
            state = 0
        else:
            exposed[card1] = False
            exposed[card2] = False
            state = 0
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global deck
    global exposed
    global visible
    
    number_pos = [0, 80] # evenly space out the cards
    # loop through the deck of cards, start with 
    # the first card at index 0
    for num in range(len(deck)):
        # if card has not been selected, show green back
        if not exposed[num]:
            first_point = (num * CARD_WIDTH, 0)
            second_point = ((num * CARD_WIDTH) + CARD_WIDTH, 0)
            third_point = ((num * CARD_WIDTH) + CARD_WIDTH, CARD_HEIGHT)
            fourth_point = (num * CARD_WIDTH, CARD_HEIGHT)
            canvas.draw_polygon([(first_point),
                                 (second_point),
                                 (third_point),
                                 (fourth_point)], 1, "Red", "Green")
        # if card has been selected, show its face    
        else:
            canvas.draw_text(str(deck[num]), number_pos, 85, "White", "sans-serif")
        number_pos[0] += 50    
        
    #update the counter for the number of moves
    label.set_text("Moves = " + str(moves))        

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", WIDTH, HEIGHT)
frame.add_button("Restart", init)
label = frame.add_label("")

# initialize global variables
init()

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
frame.start()
