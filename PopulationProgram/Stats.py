
# import TownDatabase class
from TownDatabase import TownDatabase

# new TownDatabase class object that will create a new database called "Statistics".
db = TownDatabase("Statistics.db")

# creates a table inside Statistics database called "population" with name and amount as columns
table_name = "population"
db.add_table(table_name, "(name VARCHAR(128) UNIQUE, amount INT)")


# this method will print menu options
def menu():
    print('''
    Enter 1 to upload file
    Enter 2 to print county populations
    Enter 3 to get the total sum of the population
    Enter 4 to download file sorted by name
    Enter 5 to download file sorted by highest value
    Press 0 to exit
 ''')


# this method will read a towns file and output values (if unique) to population table.
def upload():
    # new array to hold all lines read from file
    lines = []

    # open towns.text in read mode and store in variable called t.
    with open('towns.txt', "r") as t:
        # loop through all the lines in file
        for line in t:
            # split string after comma (separate town name from amount value)
            # rstrip() is also used to split space at end of string and get rid of new line(\n)
            new_line = line.rstrip('\n').split(',')

            # add formatted line to lines array
            lines.append(new_line)

    # loop values from 1 to lines array size (last num excluded).
    # Nums will be used as index values.
    # index 0 is excluded because it's the file header
    for i in range(1, (len(lines))):

        # first value in array is county name
        name = lines[i][0]

        # second value in array is population amount
        amount = int(lines[i][1])

        # check if county name has already been added to table using Class method unique_name
        # if name doesn't exit, method will return True.
        if db.unique_name("population", "name", name):

            # add new entry
            db.add_entry(name, amount)

            # print success message
            print(name + " was successfully uploaded.")

        # if county name already exists
        else:

            # get population value already in table for that city
            population = db.get_entry("population", "name", name)

            # check if the population value from file is not already in the table
            if amount != population[1]:
                # update table with new population value
                db.update_entry("population", "amount", "name", amount, name)

                # print success message
                print(name + " was successfully updated.")

    print("successfully uploaded")


# this method will print all values on the table
def printValues():
    # gets all values from population table.
    # this method will return an array if not empty and False if table is empty.
    county = db.get_all("population")

    # if returned value was False, print error message
    if not county:
        print("NO VALUES FOUND , UPLOAD FILE")

    # if not empty
    else:
        # print header
        print("County : Size")
        print("______________")

        # loop values from 0 to county array size (last value excluded).
        # Nums will be used as index values.
        for i in range(len(county)):
            # first value in tuple is county name
            name = county[i][0]

            # second value is population amount
            amount = county[i][1]

            # print values according to format "County : Size"
            print(name + " : " + str(amount))


# this method sums all the population amounts from the table
def getTotal():
    # gets all values from population table.
    # this method will return an array if not empty and false if table is empty.
    county = db.get_all("population")

    # if returned value was false, print error message
    if not county:
        print("NO VALUES FOUND , UPLOAD FILE")

    # if not empty
    else:
        # total population starting at 0
        total = 0

        # loop values from 0 to county array size (last excluded).
        # Nums will be used as index values.
        for i in range(len(county)):
            # second value in tuple is population amount. store in amount var.
            amount = county[i][1]

            # sum that value to total population
            total += amount

        # return final result of total population sum
        return total


# this gets all values from the table sorted according to specific column selection
# and direction (ASC, DESC).
# It also saves the new orders values to a file.
def sort(selection, direction, file_name):
    # gets all values (sorted) from population table.
    # this method will return an array if not empty and false if table is empty.
    order_county = db.get_all_sorted("population", selection, direction)

    # if returned value was false, print error message
    if not order_county:
        print("NO VALUES FOUND , UPLOAD FILE")

    # if not empty
    else:
        # open file passed as parameter in write mode (overwrite is desired in this case)
        # and store in variable called f.
        # if this file doesn't exist, it will create one
        with open(file_name, "w") as f:

            # write header to file
            f.write("Name,Population\n")

            # loop values from 0 to order_county array size (last value excluded).
            # Nums will be used as index values.
            for i in range(len(order_county)):
                # format values returned in "Name,Population\n" format.
                # first value in tuple is name and second is population amount.
                line = order_county[i][0] + "," + str(order_county[i][1]) + "\n"

                # write line to file
                f.write(line)

            # get total population by calling getTotal method
            total = getTotal()

            # format returned value as string to write on file.
            total_line = ("Total," + str(total) + "\n")

            # write to file
            f.write(total_line)

        # print success message
        print("file created or updated successfully")


# validate input
def validate_input(user_input):
    # will try to cast my_input to an int
    # if that is successful return converted int
    try:
        int_choice = int(user_input)
        return int_choice

    # if a ValueError exception is raised (input can't be cast into an int)
    except ValueError:
        # get a new input from user
        new_choice = input("This is not a number. Try again...")

        # call this method again with new value
        return validate_input(new_choice)


while True:

    # call menu method to print menu
    menu()

    # prompts user to select a menu option.
    my_input = input()

    # validate user input
    choice = validate_input(my_input)

    # if user's choice is 0 (Leave program), close the database and quit the program.
    if choice == 0:
        print("Leaving system...")
        db.close_database()
        exit(0)

    elif choice == 1:
        # upload to file
        upload()

    elif choice == 2:
        # print county populations
        printValues()

    elif choice == 3:
        # get total sum of the population
        total_pop = getTotal()

        # print sum of population
        print("Total population is: " + str(total_pop))

    elif choice == 4:
        # download file "town_sorted_name.txt" with values sorted by name column ASCENDING
        sort("name", "ASC", "town_sorted_name.txt")

    elif choice == 5:
        # download file "town_sorted_population.txt" with values sorted by population column DESCENDING
        sort("amount", "DESC", "town_sorted_population.txt")

    # if user enter a number outside the menu range, return to menu.
    else:
        print("Invalid option. Try again...")
