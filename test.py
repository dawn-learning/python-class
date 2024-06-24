from interviewprint import print_character, print_player


# print("hi")


# x = input()
# if (x == 1):
#     print(x)

print_character("Hi player", "Happy")
print_character("Going well?")
print_player("HI")
print_player("How's it going")
print_player("go away")

x = input()
if (x == "1"):
    print_character("How's it going")
    print_player("Bad")
    print_player("Good")
    print_player("MEH") # is the "meh" one
elif (x == "2"):
    print_character("How's it going")
    print_player("import")
    print_player("Good")
    print_player("MEH")
else:
    print_character("How's it going")
    print_player("Bad")
    print_player("Good")
