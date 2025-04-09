from interviewprint import print_character_dialogue, print_player_options, character_name

print_character_dialogue("what.", name="Amy")
print_player_options("HI how are you?")
print_player_options("WHAT!")
print_player_options("Go away.")

user_input = input()

if user_input == "1":
    print_character_dialogue("I'm fine.")
elif user_input == "2":
    print_character_dialogue("Was 2")
else:
    print_character_dialogue("That was rude.", mood="angry")

print_character_dialogue("Goodbye")

# visual novel
# interactive fiction
# text adventure
