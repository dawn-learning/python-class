from turn_functions import *

def new_level(enemy):
    enemy_health = 20
    hero_health = 10

    while enemy_health > 0:
        print_screen(enemies=enemy, disable_animations=False)
        print_health_bars(enemy_health=enemy_health, hero_health=hero_health)

        attacks = ['poke', 'whack', 'bludgeon']
        # print(attacks[0])
        # attacks.append('hit')
        # attacks.remove('hit')

        for i, attack in enumerate(attacks):
            print(i + 1, ':', attack)

        user_input: str = input()
        user_input = int(user_input) - 1
        user_input = attacks[user_input]

        if user_input == 'poke':
            enemy_health = enemy_health - 1
        elif user_input == 'whack':
            enemy_health = enemy_health - 2
        elif user_input == 'bludgeon':
            enemy_health = enemy_health - 5

        hero_health = hero_health - 2

    print_screen(enemies=enemy)
    print_health_bars(enemy_health=enemy_health, hero_health=hero_health)

new_level(character.SNAKE)
new_level(character.SCORPION)
new_level(character.DRAGON)
print('you win!')