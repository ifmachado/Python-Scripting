import random

answer = random.randint(1,10)
tries = 3
print ("Welcome to Guessing Game!")
while tries > 0:
    try:
        print("You have", tries, "tries.")
        userInput = int(input("Enter a number from 1 to 10:"))
        if userInput == answer:
            print("You win!")
            response = input("Play again? [y/n]")
            if response.lower().startswith("y"):
                answer = random.randint(1, 10)
                tries = 3
                continue
            break
        elif (userInput == answer + 1) or (userInput == answer - 1):
            print("Almost There!")
            tries = tries - 1
        elif userInput > answer:
            print("Too high.")
            tries = tries - 1
        elif userInput < answer:
            print("Too low.")
            tries = tries - 1
        if tries <=0:
            print("You lose. The answer was", answer)
            response = input("Play again? [y/n]")
            if response.lower().startswith("y"):
                answer = random.randint(1, 10)
                tries = 3
                continue
            break
    except ValueError:
        print("This is not a number. Try again...")
