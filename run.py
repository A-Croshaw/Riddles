import random
import gspread
from rich.table import Table
from rich.console import Console
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
score_list = SHEET.worksheet("score")
correct = riddles.col_values(5)
console = Console()
player = ""
percentage = 0
player_score = 0
question = []
nums = []
list_score = []


def diplay_score():

    global list_score
    numx = 1
    score_lists = SHEET.worksheet("score").get_all_values()
    print("*******************************")
    print()
    print("To See Saved Scores")
    print("Type 'Yes'")
    print("Or Press Any Key To Continue")
    print()
    scores = input()
    scores = scores.upper()
    if scores == "YES":
        list_score = score_list.row_values(numx)
        numx += 1
        table = Table(show_header=True, header_style="bold red on black", style="red on black", box=None)
        table.add_column(list_score[0], justify="center", width=16,style="red on black")
        table.add_column(list_score[1], justify="center", width=16,style="red on black")
        table.add_column(list_score[2], justify="center", width=16,style="red on black")
        while numx <= len(score_lists):
            list_score = score_list.row_values(numx)
            table.add_row(list_score[0], list_score[1], list_score[2],)
            numx += 1
        console.print(table)


def player_details():

    global player
    print("Welcome to Riddles.")
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
            print("*******************************")
            print()
            print(f"Riddle Number {riddle_number}")
            print()
            print(question[0])
            print()
            print(f"A: {question[1]} B: {question[2]} C: {question[3]}")
            print() 
            count = 0
            player_guess = ""
            while count == 0:
                player_guess = input("Enter (A, B, C): ")
                player_guess = player_guess.upper()
                print()
                if player_guess == "A":
                    count += 1
                elif player_guess == "B":
                    count += 1
                elif player_guess == "C":
                    count += 1
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
    diplay_score()


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
    print("Type 'Yes'")
    print("Or Press Any Key To Continue")
    print()
    upload = input()
    upload = upload.upper()
    if upload == "YES":
        print("Uploading Score\n")
        score_worksheet = SHEET.worksheet("score")
        score_worksheet.append_row(data)
        print("Successfully added.\n")


def play_again():

    global percentage
    global player_score
    global question
    global nums
    global list_score
    print("*******************************")
    print()
    print("To Play Again")
    print("Type 'Yes'")
    print("Or Press Any Key To Continue")
    print()
    restart = input()
    restart = restart.upper()
    if restart == "YES":
        percentage = 0
        player_score = 0
        question = []
        nums = []
        list_score = []
        return True


def new_game():

    player_details()
    welcome()
    diplay_score()
    play()    
    while play_again():
        play()
    print("*******************************")    
    print()
    print("Thank you for playing")


new_game()
