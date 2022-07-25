
import random
import time


class Game:
    # Game class attributes that will hold values needed for game play, including symbols, bools for win and replay
    # and int score.
    water_symbol = "-"
    ship_symbol = "*"
    guessed_symbol = "x"
    win = False
    score = 0
    bool_replay = False

    # labels for columns and lines, including all dictionary letters so grid size can change on object initialization.
    labels_dict = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9, "K": 10, "L": 11,
                   "M": 12, "N": 13, "O": 14, "P": 15, "Q": 16, "R": 17, "S": 17, "T": 18, "U": 19, "V": 20, "W": 21,
                   "Y": 22, "X": 23, "Z": 24, }

    # Game class constructor that will allow for different grid sizes according to height and width values passed
    def __init__(self, height, width):
        self.height = height
        self.width = width

    # this method will create a grid list with water symbols according to height and width values
    def build_grid(self):
        grid = []
        for item in range(self.height):
            grid.append([self.water_symbol] * self.width)
        return grid

    # this method will generate coordinated to hide the ship symbol within the grid.
    # coordinates will be obtained by using the randrange method from Random module.
    # randrange will select an int in range (0 to height) or (0 to width) last values excluded.
    def hide_ship(self):
        index_column = random.randrange(0, self.height)
        index_line = random.randrange(0, self.width)
        return (index_column, index_line)

    # this method prints the computer and user grids
    def game_display(self, user_grid, computer_grid):
        print("    USER'S grid:" + "                    " + "COMPUTER's grid:")

        # column and line label arrays will be slices of the alphanumeric values. Slices will be generated according
        # to width and height values.
        column_label = '1234567890'[:self.height]
        line_label = 'ABCDEFGHIJKLMNOPQRSTUVXZ'[:self.width]

        # prints spaces joined by values in the column label for both user and computer grids.
        print('    ' + '   '.join(column_label) + '  ' + "                " + '    ' + '   '.join(column_label))

        # loops through values in the range 0 to grid list size.
        for number in range(len(user_grid)):
            # prints spaces joined by line_label letter.
            # In each iteration of this loop the letter will be obtained through its index.
            print(line_label[number] + '   ' + '   '.join(user_grid[number]) + '  ' + "                " + line_label[
                number] + '   ' + '   '.join(computer_grid[number]) + '  ')
        print("\n")

    # this method will her the coordinates for hiding the ship by calling the hide_ship method.
    # It will return a list containing 2 tuples: one for user ship coordinated, one for computer ship coordinates.
    def setup_game(self):
        user_line, user_column = self.hide_ship()
        computer_line, computer_column = self.hide_ship()
        return [(user_line, user_column), (computer_line, computer_column)]

    # this method will loop through all the key, value pairs in the provided dictionary and will return the key
    # according to the value passed when method was called. This is a static method as it's meant to be used only
    # within the Game class and not by its objects.
    @staticmethod
    def get_key(my_dict, val):
        for key, value in my_dict.items():
            if val == value:
                return key

    # this method will replace the water symbol with the ship symbol in the grid through indexes.
    # Ship is considered found when the correct letter+number coordinates are typed in
    # Letter coordinate will be transformed in int index by getting its value pair from the labels_dict.
    def ship_found(self, grid, letter, number):
        line = self.labels_dict[letter]
        column = number
        grid[line][column] = self.ship_symbol

    # this method will replace the water symbol with the guessed symbol in the grid through indexes.
    # Letter coordinate will be transformed in int index by getting its value pair from the labels_dict.
    def ship_missed(self, grid, letter, number):
        line = self.labels_dict[letter]
        column = number
        grid[line][column] = self.guessed_symbol

    # this method validates the user guess by checking if it's within the grid range, if the letter is a key in the
    # labels_dict. It will also check if that guess has already been made by checking if the symbol in the grid is a
    # guessed symbol.
    def user_guess(self, labels, grid, grid_height):
        try:
            line_input = (input("Enter a line letter:")).capitalize()
            column_input = int(input("Enter a column number:")) - 1
            if grid[labels[line_input]][column_input] == "x":
                print("You've already guessed that number.")
                return self.user_guess(labels, grid, grid_height)
            else:
                return line_input, column_input

        except KeyError:
            print("Entry is not valid. Try again...")
            return self.user_guess(labels, grid, grid_height)

        except ValueError:
            print("Entry is not valid. Try again...")
            return self.user_guess(labels, grid, grid_height)

        except IndexError:
            print("Entry is not valid. Try again...")
            return self.user_guess(labels, grid, grid_height)

    # this method returns a random alphabet letter
    @staticmethod
    def random_letter(width):
        line_label = 'ABCDEFGHIJKLMNOPQRSTUVXZ'
        # gets int value in range 0 to width (last value excluded)
        index = random.randrange(0, width)
        # uses random int obtained as index to get a random letter from the line_label string.
        letter = line_label[index]
        return letter

    # gets a guess for the computer.
    def computer_guess(self, grid):
        # will loop until values obtained do not correspond to coordinated with already guesses symbol.
        while True:
            # gets a random letter by calling random_letter method
            line_computer = str(self.random_letter(self.width))

            # gets a random int between 0 and height (last value not included)
            column_computer = random.randrange(0, self.height)

            # check if the obtained coordinates don't already have the guesses symbol in the passed grid.
            if grid[self.labels_dict[line_computer]][column_computer] != "x":
                break
        return line_computer, column_computer

    # this method will be used to start a new game
    def new_game(self):
        #  Initializes turns var
        turns = 1

        # creates 2 grid (user and computer) arrays by calling Game class' build_grid method.
        user_grid = self.build_grid()
        computer_grid = self.build_grid()

        # prints the grid by calling Game class' game_display method.
        self.game_display(user_grid, computer_grid)

        # gets an array with 2 tuples with coordinates for user and computer ships
        # by calling Game class' setup_game method.

        placement_tuples = self.setup_game()

        # all turns loop
        while True:
            # all turns start showing user the turn number
            print("TURN " + str(turns))

            # calls user_guess method to get and validate user's input.
            line_user, column_user = self.user_guess(self.labels_dict, computer_grid, self.height)

            # checks if user guess matches the ship coordinates on computer's grid. horizontal coordinate is obtained
            # by getting the value in the labels_dict that corresponds to the letter user typed. then check is that
            # value matches the first value in the second tuple in the placement_tuples list. the number the used
            # types for the vertical coordinate will then be compared with second value in the second tuple.
            if self.labels_dict[line_user] == placement_tuples[1][0] and column_user == placement_tuples[1][1]:
                # change the value of win attribute to True, as user has won the game.
                self.win = True

                # calculates user score by subtracting the number of turns from 101. It will then change the value of
                # attribute score.
                self.score = 101 - turns

                # prints win message and trophy ascii art.
                print(r""" You win!
                  ___________
                 '._==_==_=_.'
                 .-\:      /-.
                | (|:.     |) |
                 '-|:.     |-'
                   \::.    /
                    '::. .'
                      ) (
                    _.' '._
                   `"""""""`
                   """)

                # prints score obtained by user.
                print("Your score was " + str(self.score))

                # 2 seconds delay so user can read the message on screen.
                time.sleep(2)

                # calls ship_found method to place the ship symbol in both user and computer's grid.
                self.ship_found(computer_grid, line_user, column_user)
                self.ship_found(user_grid, self.get_key(self.labels_dict, placement_tuples[0][0]),
                                placement_tuples[0][1])

                # prints both grids
                self.game_display(user_grid, computer_grid)

                # breaks loop because game is over.
                break

            # if the user doesn't get the correct ship coordinates, enter this conditional.
            else:
                # prints missed message
                print(r""" Water!
                .-.   .-.   .-.   .-.   .-.   .-.   .-.   .-.   .-.
                   '-'   '-'   '-'   '-'   '-'   '-'   '-'   '-'   '-'
                """)

                # 2 seconds delay so user can read the message on screen.
                time.sleep(2)

                # calls ship_missed method to place the missed symbol in computer's grid.
                self.ship_missed(computer_grid, line_user, column_user)

                # prints both grids
                self.game_display(user_grid, computer_grid)

            print("It's the computer's turn now...")

            # gets an automated guess for computer by calling computer_guess method.
            line_computer, column_computer = self.computer_guess(user_grid)

            # prints computer guess (column must be +1 as the indexes start at 0, but label values start at 1)
            print(line_computer, (column_computer + 1))

            # checks if computer guess matches the ship coordinates on user's grid with same login as previously used
            # for user guess.
            if self.labels_dict[line_computer] == placement_tuples[0][0] and column_computer == placement_tuples[0][1]:

                # changes value of attribute win to False, as user lost this match.
                self.win = False

                # prints "lost" message and game over ascii art.
                print(r""" You lost...
    
                  _____                         ____
                 / ____|                       / __ \
                | |  __  __ _ _ __ ___   ___  | |  | |_   _____ _ __
                | | |_ |/ _` | '_ ` _ \ / _ \ | |  | \ \ / / _ \ '__|
                | |__| | (_| | | | | | |  __/ | |__| |\ V /  __/ |
                 \_____|\__,_|_| |_| |_|\___|  \____/  \_/ \___|_|
                 """)

                # 2 seconds delay so user can read the message.
                time.sleep(2)

                # calls ship_found method to place the ship symbol in both user and computer's grid.
                self.ship_found(user_grid, line_computer, column_computer)
                self.ship_found(computer_grid, self.get_key(self.labels_dict, placement_tuples[1][0]),
                                placement_tuples[1][1])

                # prints both grids
                self.game_display(user_grid, computer_grid)

                # breaks the loop as game is over.
                break
            else:
                # prints missed message
                print(r""" Water!
                .-.   .-.   .-.   .-.   .-.   .-.   .-.   .-.   .-.
                   '-'   '-'   '-'   '-'   '-'   '-'   '-'   '-'   '-'
                """)

                # 2 seconds delay so user can read the message.
                time.sleep(2)

                # calls ship_missed method to place the missed symbol in user's grid.
                self.ship_missed(user_grid, line_computer, column_computer)

                # prints both grids
                self.game_display(user_grid, computer_grid)

                # adds 1 to turn number
                turns += 1

    # this method will ask if user wants a new match.
    def replay(self):
        choice = input("Would you like to play another match? y/n")

        # if they reply yes, changes bool_replay value to True and calls new_game method.
        if choice.lower() == "y":
            self.bool_replay = True
            self.new_game()

        # if they reply no, changes bool_replay value to False and prints a message.
        else:
            self.bool_replay = False
            print("Ok. Going back to starting menu." + "\n")

    # win bool getter
    def win_getter(self):
        return self.win

    # score getter
    def score_getter(self):
        return self.score

    # replay bool getter
    def get_replay(self):
        return self.bool_replay
