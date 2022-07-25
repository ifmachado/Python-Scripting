
# imports all attributes and methods from Game, Database and Authentication classes
from Game import *
from Database import *
from Authentication import *

# new Game class object with 4 as the values for height and width.
game = Game(4, 4)

# new Database class object that will create a new database called "users".
db = Database("users")

# new Authentication class object to allow login and signup.
auth = Authentication("users")

# creates a table inside users database called "users".
table_name = "users"
db.add_table(table_name, "(username TEXT UNIQUE, password INT, wins INT, highscore INT)")

while True:
    print("BATTLESHIP GAME" + "\n")

    # called Database class method menu to create and print this game's menu
    auth.menu("Leave game", "Signup", "Login")

    # prompts user to select a menu option.
    choice = input()

    # error checking to ensure user inputed an int.
    try:
        choice = int(choice)

    except ValueError:
        pass

    # if user's choice is 0 (Leave game), close the database and quit the program.
    if choice == 0:
        print("Leaving system...")
        db.close_database()
        exit(0)

    # if user's choice is 1 (Signup), call Authentication class method signup.
    elif choice == 1:
        auth.signup()

    # if user's choice is 2 (Login), let user login
    elif choice == 2:

        # get username
        name = input("Enter your username:")

        # authenticate user by calling Authentication class login method.
        auth.login(table_name, name)

        # ask if user wants to start a new game
        choice = input("Would you like to start a new game now? y/n" + "\n")

        # if yes, start a new game.
        if choice.lower() == "y":
            game.new_game()
            while True:

                # get all info in database about authenticated user.
                user = db.get_user(table_name, "username", name)

                # wins is the third element in the returned values from database.
                previous_win = user[2]

                # score is the fourth element in the returned values from database.
                previous_score = user[3]

                # use class getter to get bool value from Game class' win attribute
                bool_win = game.win_getter()

                # use class getter to get int value from Game class' score attribute
                score = game.score_getter()

                # if user won the game ( bool_win = True)
                if bool_win:

                    # add 1 to previous win value
                    new_win = previous_win + 1

                    # update database with new win value
                    db.update_user(table_name, "wins", "username", new_win, name)

                    # check if new score is bigger than the one currently on the database.
                    if score > previous_score:

                        # if yes, update database with new score value.
                        new_score = score
                        db.update_user(table_name, "highscore", "username", new_score, name)

                # call Game class replay method.
                game.replay()

                # use class getter to get bool value from Game class' bool_replay attribute, which will be False,
                # if user chose to stop the game.
                replay = game.get_replay()

                # if replay == False, break the loop to go back to menu.
                if not replay:
                    break

        # return to menu, if user doesn't want to play a new match.
        elif choice.lower() == "n":
            print("Going back to menu..." + "\n")

        # if user enters anything other than "y" or "n" return to menu.
        else:
            print("Invalid option. Try again...")

    # if user enter a number outside the menu range, return to menu.
    else:
        print("Invalid option. Try again...")
