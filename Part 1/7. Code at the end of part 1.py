import os
dialogue = "Hello my good man."

def print_text(name, dialogue, questions):
    print(name)
    print(" " + dialogue + "\n")
    print("Ask a question:")
    for i in range(len(questions)):
        print(' ' + str(i + 1) + ' - "' + questions[i] + '"')
    print(" e - Exit")

while(True):
    os.system('cls||clear')

    print_text("Sir Regenald", dialogue, ["Are you the theif?", "Did you witness anything?", "Who do you think did it?"])

    users_input = input("Select an option: ")

    if (users_input == "e"):
        break
    else:
        answers = ["No. Absolutely not!" + "\n How DARE you accuse me of that!", "Well, I did see someone running across the rooftop last night at midnight.", "I have no idea, unfortunately."]
        dialogue = answers[int(users_input)-1]
