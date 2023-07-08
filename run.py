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

# Storytelling functions


def intro():
    '''
    Prints the story intro with the typing and text delay effects
    '''
    os.system("clear")
    name = input("Please enter your name: \n")
    loading_bar = ["******************************************** \n",
                   "Your game starts now!"]
    print(f"{Fore.YELLOW}Loading The Hangman...")
    sleep(1)
    print(small_text_bits(loading_bar), )
    sleep(1.3)
    os.system("clear")

    def append_username(list):
        # Displays the username in intro
        for text in list:
            print(f"{Fore.GREEN}{name}:")
            small_text_bits(text)
        return list
    append_username(story_intro)


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
