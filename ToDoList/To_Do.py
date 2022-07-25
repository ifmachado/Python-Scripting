# Write a tool which tracks items to be done. It should do the following:
#  1. There should be a global list of items to be done that starts empty - OK!
#  2. Ask the user to choose an action, eg: add, list, remove - OK!
#  3. Each action should do something, and might require more input, for example:
#   3a. "add" should request the name of the item to do and add it to the list ok!
#   3b. "list" should print out each item. It might be helpful to number the items as well... ok!
#   3c (bonus). "remove" should request something from the user to know which item to remove from the list ok!
#  Bonus: Validate user input ok!


my_list = []

instruct = ("CREATE TO-DO LIST", "These are the available actions:", "add - add to your list",
            "remove - remove from list", "finish - finish your list", "")
print(*instruct, sep="\n")


def print_list():
    for (count, item) in enumerate(my_list, 1):
        print(count, item)

while True:
    userInput = input("Enter an action: [add/remove/finish] ")
    if userInput == "add":
        new_item = input("Enter what you'd like to add: ").capitalize()
        my_list.append(new_item)
        print_list()
    elif userInput == "remove":
        try:
            lose_item = int(input("Enter number on the list you want to remove: ")) - 1
            my_list.pop(lose_item)
            print_list()
        except IndexError:
            print("This number is not on the list. Try again...")
        except ValueError:
            print("This is not a number. Try again...")
    elif userInput == "finish":
        response = input("Are you done with your list? [y/n] ")
        if response.lower().startswith("y"):
            print("This is your list:")
            print_list()
            break
        elif response.lower().startswith("n"):
            continue
        else:
            print("I guess you're not done yet...")
    else:
        print("Action is invalid. Try again...")