import gspread
import random
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
player = ""
percentage = 0
player_score = 0
question = []
nums = []

def player_details():

    global player
    print(f"Welcome to Riddles.")
    print()
    print("*******************************")
    print()
    print("Please Type Your Name")
    player_name = input()
    print()
    player = player_name

def welcome():

    print("*******************************")
    print()
    print(f"Hello {player}!!")
    print()
    print("How to Play")
    print("-----------------------------------------------------")
    print("* There are 20 riddles to be answered")
    print("* Each riddle has 3 options A, B or C to choose from")
    print("* Each riddle will give you 1 point")
    print("-----------------------------------------------------")
    print()
    print("Good Luck")
    print()

def play():

    riddle_number = 1
    global question
    global player_score
    while riddle_number <= 20:
        num = random.randint(1, 50)
        if num not in nums:
            nums.append(num)
            question = riddles.row_values(num)
            print(nums)
            print("*******************************")
            print()
            print(f"Riddle Number {riddle_number}")
            print()
            print(question[0])
            print()
            print(f"A: {question[1]} B: {question[2]} C: {question[3]}")
            print() 
            d = 0
            player_guess = ""
            while d== 0:
                player_guess = input("Enter (A, B, C): ")
                player_guess = player_guess.upper()
                print()
                if player_guess == "A":
                    d += 1
                elif player_guess == "B":
                    d += 1
                elif player_guess == "C":
                    d += 1
                else:
                    print("*******************************")
                    print()
                    print("Incorrect Value!!")
                    print()       
            print()
            player_score += answer_check(question[4], player_guess)
            print(f"Your Current Score Is {player_score}")
            print()
            riddle_number += 1
        
    final_score(player_score)
    upload_score()    

def answer_check(correct_answer, player_guess):

    global question
    if correct_answer == player_guess:
        print("You Answered Correct!")
        print()
        return 1
    else:
        print("Sorry Wrong Answer!")
        print()
        return 0

def final_score(player_score):

    global percentage
    print("*******************************")
    print()
    print("Your Final Result")
    print()
    percentage = int((player_score/len(correct))*250)
    print(f"You Answered: {player_score} Riddles Corretly with "+str(percentage)+"% Accuracy")
    print()
    if player_score == 50:
        print(f"CONGRATULATIONS {player} YOU ARE A RIDDLE MASTER")
    
def upload_score():

    data = [player, player_score, percentage]
    print("*******************************")
    print()
    print("To Save Your Score")
    print("Type 'Yes' or 'No'")
    print()
    l = 0
    while l == 0:
        upload = input()
        upload = upload.upper()
        if upload == "YES":
            print("Uploading Score\n")
            score_worksheet = SHEET.worksheet("score")
            score_worksheet.append_row(data)
            print("Successfully added.\n")
            l += 1
        elif upload == "NO":
            l += 1
        else:
            print("*******************************")
            print()
            print("Incorrect Value!!")
            print("Type 'Yes' or 'NO'")
            print()

def play_again():

    print("*******************************")
    print()
    print("Would you like to play again?")
    print("Type 'Yes' or 'NO'")
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
            print()
            print("Incorrect Value!!")
            print("Type 'Yes' or 'NO'")
            print()

def new_game():
    latest_scores()
    player_details()
    welcome()
    play()    
    while play_again():
        play()
    print("*******************************")    
    print()
    print("Thank you for playing")

new_game()
