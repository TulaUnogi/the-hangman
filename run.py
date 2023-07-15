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

scores = SHEET.worksheet("scores")
all_scores = scores.get_all_values()

# Game variables (letters added temporarily for testing)

secret_word = ""
hidden_word = ""
score = None
user_chances = 7
guessed_letters = []
wrong_guesses = []

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
    elif directions.lower() == "1":
        append_username(turn_left)
        sleep(1.5)
        choose_direction()
    elif directions.lower() == "2":
        append_username(turn_back)
        sleep(1.5)
        choose_direction()
    elif directions.lower() == "3":
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
        set_secret_word()
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


# High Scores

def score_calculation():
    # Calculates scores and prints User's results
    global score
    score = math.ceil(len(guessed_letters) *
                      1034 - len(wrong_guesses * 25) / (user_chances + 1) * 10)
    print(f"{Fore.YELLOW}{Style.BRIGHT}Here are your results: ", "\n" * 2)
    print(f"{Fore.GREEN}Guessed letters: {len(guessed_letters)}")
    print(f"{Fore.GREEN}Wrong guesses: {len(wrong_guesses)}")
    print(f"{Fore.GREEN}Chances left: {user_chances}", "\n" * 2)
    print(f"{Fore.GREEN}{Style.BRIGHT}TOTAL SCORE: {score}")
    return score


# The Hangman Game functions

def set_secret_word():
    """
    Requests a random word from external API and
    displays it as a string of underscores.
    """
    global secret_word, hidden_word
    api_url = 'https://random-word-api.herokuapp.com/word?length=5'
    response = requests.get(api_url)
    secret_word_list = response.json()  # Displays a list including random word
    secret_word = secret_word_list[0]
    hidden_word = "_" * len(secret_word)
    return secret_word


def display_hangman():
    # Displays the hangman picture based on wrong guesses
    clear_terminal()
    if user_chances == 7:
        print(f"{Fore.GREEN}{hangman[0]}")
    elif len(wrong_guesses) == 1:
        print(f"{Fore.GREEN}{hangman[1]}")
    elif len(wrong_guesses) == 2:
        print(f"{Fore.GREEN}{hangman[2]}")
    elif len(wrong_guesses) == 3:
        print(f"{Fore.GREEN}{hangman[3]}")
    elif len(wrong_guesses) == 4:
        print(f"{Fore.GREEN}{hangman[4]}")
    elif len(wrong_guesses) == 5:
        print(f"{Fore.GREEN}{hangman[5]}")
    elif len(wrong_guesses) == 6:
        print(f"{Fore.GREEN}{hangman[6]}")
    elif len(wrong_guesses) == 7:
        print(f"{Fore.GREEN}{hangman[7]}")  
    else:
        print(f"{Fore.RED}Oops! Something went wrong. Exiting.")
        exit()
        

# In progress!!

def main_hangman_game():
    """
    While the user didn't run out of chances:
    - get the users input to guess the letter
    - check if the letter is in the secret word
    - display a number of chances left
    - display a guessed letters
    - update the wrong guesses list
    - call the function to display the hangman's tree picture
    """
    global guessed_letters, wrong_guesses, user_chances
    while user_chances > 0:
        display_hangman()
        print(secret_word)
        print(hidden_word)
        print(f"You have {user_chances} chances left.")
        print(f"{Style.BRIGHT}Incorrect letters: {wrong_guesses}")
        print(f"{Style.BRIGHT}Guessed letters: {guessed_letters}")
        user_guess = input(f"{Fore.GREEN}Enter a letter \n")
        user_guess = user_guess.upper()
        if user_guess in secret_word.upper():
            if user_guess in guessed_letters:
                print(f"{Fore.RED}You already guessed that letter!")
                sleep(0.7)
                main_hangman_game()
            else:
                guessed_letters.append(user_guess)
                sleep(0.7)
                main_hangman_game()
        elif user_guess == secret_word.upper():
            clear_terminal()
            print(print(f"{Fore.GREEN}{congrats}"))
            score_calculation()
        else:
            if user_guess in wrong_guesses:
                print(f"{Fore.RED}You already guessed that letter!")
                sleep(1)
                main_hangman_game()
            else:
                print(f"{Fore.RED}Nice try, but a wrong guess!")
                wrong_guesses.append(user_guess)
                user_chances = user_chances - 1
                sleep(1.5)
                main_hangman_game()                
    end_game()


def end_game():
    clear_terminal()
    print(f"{Fore.GREEN}{hangman[7]}")
    sleep(3)
    clear_terminal()
    print(f"{Fore.RED}{game_over}")
    sleep(3)
    score_calculation()
    sleep(4)
    clear_terminal()
    main_menu()


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
            exiting_loading = ["************************", "❤ BYE-BYE ❤"]
            print(f"{Style.BRIGHT}{exiting}")
            small_text_bits(exiting_loading)
            exit()
        elif exit_choice.lower() == "n":
            main_menu()
    elif menu_choice == "4":  # temporarily here to skip dialogues
        clear_terminal()
        set_secret_word()
    else:
        print(f"{Fore.RED}Please enter a valid option.")
        sleep(1.5)
        main_menu()


# Calling the storytelling functions

set_secret_word()
main_hangman_game()
