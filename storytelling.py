import sys
from time import sleep

# Functions for printing the string variables used for storytelling


def intro():
    '''
    Creates a typing effect for the story intro string
    '''

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

    for char in story_intro:
        sleep(0.08)
        sys.stdout.write(char)
        sys.stdout.flush()
    return story_intro
