import sys
from time import sleep


# Here to be functions for creating a typing and text delay

def typing_effect(text):
    '''
    Creates a typing effect for the story intro string
    '''
    for char in text:
        sleep(0.08)
        sys.stdout.write(char)
        sys.stdout.flush()
    return text


def text_delay_effect(self):
    '''
    Delays printing the blocks of text
    '''
    # loop through objects here and then:
    sleep(1.5)


# Functions for printing the string variables used for storytelling

def intro():
    '''
    Prints the story intro with the typing and text delay effects
    '''

    # need to turn it into objects:
    story_intro = '''
    "Uh, it's very dark tonight in the forest...
    Hold on...
    Where actually am I?"
    ---
    *PHONE CHECK*
    ---
    "There's no network coverage here...
    Perfect.
    Just PERFECT.
    Ehhh, I should've downloaded the maps offline beforehand.
    How did I even get in here?
    Ah... Right...
    There was a camping party with guys...
    ...With a... bonfire...?
    Somehow I'm struggling to remember.
    Weird.
    Anyway...
    I most likely went for a little tinkle and got lost in the woods.
    Now I'm cold and surrounded by trees. Great.
    Let's find my way back.
    I better leave an [X] mark on the ground.
    It would be better to know, that I was already here... Just in case.
    Now, which direction should I go?"
    '''
    typing_effect(story_intro)
    return story_intro
