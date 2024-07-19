from turn_functions import *

def run_level(attacks, hero_health, enemy):
    enemy_health : int = 20
    while (enemy_health > 0):
        print_screen(enemies=enemy, disable_animations=False)
        print_health_bars(enemy_health=enemy_health, hero_health=hero_health)
        for i in range(len(attacks)):
            print(i+1, attacks[i])
        user_input = input()
        if user_input == "1":
            enemy_health = enemy_health -1
        elif user_input == "2":
            enemy_health = enemy_health - 2
        elif user_input == "3":
            enemy_health = enemy_health - 5
        hero_health -= 1
        if hero_health < 1:
            print_game_over()
            quit()
    print_screen(enemies=enemy)
    print_health_bars(enemy_health=enemy_health, hero_health=hero_health)
    return hero_health

hero_health : int = 10
attacks : list = ["Whack", "Thrust"]
attacks.append("Magic")

hero_health = run_level(attacks, hero_health, character.SCORPION)
run_level(attacks, hero_health, character.SNAKE)
print_victory()
