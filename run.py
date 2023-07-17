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
from tabulate import tabulate


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

SCORES_SHEET = SHEET.worksheet("scores")
ALL_SCORES = SCORES_SHEET.get_all_values()

# Game variables

SECRET_WORD = ""
HIDDEN_WORD = ""
SCORE = 0
SCORE1 = 0
SCORE2 = 0
USER_CHANCES = 7
GUESSED_LETTERS = []
WRONG_GUESSES = []
DEFINITION = ""
GAME_ROUND = 1
SCORES_DATA = [NAME, SCORE]

# Misc functions

def new_game():
    """
    Resets variables to get ready for new round
    """
    global SCORE, USER_CHANCES, GUESSED_LETTERS, WRONG_GUESSES, DEFINITION
    SCORE = 0 
    set_secret_word()
    USER_CHANCES = 7
    GUESSED_LETTERS = []
    WRONG_GUESSES = []
    DEFINITION = ""
    

def reset_all_values():
    # Resets all the values 
    global NAME, MURDERER, SCORE1, SCORE2, GAME_ROUND
    new_game()
    SCORE1 = 0
    SCORE2 = 0
    GAME_ROUND = 1
    NAME = ""
    MURDERER = "*Shadow in the dark*"
    


def clear_terminal():
    """
    Clears the terminal
    """
    os.system("clear")


def small_text_bits(list):
    '''
    Displays small blocks of text one at the time
    From stackoverflow.com/questions/20302331/typing-effect-in-python
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
    global NAME
    clear_terminal()
    print(f"{Fore.RED}{GAME_LOGO}")
    print("\n" * 3)
    NAME = input(f"{Fore.GREEN}Please enter your name:{Style.RESET_ALL} \n \n")
    clear_terminal()


def append_username(list):
    # Displays the username to dialogues in game
    sleep(1.5)
    for text in list:
        print(f"{Fore.GREEN}{FOREST}")
        print("\n" * 4)
        print(f"{Fore.GREEN}{NAME}:")
        small_text_bits(text)
    return list


def append_murderer(list):
    # Appends the murderer variable to dialogues in game
    sleep(1.5)
    for text in list:
        print(f"{Fore.RED}{MURDERER_FACE}")
        print("\n" * 4)
        print(f"{Fore.RED}{MURDERER}:")
        small_text_bits(text)
    return list

def choose_mode():
    """
    Takes User input to allow a choice between a story mode and 
    a plain Hangman game.
    """
    clear_terminal()
    print(f"{Fore.RED}{GAME_LOGO}")
    print("\n" * 3, f"{Fore.GREEN}{Style.BRIGHT}CHOOSE ONE OF THE OPTIONS:\n")
    print(f"""\n{Fore.RED}1. Story mode:{Style.RESET_ALL} 
    (If you play the game for the first time OR just enjoy the story time)""")
    print(f"""{Fore.RED}2. Plain Hangman:{Style.RESET_ALL}
    (If you wish to skip directly to the game part)""")
    print("\n" * 2)
    mode_choice = input(f"""{Fore.YELLOW}Please type only 1 OR 2:\n
    {Style.RESET_ALL} """)
    if mode_choice == "1":
        intro()
    elif mode_choice == "2":
        get_username()
        main_hangman_game()
    else:
        print(f"{Fore.RED}CHOOSE EITHER 1 OR 2!")
        sleep(1.5)
        clear_terminal()
        choose_mode()


# Storytelling functions

def intro():
    '''
    Prints the story intro with the typing and text delay effects
    '''
    clear_terminal()
    loading_bar = ["******************************************** \n",
                   "\nYour game starts now!"]
    get_username()
    print(f"{Fore.RED}{GAME_LOGO}")
    print("\n"*3)
    print(f"{Fore.YELLOW}Loading The Hangman...\n \n")
    sleep(1)
    print(small_text_bits(loading_bar), )
    sleep(1.3)
    clear_terminal()
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
    SCORE = math.ceil((len(GUESSED_LETTERS) *
                      1034 - len(WRONG_GUESSES * 25)) + (USER_CHANCES) * 5)
    total_score = SCORE + SCORE1 + SCORE2
    print(f"{Fore.RED}{GAME_LOGO}\n\n")
    print(f"{Fore.YELLOW}{Style.BRIGHT}Here are your results: ", "\n" * 2)
    print(f"{Fore.GREEN}Guessed letters: {len(GUESSED_LETTERS)}")
    print(f"{Fore.GREEN}Wrong guesses: {len(WRONG_GUESSES)}")
    print(f"{Fore.GREEN}Chances left: {USER_CHANCES}", "\n" * 2)
    print(f"{Fore.GREEN}{Style.BRIGHT}TOTAL SCORE: {total_score}")


def update_score_sheet():
    # Updates the score sheet
    global SCORES_SHEET
    clear_terminal()
    print(f"{Fore.RED}{GAME_LOGO}")
    print("\n" *3)
    small_text_bits(["Updating the SCORE BOARD", "................."])    
    SCORES_SHEET.append_row(SCORES_DATA)
    print(f"{Fore.GREEN}SCORE BOARD updated!")



def score_table():
    """
    Draws the high scores table and prints the
    5 highest scores
    """
    clear_terminal()
    print(f"{Fore.YELLOW}{HIGH_SCORE_FONT}")
    """
    Sorts the scores. From:
    stackoverflow.com/questions/30076145/how-to-sort-list-of-lists-by-highest-number
    """
    sorted_scores = sorted(ALL_SCORES, key=lambda x: int(x[1]), reverse=True)
    head_rank = "RANK"
    head_name = "NAME"
    head_scores = "SCORES"
    rank = [1, 2, 3, 4, 5]
    table_data = sorted_scores[:5]
    headings = [head_name, head_scores]
    print("\n" * 3)
    # From: statology.org/create-table-in-python/
    print(tabulate(table_data, headers=headings, tablefmt="fancy_grid"))
    print()
    back_to_main = input(f"{Fore.GREEN}To return to Main Menu press B: \n")
    if back_to_main.lower() == "b":
        clear_terminal()
        __main__()
    else:
        print(f"{Fore.RED}Wrong input.Please press B.")
        sleep(1.5)
        clear_terminal
        score_table()
   

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
        DEFINITION = f"{Fore.RED}This is a tricky word! GOOD LUCK! Khee, khee, khee!"


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
    print("\n" * 2)
    print(f"{Style.BRIGHT}HIDDEN WORD:{Style.RESET_ALL} {HIDDEN_WORD}")
    print(f"\n{Style.BRIGHT}HINT:{Style.RESET_ALL} {DEFINITION}")
    print(f"\n{Fore.RED}Incorrect letters: {Style.RESET_ALL}{WRONG_GUESSES}")
    print(f"{Fore.GREEN}Guessed letters: {Style.RESET_ALL}{GUESSED_LETTERS}")
    print(f"\n{Style.BRIGHT}You have {USER_CHANCES} chances left.")
    print(f"\n{Style.DIM}If you guessed all the letters")
    print(f"{Style.DIM}please press any new letter to continue!")


def lost_game():
    """
    Prints the lost game ending, displays calculated scores and 
    returns to Main Menu.
    Resets all values.
    """
    global SCORE1, SCORE2, GAME_ROUND
    clear_terminal()
    print(f"{Fore.GREEN}{HANGMAN[7]}")
    print(f"The hidden word was: {Fore.YELLOW}{SECRET_WORD}.\n")
    print(f"\n{Fore.RED}Now... Goodnight, sweet angel!")
    sleep(3)
    clear_terminal()
    print("\n" * 5)
    print(f"\n{Fore.RED}{GAME_OVER}")
    sleep(2)
    score_calculation()
    update_score_sheet()
    sleep(10)
    clear_terminal()
    reset_all_values()
    __main__()

def won_game():
    clear_terminal()
    print("\n" * 5)
    print(f"\n{Fore.GREEN}{CONGRATS}")
    sleep(2)
    score_calculation()
    sleep(10)
    clear_terminal()

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


def offer_play_again():
    """
    Takes user input to decide on playing another round
    Changes the rounds number if playing again
    """
    global GAME_ROUND
    clear_terminal()
    print(f"{Fore.RED}{GAME_LOGO}")
    print("\n" * 3)
    play_again = input(f"""{Fore.YELLOW}{Style.BRIGHT}PLAY AGAIN? Y / N
    {Style.RESET_ALL} \n""")
    if play_again == "Y".lower():
        GAME_ROUND = GAME_ROUND + 1
        handle_more_rounds()
    elif play_again == "N".lower():
        clear_terminal()
        print(f"{Fore.GREEN}FOREST", "\n")
        print(f"""{Fore.YELLOW}You have managed to escape the murderer
        and come back to your friends!""")
        print("\n" * 3)
        print(f"{Fore.GREEN}You're safe now! Congrats!")
        print("\n" * 3)
        update_score_sheet()
        sleep(6)
        reset_all_values()
        __main__()
    else:
        print(f"{Fore.RED}Please enter valid option.")
        sleep(2)
        clear_terminal()
        offer_play_again()


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
        print("\n" * 2)
        user_guess = input(f"{Fore.YELLOW}Enter a letter:{Style.RESET_ALL} \n")
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
        elif "_" not in HIDDEN_WORD:
            while GAME_ROUND < 3:
                clear_terminal()
                won_game()
                offer_play_again()
            clear_terminal()
            won_game()
            __main__()
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
    lost_game()

def handle_more_rounds():
    """
    Prints the Murderer's message
    Resets the game variables
    Assigns the scores to the new variables
    """
    global SCORE, SCORE1, SCORE2
    while GAME_ROUND <= 3:
        if GAME_ROUND == 2:
            clear_terminal()
            append_murderer(GAME_2)
            sleep(2)
            clear_terminal()
            set_secret_word()
            SCORE1 = SCORE # Passes 1st score to new variable
            # Resets the values for a new game
            new_game()
            main_hangman_game()
        elif GAME_ROUND == 3:
            clear_terminal()
            append_murderer(GAME_3)
            sleep(2)
            clear_terminal()
            set_secret_word()
            SCORE2 = SCORE
            new_game()
            main_hangman_game()
    won_game()
    update_score_sheet()
    __main__()


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
        choose_mode()
    elif menu_choice == "2":
        clear_terminal()
        score_table()
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

def __main__():
    set_secret_word()
    main_menu()

__main__()