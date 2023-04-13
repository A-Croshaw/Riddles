import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Riddles')
riddles = SHEET.worksheet("riddles")
correct = riddles.col_values(5)

def new_game():
    player_guesses = []
    riddle_number = 0
    player_score = 0
    answer = riddles.col_values(2)
    answer_two = riddles.col_values(3)
    for riddle in riddles.col_values(1):
        A = answer[riddle_number]
        B = answer_two[riddle_number]
        print("*******************************")
        print(riddle)
        print()
        print("A: ", A,"  ", "B: ", B)
        print()        
        player_guess = input("Enter (A, B): ")
        print()
        player_guess = player_guess.upper()
        player_guesses.append(player_guess)
        riddle_number += 1
        player_score += answer_check(correct[riddle_number], player_guess)
        print(player_score)

def answer_check(correct_answer, player_guess):

    if correct_answer == player_guess:
        print("You Answered Correct!")
        return 1
    else:
        print("Sorry Wrong Answer!")
        return 0

def score():
    pass

def store_score():
    pass

def play_again():
    pass

new_game()

store_score()
