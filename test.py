import os

def print_text(name, dialogue, questions):
    print(name)
    print(" " + dialogue + "\n")
    print("Ask a question:")
    for i in range(len(questions)):
        print(' ' + str(i + 1) + ' - "' + questions[i] + '"')
    print(" e - Exit")

name = "Sir Regenald"
dialogue = "Hello my good man."
questions = ["Are you the theif?", "Did you witness anything?", "Who do you think did it?"]

while(True):
    os.system('cls||clear')

    print_text(name, dialogue, questions)

    users_input = input("Select an option: ")

    if (users_input == "e"):
        break
    else:
        answers = ["No. Absolutely not!" + "\n How DARE you accuse me of that!", "Well, I did see someone running across the rooftop last night at midnight.", "I have no idea, unfortunately."]
        dialogue = answers[int(users_input)-1]
