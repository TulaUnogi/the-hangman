# Imports

from pictures import *
from storytelling import *
import colorama
from colorama import Fore, Style
import sys
import os
from time import sleep
import requests
import gspread
from google.oauth2.service_account import Credentials
import math
from PyDictionary import PyDictionary


# Initialize colorama
colorama.init(autoreset=True)

# Credentials and other gspread variables

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("the_hangman_scores")

SCORES = SHEET.worksheet("scores")
ALL_SCORES = SCORES.get_all_values()

# Game variables

SECRET_WORD = ""
HIDDEN_WORD = ""
SCORE = None
USER_CHANCES = 7
GUESSED_LETTERS = []
WRONG_GUESSES = []
DEFINITION = ""

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
    global NAME
    NAME = input("Please enter your name: \n")
    clear_terminal()


def append_username(list):
    # Displays the username to dialogues in game
    sleep(1.5)
    for text in list:
        print(f"{Fore.GREEN}{FOREST}")
        print(f"{Fore.GREEN}{NAME}:")
        small_text_bits(text)
    return list


def append_murderer(list):
    # Appends the murderer variable to dialogues in game
    sleep(1.5)
    for text in list:
        print(f"{Fore.RED}{MURDERER_FACE}")
        print(f"{Fore.RED}{MURDERER}:")
        small_text_bits(text)
    return list


# Storytelling functions

def intro():
    '''
    Prints the story intro with the typing and text delay effects
    '''
    os.system("clear")
    loading_bar = ["******************************************** \n",
                   "Your game starts now!"]
    get_username()
    print(f"{Fore.RED}{GAME_LOGO}")
    print("\n"*3)
    print(f"{Fore.YELLOW}Loading The Hangman...")
    sleep(1)
    print(small_text_bits(loading_bar), )
    sleep(1.3)
    os.system("clear")
    append_username(STORY_INTRO)
    choose_direction()


def choose_direction():
    """
    Takes User input and presents different output
    based on their choice
    """
    print(f"{Fore.RED}{GAME_LOGO}")
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
        global MURDERER
        MURDERER = "*Shadow in the dark*"
        append_username(GO_AHEAD)
        append_murderer(MURDERER_INTRO)
        will_you_play()
    elif directions.lower() == "1":
        append_username(TURN_LEFT)
        sleep(1.5)
        choose_direction()
    elif directions.lower() == "2":
        append_username(TURN_BACK)
        sleep(1.5)
        choose_direction()
    elif directions.lower() == "3":
        append_username(TURN_RIGHT)
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
    print(f"{Fore.RED}{GAME_LOGO}")
    print("\n" * 3)
    play = input(f"""{Fore.YELLOW}{Style.BRIGHT}
    WILL YOU PLAY THE GAME?{Style.RESET_ALL}
    Y = YES
    N = NO
    """)
    if play.lower() == "y":
        global MURDERER
        MURDERER = "Jack Ketch"
        clear_terminal()
        append_username(WILL_PLAY)
        sleep(1)
        clear_terminal()
        append_murderer(RULES)
        main_hangman_game()
    elif play.lower() == "n":
        clear_terminal()
        append_username(NOT_PLAYING)
        sleep(1)
        clear_terminal()
        print(f"{Fore.RED}{GAME_OVER}")
        sleep(4)
        clear_terminal()
        main_menu()
    else:
        print(f"{Fore.RED}Please enter a valid option.")
        sleep(1)
        clear_terminal()
        will_you_play()


# High Scores

def score_calculation():
    # Calculates scores and prints User's results
    global SCORE
    SCORE = math.ceil(len(GUESSED_LETTERS) *
                      1034 - len(WRONG_GUESSES * 25) / (USER_CHANCES + 1) * 10)
    print(f"{Fore.YELLOW}{Style.BRIGHT}Here are your results: ", "\n" * 2)
    print(f"{Fore.GREEN}Guessed letters: {len(GUESSED_LETTERS)}")
    print(f"{Fore.GREEN}Wrong guesses: {len(WRONG_GUESSES)}")
    print(f"{Fore.GREEN}Chances left: {USER_CHANCES}", "\n" * 2)
    print(f"{Fore.GREEN}{Style.BRIGHT}TOTAL SCORE: {SCORE}")


# The Hangman Game functions

def set_secret_word():
    """
    Requests a random word from external API and
    displays it as a string of underscores.
    """
    global SECRET_WORD, HIDDEN_WORD, DEFINITION
    api_url = "https://random-word-api.herokuapp.com/word?length=5"
    response = requests.get(api_url)
    secret_word_list = response.json()  # Displays a list including random word
    SECRET_WORD = secret_word_list[0]
    HIDDEN_WORD = "_" * len(SECRET_WORD)
    dictionary = PyDictionary()
    DEFINITION = dictionary.meaning(SECRET_WORD)
    if DEFINITION == None:
        DEFINITION = f"{Fore.RED}This is a tricky word! GOOD LUCK, {NAME}! Khee, khee, khee!"


def display_hangman():
    # Displays the hangman picture based on wrong guesses
    clear_terminal()
    if USER_CHANCES == 7:
        print(f"{Fore.GREEN}{HANGMAN[0]}")
    elif len(WRONG_GUESSES) == 1:
        print(f"{Fore.GREEN}{HANGMAN[1]}")
    elif len(WRONG_GUESSES) == 2:
        print(f"{Fore.GREEN}{HANGMAN[2]}")
    elif len(WRONG_GUESSES) == 3:
        print(f"{Fore.GREEN}{HANGMAN[3]}")
    elif len(WRONG_GUESSES) == 4:
        print(f"{Fore.GREEN}{HANGMAN[4]}")
    elif len(WRONG_GUESSES) == 5:
        print(f"{Fore.GREEN}{HANGMAN[5]}")
    elif len(WRONG_GUESSES) == 6:
        print(f"{Fore.GREEN}{HANGMAN[6]}")
    elif len(WRONG_GUESSES) == 7:
        print(f"{Fore.GREEN}{HANGMAN[7]}")  
    else:
        print(f"{Fore.RED}Oops! Something went wrong. Exiting.")
        exit()
        

def display_core_game():
    """
    Displays hidden word, hint, guessed and wrong letters 
    and chances left.
    """
    print(f"{Style.BRIGHT}HIDDEN WORD:{Style.RESET_ALL} {HIDDEN_WORD}")
    print(f"\n{Style.BRIGHT}HINT:{Style.RESET_ALL} {DEFINITION}")
    print(f"{Fore.RED}Incorrect letters: {Style.RESET_ALL}{WRONG_GUESSES}")
    print(f"{Fore.GREEN}Guessed letters: {Style.RESET_ALL}{GUESSED_LETTERS}")
    print(f"{Style.BRIGHT}You have {USER_CHANCES} chances left.")


def end_game():
    """
    Prints the lost game ending, displays calculated scores and 
    returns to Main Menu.
    """
    clear_terminal()
    print(f"{Fore.GREEN}{HANGMAN[7]}")
    print(f"The hidden word was: {Fore.YELLOW}{SECRET_WORD}.\n")
    print(f"\n{Fore.RED}Now... Goodnight, sweet angel!")
    sleep(3)
    clear_terminal()
    print(f"{Fore.RED}{GAME_LOGO}")
    print(f"\n{Fore.RED}{GAME_OVER}")
    sleep(1)
    score_calculation()
    sleep(6)
    clear_terminal()
    main_menu()


def display_guessed_letters(user_guess):
    """
    Updates the hidden word with guessed letters.
    Function created with help of my Mentor- thank you!
    """
    global HIDDEN_WORD, SECRET_WORD
    hidden_word_list = list(HIDDEN_WORD)
    user_guess_list = list(map(lambda x: x.upper(), user_guess))
    for index, char in enumerate(SECRET_WORD):
        if char.upper() in user_guess_list:
            hidden_word_list[index] = SECRET_WORD[index]
    HIDDEN_WORD = "".join(hidden_word_list)


def main_hangman_game():
    """
    While the user didn't run out of chances:
    - get the users input to guess the letter
    - check if the letter is in the secret word
    - display a word hint
    - display a number of chances left
    - display a guessed letters
    - update the wrong guesses list
    - display the hangman's tree picture
    """
    global GUESSED_LETTERS, WRONG_GUESSES, USER_CHANCES
    while USER_CHANCES > 0:
        display_hangman()
        display_core_game()
        user_guess = input(f"\n{Fore.YELLOW}Enter a letter: \n")
        user_guess = user_guess.upper()
        if user_guess in SECRET_WORD.upper():
            if user_guess in GUESSED_LETTERS:
                print(f"{Fore.RED}You already guessed that letter!")
                sleep(0.7)
                continue 
            else:
                GUESSED_LETTERS.append(user_guess)
                display_guessed_letters(user_guess)
                sleep(0.7)
                continue 
        elif user_guess == SECRET_WORD.upper():
            clear_terminal()
            print(f"{Fore.GREEN}{CONGRATS}")
            score_calculation()
        else:
            if user_guess in WRONG_GUESSES:
                print(f"{Fore.RED}You already guessed that letter!")
                sleep(1)
                continue 
            else:
                print(f"{Fore.RED}Nice try, but a wrong guess!")
                WRONG_GUESSES.append(user_guess)
                USER_CHANCES = USER_CHANCES - 1
                sleep(1.5)
                continue             
    end_game()


# Game Menu

def display_logo():
    # Displays logo 
    print(f"{Fore.YELLOW}{WELCOME}")
    print(f"{Fore.RED}{GAME_LOGO}")


def display_menu_options():
    # Displays the Main Menu options to the user
    left_option = f"{Style.BRIGHT}{Fore.GREEN}1. LET'S PLAY"
    middle_option = f"{Style.BRIGHT}{Fore.GREEN}2. HIGH SCORES"
    right_option = f"{Style.BRIGHT}{Fore.GREEN}3. EXIT"
    print(f"\n{left_option : <25}{middle_option : ^25}{right_option : >25}\n")


def exiting_sequence():
    # Prints the exiting sequence.
 
    clear_terminal()
    sleep(1)
    exiting = f"{Fore.YELLOW}{Style.BRIGHT}Exiting in progress:\n"
    exiting_loading = ["************************\n", "\n❤  BYE-BYE ❤ "]
    print(f"{Fore.RED}{GAME_LOGO}")
    print(exiting)
    small_text_bits(exiting_loading)
    exit()


def main_menu():
    """
    Displays main game menu.
    Takes user's input to call the menu functions.
    """
    display_logo()
    display_menu_options()
    menu_choice = input(f"{Style.BRIGHT}Select an option: \n")
    if menu_choice == "1":
        intro()
    elif menu_choice == "2":
        clear_terminal()
        print("The High Scores to be here")
    elif menu_choice == "3":
        clear_terminal()
        display_logo()
        print(f"{Fore.YELLOW}{Style.BRIGHT}\nAre you leaving already?")
        exit_choice = input("\n\nY = YES       N = NO\n\n")
        if exit_choice.lower() == "y":
            exiting_sequence()
        elif exit_choice.lower() == "n":
            main_menu()
    elif menu_choice == "4":
        clear_terminal()
        set_secret_word()
    else:
        print(f"{Fore.RED}Please enter a valid option.")
        sleep(1.5)
        main_menu()


# Calling the storytelling functions

set_secret_word()
main_menu()
