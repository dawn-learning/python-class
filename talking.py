import os
game_not_over = True

rooms_list = ["living room", "kitchen", "bathroom", "bedroom"]
print("You enter the house. You know who the killer is, you just have to prove if by finding the murder weapon.")

# Rooms selection
while (game_not_over):
    os.system("cls||clear")
    print("The house has four rooms:")
    for room in rooms_list:
        print(room)
    print("Which room do you want to look in?")
    selected_room = input()

    if (selected_room == "living room"):
        objects_in_room = ["dresser", "couch", "cat", "lamp", "newspaper"]
    elif (selected_room == "kitchen"):
        objects_in_room = ["dresser", "couch", "cat", "lamp", "newspaper"]
    elif (selected_room == "bathroom"):
        objects_in_room = ["dresser", "couch", "cat", "lamp", "newspaper"]
    elif (selected_room == "bedroom"):
        objects_in_room = ["dresser", "couch", "cat", "lamp", "newspaper"]
    elif (selected_room == "e" or selected_room == "exit"):
            break
    else:
        print("Select a room")
        continue

    print("You enter the " + selected_room + ".")
    # Checking room
    while (True):
        os.system("cls||clear")
        print("You find several objects. \nWhich one do you look under for the murder weapon?")
        for object in objects_in_room:
            print(object)
        selected_object = input()

        if (selected_object == "couch" and selected_room == "living room"):
            print("You check under the couch. You find the knife.\nYou have the evidence to convict the killer.")
            game_not_over = False
            break
        elif (selected_object == "e" or selected_object == "exit"):
            break
        elif (selected_object in objects_in_room):
            print("You find nothing of note under the " + selected_object + ".\nYou need to keep searching.")
        else:
            print("Select an object")
