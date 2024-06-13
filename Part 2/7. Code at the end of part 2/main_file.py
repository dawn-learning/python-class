import os
from classes_file import *

characters = [
    Suspect(name="Suspect_1", starter_dialogue="a", location=(1, 1))
        .addQuestionAndAnswer(question="Are you the theif?", answer="No. Absolutely not!\n How DARE you accuse me of that!")
        .addQuestionAndAnswer(question="Are you the theif?", answer="No. Absolutely not!")
        .addQuestionAndAnswer(question="Are you the theif?", answer="How DARE you accuse me of that!"), 
    Villian(name="Suspect_2", starter_dialogue="a", location=(1, 1)),
]

while True:
    os.system('cls||clear')
    print("Select a suspect")
    for i in range(len(characters)):
        print(" " + str(i+1) + " - " + characters[i].name)
    print(" e - Exit")
    selection = input()
    if (selection == "e"):
        break
    selected_character_id = int(selection) - 1
    selected_character = characters[selected_character_id]
    dialogue = selected_character.starter_dialogue
    while True:
        os.system('cls||clear')
        print(selected_character.name)
        print(" " + dialogue)
        print("-" * 50)
        for i in range(len(selected_character.questionsAndAnswers)):
            print(' ' + str(i + 1) + ' - "' + selected_character.questionsAndAnswers[i][0] + '"')
        print(" e - Exit")
        selection = input()
        if (selection == "e"):
            break
        else:
            dialogue = selected_character.questionsAndAnswers[int(selection)-1][1]
os.system('cls||clear')
