
from Database import Database


# authentication class inherits from Database class
class Authentication(Database):

    def __init__(self, db_name):
        super().__init__(db_name)

    # this method will print menu options with a number in from of them.
    def menu(self, *options):
        print("Select an option:")
        # enumerate method is used to get counter that will be displayed together with unpacked values from *options
        # parameter. Counter will start at 0.
        for (count, item) in enumerate(options, 0):
            print(count, ".", item)

    # this method will allow new users to input information and add those to the database
    def signup(self):
        name = input("Enter a username:")
        # calls unique_name method to validate user input.
        if self.unique_name("users", "username", name):

            # prompts user for password
            password = input("Enter a password:")

            # calls add user method with inputed information as parameters.
            self.add_user(name, password)

            # success message
            print(name + " has been added.")

        else:
            # recursion if username is already in the database.
            print("This username is already being used. Try again...")
            self.signup()

    # this method will allow new users to input information and add those to the database
    def login(self, table, name):

        # calls get_user method with username passed as parameter. Will get as the info on that user's line on the
        # table. if user is not on database, the method will return False and this bool value will be stored as user
        user = self.get_user(table, "username", name)

        # if user's value is False, ask if user wants to sign up.
        if not user:
            print("Looks like you haven't signed up yet.")
            choice = input("Would you like to sign up now? y/n")

            # if user wants to sign up, call signup method.
            if choice.lower() == "y":
                self.signup()
            else:
                print("Ok. Going back to starting menu.")

        # if the first value in the user array (which is the username stored in the database) equals the name passed
        # as parameter, means typed username is correct.
        elif user[0] == name:
            # ask for password.
            password = input("Enter your password:")

            # error checking to ensure user inputed an int.
            try:
                password = int(password)
            except ValueError:
                pass
            # if that matches the second value in the user array, print welcome back message with wins value and
            # highest score value stored on the database.
            if user[1] == password:
                print("Welcome back " + name + "!")
                print("You've won this game " + str(user[2]) + " times. Your current score is " + str(user[3]) + ".")

            # if values don't match, method will call itself again.
            else:
                print("Your password is incorrect. Try again...")
                self.login(table, name)
