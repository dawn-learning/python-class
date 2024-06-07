
reformat to use classes:

```python
class interviewe():
    def __init__(self, name, questions, answers, default):
        self.name = name
        self.questions = questions
        self.answers = answers
        self.default = default

def print_text(name, dialogue, questions):
    os.system('cls||clear')
    print(name)
    print(" " + dialogue + "\n")
    print("Ask a question:")
    for i in range(len(questions)):
        print(' ' + str(i + 1) + ' - "' + questions[i] + '"')
    print(" e - Exit")

character = interviewe("Sir Regenald", ["Are you the theif?", "Did you witness anything?", "Who do you think did it?"], [
        "No. Absolutely not!" + "\n How DARE you accuse me of that!",
        "Well, I did see someone running across the rooftop last night at midnight.",
        "ah"
    ], "Hello my good man.")

dialogue = character.default

while(True):
    print_text(character.name, dialogue, character.questions)
    users_input = input("Select an option: ")
    if (users_input == "e"):
        break
    for i in range(len(character.questions)):
        dialogue = character.answers[int(users_input)-1]
```

Fancy

```python
import os

class interviewe():
    def __init__(self, name, questions, answers, default):
        self.name = name
        self.questions = questions
        self.answers = answers
        self.default = default

def print_text(name, dialogue, questions):
    os.system('cls||clear')
    print(name)
    print(" " + dialogue + "\n")
    print("Ask a question:")
    for i in range(len(questions)):
        print(' ' + str(i + 1) + ' - "' + questions[i] + '"')
    print(" e - Exit")

def talkWithCharacter(character):
    dialogue = character.default
    while(True):
        print_text(character.name, dialogue, character.questions)
        users_input = input("Select an option: ")
        if (users_input == "e"):
            break
        for i in range(len(character.questions)):
            dialogue = character.answers[int(users_input)-1]

character = interviewe("Sir Regenald", ["Are you the theif?", "Did you witness anything?", "Who do you think did it?"], [
        "No. Absolutely not!" + "\n How DARE you accuse me of that!",
        "Well, I did see someone running across the rooftop last night at midnight.",
        "ah"
    ], "Hello my good man.")

while(True):
    print("Speak to:")
    print("1 - Sir Regenald")
    print("2 - George")
    users_input = input("Select an option: ")
    if (users_input == "1"):
        talkWithCharacter(character)
```
