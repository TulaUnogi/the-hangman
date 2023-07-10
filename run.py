# Imports

from pictures import *
from storytelling import *
import colorama
from colorama import Fore, Style
import sys
import os
from time import sleep


# Initialize colorama
colorama.init(autoreset=True)


# Misc functions


def clear_terminal():
    """
    Clears the terminal
    """
    os.system("clear")


def small_text_bits(list):
    '''
    Displays small blocks of text one at the time
    '''
    for text in list:
        for char in text:
            sleep(0.07)
            sys.stdout.write(char)
            sys.stdout.flush()
    sleep(1)
    clear_terminal()
    return text


def get_username():
    # Gets User input to create the global name variable
    clear_terminal()
    global name
    name = input("Please enter your name: \n")
    clear_terminal()


def append_username(list):
    # Displays the username to dialogues in game
    sleep(1.5)
    for text in list:
        print(f"{Fore.GREEN}{name}:")
        small_text_bits(text)
    return list


def append_murderer(list):
    # Appends the murderer variable to dialogues in game
    sleep(1.5)
    for text in list:
        print(f"{Fore.RED}{murderer}:")
        small_text_bits(text)
    return list


# Storytelling functions

def intro():
    '''
    Prints the story intro with the typing and text delay effects
    '''
    os.system("clear")
    print(name)
    loading_bar = ["******************************************** \n",
                   "Your game starts now!"]
    get_username()
    print(f"{Fore.YELLOW}Loading The Hangman...")
    sleep(1)
    print(small_text_bits(loading_bar), )
    sleep(1.3)
    os.system("clear")
    append_username(story_intro)
    choose_direction()


def choose_direction():
    """
    Takes User input and presents different output
    based on their choice
    """
    print("\n" * 3, f"{Fore.YELLOW}{Style.BRIGHT}Choose the direction:")
    directions = input("""

    1 = TURN LEFT
    2 = TURN BACK
    3 = TURN RIGHT
    4 = GO AHEAD
     \n \n \n
    """)
    clear_terminal()
    if directions.lower() == "4":
        global murderer
        murderer = "*Shadow in the dark*"
        append_username(go_ahead)
        append_murderer(murderer_intro)
        will_you_play()
    elif directions.lower() == "2":
        append_username(turn_left)
        sleep(1.5)
        choose_direction()
    elif directions.lower() == "3":
        append_username(turn_back)
        sleep(1.5)
        choose_direction()
    elif directions.lower() == "4":
        append_username(turn_right)
        sleep(1.5)
        choose_direction()
    else:
        print(f"{Fore.RED}Please type a valid option.")
        choose_direction()
    return directions


def will_you_play():
    """
    Takes the User input to decide whether to terminate the game
    or to play The Hangman with the murderer.
    Prints the dialogues depending on the choice.
    """
    clear_terminal()
    play = input(f"""{Fore.YELLOW}{Style.BRIGHT}
    WILL YOU PLAY THE GAME?{Style.RESET_ALL}
    Y = YES
    N = NO
    """)
    if play.lower() == "y":
        global murderer
        murderer = "Jack Ketch"
        clear_terminal()
        append_username(will_play)
        sleep(1)
        clear_terminal()
        append_murderer(rules)
        print("placeholder for hangman function")
    elif play.lower() == "n":
        clear_terminal()
        append_username(not_playing)
        sleep(1)
        clear_terminal()
        print(f"{Fore.RED}{game_over}")
        sleep(4)
        clear_terminal()
        main_menu()
    else:
        print(f"{Fore.RED}Please enter a valid option.")
        sleep(1)
        clear_terminal()
        will_you_play()

# Game Menu


def main_menu():
    """
    Displays the Main Menu to the user
    Takes user's input to call the menu functions
    """
    print(f"{Fore.YELLOW}{welcome}")
    print(f"{Fore.RED}{game_logo}")

    left_option = "1. LET'S PLAY"
    middle_option = "2. HIGH SCORES"
    right_option = "3. EXIT"
    print(f"{left_option : <30}{middle_option : ^30}{right_option : >30}")
    menu_choice = input("Select an option: \n")

    if menu_choice == "1":
        intro()
    elif menu_choice == "2":
        clear_terminal()
        print("The High Scores to be here")
    elif menu_choice == "4":  # temporarily here to skip dialogues
        clear_terminal()
        will_you_play()
    elif menu_choice == "3":
        clear_terminal()
        print(f"{Fore.YELLOW}{Style.BRIGHT}Are you leaving already?")
        exit_choice = input("Y = YES       N = NO  \n")
        if exit_choice.lower() == "y":
            clear_terminal()
            sleep(1)
            exiting = "Exiting in progress"
            exiting_loading = ["""
************************""", "❤ BYE-BYE ❤ "]
            print(f"{Style.BRIGHT}{exiting}")
            small_text_bits(exiting_loading)
            exit()
        elif exit_choice.lower() == "y":
            main_menu()
        else:
            print(f"{Fore.RED}Please enter a valid option.")
            sleep(1.5)
            main_menu()
    else:
        print(f"{Fore.RED}Please enter a valid option.")
        sleep(1.5)
        main_menu()


# Calling the storytelling functions

main_menu()
