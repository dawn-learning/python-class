from os import system

class Location():
    def __init__(self, x, y, name = None, wants = None, gives = None) -> None:
        self.x = x
        self.y = y
        self.name = name
        self.wants = wants
        self.gives = gives
        self.complete = False

class Player():
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.money = 0

locations = [
    Location(0, 0, "Ilcanor", "Stone", "Grain"), 
    Location(3, 2, "Ballan", "Water", "Stone"),
    Location(1, 1, "Staring town", gives = "Water"),
]
player = Player(0, 0)
inventory = []

def render_screen():
    system("cls || clear")
    for i in range(10):
        for j in range(10):
            element = "🟩"
            for a in locations:
                if j == a.x and i == a.y:
                    element = "🟥"
            if j == player.x and i == player.y:
                element = "💗"
            print(element, end="")
        print()
    print("inventory:", inventory)
    print(player.money)


def update_user():
    user_input = input()
    if user_input.startswith("u"):
        player.y -= 1
    if user_input.startswith("d"):
        player.y += 1
    if user_input.startswith("r"):
        player.x += 1
    if user_input.startswith("l"):
        player.x -= 1

while (True):
    render_screen()
    update_user()
    for a in locations:
        if a.x == player.x and a.y == player.y and not a.complete:
            system("cls || clear")
            print(a.name)
            print(a.wants)
            print(a.gives)
            input()
            if a.wants == None:
                inventory.append(a.gives)
                a.complete = True
            elif a.wants in inventory:
                inventory.remove(a.wants)
                inventory.append(a.gives)
                a.complete = True
                player.money += 1000
                print("Thanks")
    if player.money >= 2000: break
system("cls || clear")
print("Victory")
