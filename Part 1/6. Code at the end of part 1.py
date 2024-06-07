questions = ['1 - "Are you the thief?"', '2 - "Did you witness anything?"', '3 - "Did you witness anything?"']
answers = ["No. Absolutely not!\nHow DARE you accuse me of that!", "Select a valid command to ask a question.", "Select a valid command to ask a question."]

while (True):
    print("Sir Regenald")
    print(" Hello my good man.")
    print("-----")
    print("Ask a question:")

    for a in questions:
        print(a)
    print(" e - exit")


    the_input = input("Select: ")
    if (the_input == "e"):
        break
    print(answers[int(the_input)-1])
