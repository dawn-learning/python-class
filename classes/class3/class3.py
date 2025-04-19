# inheritance --> City(Location)

class Location():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class City(Location):
    def __init__(self, x, y):
        super().__init__(x, y)

class Player(Location):
    def __init__(self, x, y, inventory):
        super().__init__(x, y)
        self.inventory = inventory

cities = [City(3, 5), City(5, 2), City(6, 6), City(0, 7)]
player = Player(1, 1, [])

for y in range(8):
    for x in range(8):
        square = '🟩'
        for city in cities:
                if x == city.x and y == city.y:
                    square = '🟫'
        if x == player.x and y == player.y:
            square = '❤ '
        print(square, end='')
    print()

with open('text.txt', 'r') as f:
    player.inventory = f.read().splitlines()

print(player.inventory)
player.inventory.append('cat')

with open('text.txt', 'w') as f:
    for a in player.inventory:
        f.write(a + '\n')

print(player.inventory)