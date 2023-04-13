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
player = []

def player_details():
    print("Please Type Your Name")
    player_name = input()
    player.append(player_name)

def welcome():
    print(f"Welcome to Riddles {player}.")
    print()
    print("How to Play")
    print("-----------------------------------------------------")
    print("* There are 50 riddles to be answered")
    print("* Each riddle has 3 options A, B or C to choose from")
    print("* Each riddle will give you 1 point. Can you get 50!!")
    print("-----------------------------------------------------")
    print("Good Luck")

def play():
    riddle_number = 1
    player_score = 0
    option_one = riddles.col_values(2)
    option_two = riddles.col_values(3)
    option_three = riddles.col_values(4)
    while riddle_number <= 50:
        for riddle in riddles.col_values(1):
            options = f"A: {option_one[riddle_number-1]} B: {option_two[riddle_number-1]} C: {option_three[riddle_number-1]}"    
            print("*******************************")
            print(f"Riddle Number {riddle_number}")
            print(riddle)
            print()
            print(options)
            print() 
            d = 0
            player_guess = ""
            while d== 0:
                player_guess = input("Enter (A, B, C): ")
                player_guess = player_guess.upper()
                if player_guess == "A":
                    d += 1
                elif player_guess == "B":
                    d += 1
                elif player_guess == "C":
                    d += 1
                else:
                    print("*******************************")
                    print("Incorrect Value!!")
                    print()       
            
            print()

            player_score += answer_check(correct[riddle_number-1], player_guess)
            print(f"Your Current Score Is {player_score}")
            riddle_number += 1
        
    final_score(player_score)

def answer_check(correct_answer, player_guess):

    if correct_answer == player_guess:
        print("You Answered Correct!")
        print()
        return 1
    else:
        print("Sorry Wrong Answer!")
        print()
        return 0

def final_score(player_score):
    print("*******************************")
    print("Your Final Result")
    print()
    final_score = int((player_score/len(correct))*100)
    print(f"You Answered: {player_score} Riddles Corretly with "+str(final_score)+"% Accuracy")
    print()
    if player_score == 50:
        print(f"CONGRATULATIONS {player} YOU ARE A RIDDLE MASTER")

def play_again():

    print("*******************************")
    print("Would you like to play again?")
    print("(type Yes or NO!)")
    print()
    x = 0
    while x == 0:
        restart = input()
        restart = restart.upper()
        if restart == "YES":
            x += 1
            return True
        elif restart == "NO":
            x += 1
            return False
        else:
            print("*******************************")
            print("Incorrect Value!!")
            print("(type Yes or NO!)")
            print()
            
def new_game():

    player_details()
    welcome()
    play()
    while play_again():
        play()
    print("*******************************")    
    print("Thank you for playing")

new_game()
