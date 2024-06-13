import os
from classes_file import *

characters = [
    Suspect(name="Suspect_1", starter_dialogue="a", location=(1, 1))
        .addQuestionAndAnswer(question="Are you the theif?", answer="No. Absolutely not!\n How DARE you accuse me of that!")
        .addQuestionAndAnswer(question="Are you the theif?", answer="No. Absolutely not!")
        .addQuestionAndAnswer(question="Are you the theif?", answer="How DARE you accuse me of that!"), 
    Villian(name="Suspect_2", starter_dialogue="a", location=(1, 1)),
]

def clear():
    os.system('cls||clear')

def character_dialogue(name, dialogue):
        print(name)
        print(" " + dialogue)
        print("-" * 50)

def exit_text():
    print(" e - Exit")

while True:
    clear()
    print("Select a suspect")
    for i in range(len(characters)):
        print(" " + str(i+1) + " - " + characters[i].name)
    exit_text()
    selection = input()
    if (selection == "e"):
        break
    selected_character = characters[selected_character_id := int(selection) - 1]
    dialogue = selected_character.starter_dialogue
    while True:
        clear()
        character_dialogue(selected_character.name, dialogue)
        for i in range(len(selected_character.questionsAndAnswers)):
            print(' ' + str(i + 1) + ' - "' + selected_character.questionsAndAnswers[i][0] + '"')
        exit_text()
        selection = input()
        if (selection == "e"):
            break
        dialogue = selected_character.questionsAndAnswers[int(selection)-1][1]
clear()
