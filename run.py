# Imports

from pictures import *
from storytelling import *
from cprint import *
import sys
import os
from time import sleep

# Misc functions


def clear_terminal():
    """
    Clears the terminal
    """
    os.system("clear")


def main_menu():
    """
    Displays the Main Menu to the user
    Takes user's input to call the menu functions
    """
    cprint.fatal(welcome)
    cprint.err(game_logo)

    left_option = "1. LET'S PLAY"
    middle_option = "2. HIGH SCORES"
    right_option = "3. EXIT"
    print(f"{left_option : <30}{middle_option : ^30}{right_option : >30}")
    menu_choice = input("Select an option: \n")

    if menu_choice == "1":
        clear_terminal()
        name = input("Please enter your name: \n")
        loading_bar = ["......................", "Your game starts now!"]
        cprint.warn("Loading The Hangman...")
        sleep(1)
        small_text_bits(loading_bar)
        sleep(1.3)
        intro()
    elif menu_choice == "2":
        clear_terminal()
        print("The High Scores to be here")
    elif menu_choice == "3":
        clear_terminal()
        cprint.warn("Are you leaving already?")
        exit_choice = input("Y = YES       N = NO  \n")
        if exit_choice.lower() == "y":
            clear_terminal()
            sleep(1)
            exiting = ["""Exiting in progress...
.........................""", "BYE- BYE ❤ "]
            small_text_bits(exiting)
            exit()
        elif exit_choice.lower() == "y":
            main_menu()
        else:
            cprint.fatal("Please enter a valid option.")
            sleep(1.5)
            main_menu()
    else:
        cprint.fatal("Please enter a valid option.")
        sleep(1.5)
        main_menu()


# Calling the storytelling functions

main_menu()
# meet_the_murderer()
