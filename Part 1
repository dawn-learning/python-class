Test Example

We want to show text to the user. We could create our own popup window but, in order to run the code we need something called the command line, so we will just use that.

```python

print(print)

print("hi")

```

Command(what we want the command to work with)

So lets add the text to interview a suspect.

```python

print("Sir Regenald")

print(" Hello my good man.")

print("Ask a question:")

print(' "Are you the theif?"')

print(' "Did you witness anything?"')

```

Now we need to figure out which of the options the user want to select.

```Python

print(' 1 - "Are you the theif?"')

print(' 2 - "Did you witness anything?"')

print(input("Select: "))

```

TANGENT

Set equivalence vs check equivalence

```python

10 = 2*x

x = 5

```

a

```python

users_input = input("Select an option: ")

if (users_input == "1"):

    print("No. Absolutely not!")

    print("How DARE you accuse me of that!")

else:

    print("Well, I did see someone running across the rooftop last night at midnight.")

```

add for loop:

```Python

import os

dialogue = "Hello my good man."

while(True):

    os.system('cls||clear')

    print("Sir Regenald")

    print(" " + dialogue + "\n")

    print("Ask a question:")

    print(' 1 - "Are you the theif?"')

    print(' 2 - "Did you witness anything?"')

    print(" e - Exit")

    users_input = input("Select an option: ")

    if (users_input == "1"):

        dialogue = "No. Absolutely not!" + "\n How DARE you accuse me of that!"

    elif (users_input == "2"):

        dialogue = "Well, I did see someone running across the rooftop last night at midnight."

    else:

        break

```

introduce functions:

```python

def print_text():

    print("Sir Regenald")

    print(" " + dialogue + "\n")

    print("Ask a question:")

    print(' 1 - "Are you the theif?"')

    print(' 2 - "Did you witness anything?"')

    print(" e - Exit")

```

introduce parameters in functions

```python

def print_text(name, dialogue):

    print(name)

    print(" " + dialogue + "\n")

    print("Ask a question:")

    print(' 1 - "Are you the theif?"')

    print(' 2 - "Did you witness anything?"')

    print(" e - Exit")

```

introduce lists:

```python

['"Are you the theif?"', '"Did you witness anything?"']

```

```python

def print_text(name, dialogue, questions):

    print(name)

    print(" " + dialogue + "\n")

    print("Ask a question:")

    print(' 1 - ' + questions[0])

    print(' 2 - ' + questions[1])

    print(" e - Exit")

```

loops:

```python

for question in questions:

        print(' 1 - "' + question + '"')

```

for i:

```python

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

    if (users_input == "1"):

        dialogue = "No. Absolutely not!" + "\n How DARE you accuse me of that!"

    elif (users_input == "2"):

        dialogue = "Well, I did see someone running across the rooftop last night at midnight."

    else:

        break

```

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

