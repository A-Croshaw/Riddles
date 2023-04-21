import random
import gspread
from google.oauth2.service_account import Credentials
from rich.table import Table
from rich import box
from rich.console import Console

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]
CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("Riddles")
riddles = SHEET.worksheet("riddles")
score_list = SHEET.worksheet("score")
correct = riddles.col_values(5)

"""Variables for styling the console out puts """
correct_style = "spring_green3 on grey0"
incorrect_style = "blink red on grey0"
lines_style = "bold bright_red on grey0"
info_style = "bright_yellow on grey0"
riddle_style = "white on grey0"
option_style = "wheat1 on grey0"
console = Console()

"""Global variables to hold game data"""
player = ""
percentage = 0
player_score = 0
question = []
nums = []
list_score = []


def player_details():
    """
    Welcomes the user and asks for there name
    saves the name to the player_name variable
    """
    global player
    console.print(
        "\n Welcome to Riddles.\n ",
        style=info_style, justify="center")
    console.print(
        "-------------------------------------"
        "------------------------------------ \n ",
        style=lines_style,
        justify="center",
    )
    console.print(
        "Please Type Your Name \n ",
        style=info_style, justify="center")
    console.print(
        "Or Press Enter To Continue \n",
        style=info_style, justify="center"
    )
    player_name = input()
    player = player_name
    welcome()


def welcome():
    """
    Displays information to the user about the game.
    """
    console.print(
        " \n ----------------------------------"
        "--------------------------------------- \n ",
        style=lines_style,
        justify="center",
    )
    console.print(f"Hello {player}!!  \n ", style=info_style, justify="center")
    console.print("How To Play  \n ", style=info_style, justify="center")
    console.print(
        "---------------------------------------"
        "---------------------------------- \n ",
        style=lines_style,
        justify="center",
    )
    console.print(
        "* There are 20 riddles to be answered \n ",
        style=info_style, justify="center"
    )
    console.print(
        "* Each riddle has 3 options A, B or C to choose from  \n ",
        style=info_style,
        justify="center",
    )
    console.print(
        "* Each riddle will give you 1 point \n ",
        style=info_style, justify="center"
    )
    console.print(
        "* Will not be able to save score if no player name given "
        "\n game will need to be re-started to enter \n ",
        style=info_style, justify="center"
    )

    console.print(
        "---------------------------------"
        "---------------------------------------- \n ",
        style=lines_style,
        justify="center",
    )
    console.print(
        "Press Enter To Continue \n ",
        style=info_style, justify="center"
    )
    input()


def diplay_score():
    """
    Prompts the user to see score that have been saved.
    Imports the data from google sheets
    Displays the content within a table styled by RICH
    """

    global list_score
    numx = 1
    score_lists = SHEET.worksheet("score").get_all_values()
    console.print(
        " \n -------------------------------"
        "------------------------------------------ \n ",
        style=lines_style,
        justify="center",
    )
    console.print(
        "To See Saved Scores \n ",
        style=info_style, justify="center")
    console.print(
        "Type 'Yes' \n ",
        style=info_style, justify="center")
    console.print(
        "Or Press Enter To Continue \n ", style=info_style, justify="center"
    )
    scores = input()
    scores = scores.upper()
    if scores == "YES":
        console.print(
            " \n -------------------------------"
            "------------------------------------------ \n ",
            style=lines_style,
            justify="center",
        )
        list_score = score_list.row_values(numx)
        numx += 1
        table = Table(
            title="Scores \n",
            title_justify="center",
            title_style="yellow on grey0",
            show_header=True,
            header_style="blue3 on grey0",
            style="red on grey0",
            box=box.ASCII,
            expand=True,
        )
        table.add_column(
            list_score[0], justify="center",
            width=16, style="spring_green3 on grey0"
        )
        table.add_column(
            list_score[1], justify="center",
            width=16, style="spring_green3 on grey0"
        )
        table.add_column(
            list_score[2],
            justify="center",
            width=16,
            style="spring_green3 on grey0",
        )
        while numx <= len(score_lists):
            list_score = score_list.row_values(numx)
            table.add_row(
                list_score[0],
                list_score[1],
                list_score[2] + " %",
            )
            numx += 1
        console.print(table)
        console.print(
            " \n Press Enter To Continue \n ",
            style=info_style, justify="center"
        )
        input()


def play():
    """
    Displays the riddles imported from google sheets:
    Randomly selects 20 riddles from the imported riddles.
    Promts the user to make a choice from a selction of answers.
    Checks the users imputted choice againts the correct answers stored in
    google sheets and displays the correct output
    before looping back to next riddle
    After all 20 riddles answered will check user score with the final_score
    function.
    Then calls upload_score fuction
    Finally calls display_score functionlast
    """
    riddle_number = 1
    global question
    global player_score
    console.print(
        " \n -------------------------------"
        "------------------------------------------ \n ",
        style=lines_style,
        justify="center",
    )
    console.print(
        "Good Luck",
        style=info_style, justify="center")
    while riddle_number <= 20:
        num = random.randint(1, 50)
        if num not in nums:
            nums.append(num)
            question = riddles.row_values(num)
            console.print(
                " \n ---------------------------------"
                "---------------------------------------- \n ",
                style=lines_style,
                justify="center",
            )
            console.print(
                f"Riddle Number {riddle_number} \n ",
                style=info_style, justify="center"
            )
            console.print(
                f"{question[0]} \n",
                style=riddle_style, justify="center")
            console.print(
                f"A: {question[1]}   "
                f"   B: {question[2]}  "
                f"  C: {question[3]}  \n ",
                style=option_style,
                justify="center",
            )
            count = 0
            player_guess = ""
            while count == 0:
                console.print(
                    "Enter (A, B, C): \n",
                    style=info_style, justify="center")
                player_guess = input()
                player_guess = player_guess.upper()
                if player_guess == "A":
                    count += 1
                elif player_guess == "B":
                    count += 1
                elif player_guess == "C":
                    count += 1
                else:
                    console.print(
                        "\n -----------------------------------"
                        "-------------------------------------- \n ",
                        style=lines_style,
                        justify="center",
                    )
                    console.print(
                        "Incorrect Value!! :warning:  \n ",
                        style=incorrect_style,
                        justify="center",
                    )
                    console.print(
                        "Type A, B, or C  \n ",
                        style=incorrect_style, justify="center"
                    )
            player_score += answer_check(question[4], player_guess)
            console.print(
                f"Your Current Score Is {player_score}  ",
                style=info_style,
                justify="center",
            )
            riddle_number += 1

    final_score(player_score)
    if player != "":
        upload_score()
    diplay_score()


def answer_check(correct_answer, player_guess):
    """
    Checks the users answers imputted with
    the correct answers imported from google sheets.
    Displays correct output depending on the answer given.
    """
    console.print(
        " \n-------------------------------"
        "------------------------------------------ \n ",
        style=lines_style,
        justify="center",
    )
    if correct_answer == player_guess:
        console.print(
            "You Answered Correct!  \n ",
            style=correct_style, justify="center"
        )
        return 1
    else:
        console.print(
            "Sorry Wrong Answer!  \n ",
            style=incorrect_style, justify="center"
        )
        return 0


def final_score(players_score):
    """
    Displays users final score and produces a percentage
    If user scores max points displays congratulations message aswell
    """
    global percentage
    console.print(
        "\n-------------------------------"
        "------------------------------------------ \n ",
        style=lines_style,
        justify="center",
    )
    console.print("Your Final Result  \n ", style=info_style, justify="center")
    percentage = int((players_score / len(correct)) * 250)
    console.print(
        f"You Answered: {player_score} Riddles Corretly With "
        + str(percentage)
        + "% Accuracy  \n ",
        style=correct_style,
        justify="center",
    )
    if player_score == 20:
        console.print(
            f"CONGRATULATIONS {player} YOU ARE A RIDDLE MASTER  \n ",
            style=correct_style,
            justify="center",
        )


def upload_score():
    """
    Promts user with question to save score.
    if yes then will up date the score worksheet with a new row.
    with messages displyed when staterd and successful.
    """
    data = [player, player_score, percentage]
    console.print(
        " \n -------------------------------"
        "------------------------------------------ \n ",
        style=lines_style,
        justify="center",
    )
    console.print(
        "To Save Your Score  \n ",
        style=info_style, justify="center")
    console.print("Type 'Yes'  \n ", style=info_style, justify="center")
    console.print(
        "Or Press Enter To Continue  \n ", style=info_style, justify="center"
    )
    upload = input()
    upload = upload.upper()
    if upload == "YES":
        console.print(
            " \n -------------------------------"
            "------------------------------------------ \n ",
            style=lines_style,
            justify="center",
        )
        console.print("Uploading Score \n", style=info_style, justify="center")
        score_worksheet = SHEET.worksheet("score")
        score_worksheet.append_row(data)
        console.print(
            "Successfully Added.",
            style=info_style, justify="center")


def play_again():
    """
    Promts the user asking to play again.
    if yes returns true value.
    if no returns a false value.
    if new game started it restests
    global variables back to empty state.
    """
    global percentage
    global player_score
    global question
    global nums
    global list_score
    console.print(
        " \n-----------------------------------"
        "-------------------------------------- \n ",
        style=lines_style,
        justify="center",
    )
    console.print("To Play Again  \n ", style=info_style, justify="center")
    console.print("Type 'Yes'  \n ", style=info_style, justify="center")
    console.print(
        "Or Press Enter To Continue \n ", style=info_style, justify="center"
    )
    restart = input()
    restart = restart.upper()
    if restart == "YES":
        welcome()
        percentage = 0
        player_score = 0
        question = []
        nums = []
        list_score = []
        return True


def new_game():
    """
    Main function called
    has thank message to show the end of the game
    """
    player_details()
    diplay_score()
    play()
    while play_again():
        play()
    console.print(
        " \n -------------------------------"
        "------------------------------------------ \n ",
        style=lines_style,
        justify="center",
    )
    console.print(
        "Thank You For Playing \n  ", style=info_style, justify="center")


new_game()
