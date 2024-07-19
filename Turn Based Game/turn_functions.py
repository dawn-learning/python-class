from __future__ import annotations
from os import system
import random
from enum import Enum
from time import sleep

screen_height = 17
screen_width = 77

global previous_enemies
previous_enemies = None
global previous_hero
previous_hero = None
global last_enemies_input
last_enemies_input = None

class character(Enum):
    HERO = "Hero"
    SNAKE = "Snake"
    SCORPION = "Scorpion"
    DRAGON = "Dragon"


class characters():
    def to_subclass(potential_character):
        if potential_character == character.HERO:
            return Hero()
        elif potential_character == character.SNAKE:
            return Snake()
        elif potential_character == character.SCORPION:
            return Scorpion()
        elif potential_character == character.DRAGON:
            return Dragon()

    def _shrink_character(character):
        smaller_version = []
        for i in range(int(len(character)/2)):
            new_row = ""
            first_row = i * 2
            second_row = i*2 + 1
            if second_row >= len(character):
                second_row = None
            for j in range(int(len(character[0])/2)):
                first_element = j * 2
                second_element = j * 2 + 1
                if second_element >= len(character[0]):
                    second_element = None
            
                items = {}

                def for_row_column(row, col):
                    if character[row][col] in items:
                        items[character[row][col]] += 1
                    else:
                        items[character[row][col]] = 1

                for_row_column(first_row, first_element)
                if second_element:
                    for_row_column(first_row, second_element),
                if second_row:
                    for_row_column(second_row, first_element),
                    if second_element:
                        for_row_column(second_row, second_element),

                max = ""
                max_value = -1
                for a in items.keys():
                    if items[a] > max_value:
                        max = a
                        max_value = items[a]
                new_row += max
            smaller_version.append(new_row)
        return smaller_version

    def is_a_character(obj):
        return True

class Hero(characters):
    def __init__(self) -> None:
        self.basic_art = [
            "🤍🟪🤍🤍",
            "🤍🟪🟪🤍",
            "🟪🟪🟪🟪",
            "🤍⬜⬜🤍",
            "🟪🟪🟪🤍",
            "🤍🟪🟪🤍",
            "🤍🟪🟪🤍",
        ]
        self.wand_art = [
            "🤍",
            "🟫",
            "🟫",
            "🟫",
            "🟫",
            "🤍",
            "🤍",
        ]
        self.wand_art_down = [
            "🤍🤍🤍",
            "🤍🤍🤍",
            "🤍🤍🤍",
            "🤍🤍🤍",
            "🟫🟫🟫",
            "🤍🤍🤍",
            "🤍🤍🤍",
        ]
        self.art = [self.wand_art[i] + self.basic_art[i] for i in range(len(self.basic_art))]

class Snake(characters):
    def __init__(self) -> None:
            self.type = "Fire"
            self.art = [
            "🤍🤍🤍🤍🟥🟥🤍🤍🟥🟥🤍🤍🤍🤍",
            "🤍🤍🤍🤍🟥🟥🤍🤍🟥🟥🤍🤍🤍🤍",
            "🤍🤍🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🤍🤍",
            "🤍🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🤍",
            "🟥🟥🟥🟥🤍🟥🟥🟥🟥🟥🤍🤍🟥🟥",
            "🟥🟥🟥🟥🤍🤍🟥🟥🟥🟥🤍🤍🟥🟥",
            "🟥🟥🟥🟥🤍🤍🤍🤍🤍🟥🟥🟥🟥🟥",
            "🟥🟥🟥🟥🤍🤍🤍🤍🤍🤍🟥🟥🟥🤍",
            "🟥🟥🟥🟥🟥🤍🤍🤍🤍🤍🤍🤍🤍🤍",
            "🟥🟥🟥🟥🟥🟥🟥🤍🤍🤍🤍🤍🤍🤍",
            "🤍🟥🟥🟥🟥🟥🟥🟥🟥🤍🤍🤍🤍🤍",
            "🤍🤍🟥🟥🟥🟥🟥🟥🟥🟥🟥🤍🤍🤍",
            "🤍🤍🤍🤍🟥🟥🟥🟥🟥🟥🟥🟥🟥🤍",
            "🤍🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥",
        ]

    def animation(self, step):
        step = 13-step
        new_art = self.art.copy()
        for _ in range(step):
            new_art.insert(0, "🤍" * len(new_art[0]))
        for _ in range(step):
            new_art.pop()
        return new_art

class Scorpion(characters):
    def __init__(self) -> None:
        self.type = "Earth"
        self.art = [
            "🤍🤍🟫🟫🟫🟫🟫🟫🤍🤍🤍🤍🤍🤍",
            "🤍🟫🟫🟫🟫🟫🟫🟫🟫🤍🤍🤍🤍🤍",
            "🟫🟫🟫🟫🤍🤍🤍🟫🟫🟫🤍🤍🤍🤍",
            "🟫🟫🟫🤍🤍🤍🤍🤍🟫🟫🤍🤍🤍🤍",
            "🟫🟫🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍",
            "🟫🟫🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍🤍",
            "🟫🟫🟫🟫🟫🟫🤍🤍🤍🤍🤍🤍🤍🤍",
            "🟫🟫🟫🟫🟫🟫🤍🤍🤍🤍🤍🤍🤍🤍",
            "🤍🤍🟫🟫🟫🟫🟫🟫🟫🟫🤍🤍🤍🤍",
            "🤍🤍🟫🟫🟫🟫🟫🟫🟫🟫🤍🤍🤍🤍",
            "🟫🟫🤍🤍🟫🟫🟫🟫🤍🤍🟫🟫🟫🟫",
            "🟫🟫🤍🤍🟫🟫🟫🟫🤍🤍🟫🟫🟫🟫",
            "🟫🟫🤍🤍🟫🟫🤍🤍🟫🟫🟫🟫🤍🤍",
            "🟫🟫🤍🤍🟫🟫🤍🤍🟫🟫🟫🟫🤍🤍",
        ]

    def animation(self, step):
        new_art = self.art.copy()
        if step < 7:
            for _ in range(7-step):
                new_art.pop(0)
                new_art.pop(0)
                new_art.append("🤍" * len(self.art[0]))
                new_art.append("🤍" * len(self.art[0]))
        elif step > 7:
            if step < 10:
                new_art.pop()
                new_art.insert(0, "🤍" * len(self.art[0]))
            if step >= 9 and step < 12:
                new_art.pop(5)
                new_art.insert(0, "🤍" * len(self.art[0]))
        return new_art


class Dragon(characters):
    def __init__(self, small = False) -> None:
        self.type = "Water"
        self.art = [
            "🤍🤍🤍🟦🟦🟦🤍🤍🤍🤍🤍🤍🤍🤍",
            "🤍🤍🤍🤍🟦🟦🟦🟦🤍🤍🟦🟦🤍🤍",
            "🤍🤍🤍🤍🤍🟦🟦🟦🟦🟦🤍🤍🟦🟦",
            "🤍🤍🤍🤍🤍🟦🟦🟦🟦🟦🤍🤍🟦🟦",
            "🤍🤍🤍🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦",
            "🤍🤍🤍🤍🟦🟦🟦🟦🟦🟦🟦🤍🤍🤍",
            "🤍🤍🤍🤍🤍🤍🟦🟦🟦🤍🤍🤍🤍🤍",
            "🤍🤍🤍🤍🟦🟦🟦🟦🟦🟦🤍🤍🤍🤍",
            "🤍🤍🤍🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🤍",
            "🤍🤍🤍🟦🟦🟦🟦🟦🟦🟦🟦🟦🤍🤍",
            "🟦🤍🤍🟦🟦🟦🟦🟦🟦🟦🤍🤍🤍🤍",
            "🟦🟦🤍🤍🟦🟦🟦🟦🟦🟦🤍🤍🤍🤍",
            "🤍🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🤍🤍🤍",
            "🤍🤍🟦🟦🟦🟦🟦🤍🤍🟦🟦🟦🤍🤍",
        ]

        if small:
            self.art = characters._shrink_character(self.art)

    def animation(self, step):
        step = 14-step
        new_art = self.art.copy()
        for i in range(len(self.art)):
            delete_budget = (len(self.art)-i + 1)*step-14
            if delete_budget < 0: delete_budget = 0
            # print(delete_budget)
            for _ in range(delete_budget):
                spot = random.randint(0, len(self.art[i])-1)
                # print("before", new_art[i], spot)
                new_art[i] = new_art[i][0 : spot] + "🤍" + new_art[i][spot+1:]
                # print("after ", new_art[i])
        return new_art
        # return []


def clear_screen():
    system("cls || clear")

def print_screen(enemies : characters = None, hero = Hero(), screen_clear : bool = True, disable_animations : bool = True):
    global last_enemies_input
    trigger_intro_animation = last_enemies_input != enemies and enemies != None and not disable_animations
    last_enemies_input = enemies
    
    if type(enemies) == character:
        enemies = characters.to_subclass(enemies)
    if type(hero) == character:
        hero = characters.to_subclass(hero)

    # Type checking
    global previous_enemies
    global previous_hero

    if not enemies:
        enemies = previous_enemies
    if not hero:
        hero = previous_hero
    try:
        if not characters.is_a_character(enemies):
            e = Exception(f"enemies must be a character or a list of characters. Is a {type(enemies)}")
            if type(enemies) != list:
                raise e
            for a in enemies:
                if not characters.is_a_character(a):
                    raise e
    except:
        raise Exception("enemies must be a character or a list of characters")
    try:
        if not characters.is_a_character(hero):
            raise Exception("hero must be a character")
    except:
        raise Exception("hero must be a character")
    if not type(screen_clear) == bool:
        raise Exception("clear_screen must be a boolean")

    if type(enemies) != list:
        enemies = [enemies]

    previous_enemies = enemies
    previous_hero = hero

    def print_output(output):
        if screen_clear: clear_screen()
        for a in output:
            print(f'{a.replace("🤍", "  ")}')
        print() # Spacer

    # SETTINGS
    HERO_GROUND_SPACE = 10

    if trigger_intro_animation:
        for step in range(15):
            print_output(_get_2D_array_to_print(enemies = enemies, hero = hero, hero_ground_space = HERO_GROUND_SPACE, step=step))
            sleep(0.05)
    else:
        print_output(_get_2D_array_to_print(enemies = enemies, hero = hero, hero_ground_space = HERO_GROUND_SPACE, step=14))


def _get_2D_array_to_print(enemies, hero, hero_ground_space, step):
    output = []
    for i in range(screen_height):
        line = ""
        seporator = int((screen_width-4)/2)
        for j in range(len(enemies)):
            enemy = enemies[j].animation(step)
            if i < len(enemy):
                enemy_text = enemy[len(enemy)-1-i]
                seporator -= len(enemy_text)
                if j != 0:
                    seporator -= 1
                    enemy_text = "🤍" + enemy_text
                if enemies[j].type == "Fire" or enemies[j].type == "Water":
                     for block in enemy_text:
                        if block == "🟥":
                            if (random.randint(0, 1) == 0):
                                line += "🟧"
                            else:
                                line += "🟥"
                        elif block == "🟦":
                            if (random.randint(0, 5) == 0):
                                line += "🟩"
                            else:
                                line += "🟦"
                        else:
                            line += block
                else:
                    line += enemy_text
        if i < len(hero.art):
            hero_text = hero.art[len(hero.art)-1-i]
            seporator -= len(hero_text)
            line += "🤍" * seporator
            line += hero_text
        else:
            line += "🤍" * seporator
        output.insert(0, "🤍" + line + "🤍")

    enemy_ground_side = 0
    hero_ground_size = 0
    width__blocks_count = int(screen_width/2)
    if enemies and not hero:
        enemy_ground_side = width__blocks_count
    if not enemies and hero:
        hero_ground_size = width__blocks_count
    if enemies and hero:
        hero_ground_size = hero_ground_space
        enemy_ground_side = width__blocks_count - hero_ground_size
    ground = ""
    for _ in range(enemy_ground_side):
        if enemies[0].type == "Fire":
            if random.randint(0, 2) == 0:
                ground += "🟥"
            else:
                ground += "🟧"
        elif enemies[0].type == "Water":
            if random.randint(0, 5) == 0:
                ground += "🟩"
            else:
                ground += "🟦"
        else:
            ground += "🟫"
    ground += "🟫" * hero_ground_size
    output.append(ground)

    return output



def print_health_bars(
        enemy_health : int | list[int] | None = None, 
        enemy_max_health : int | list[int] | None = 20,
        enemy_name : str | list[str] = [], 
        enemy_overhealth : int | list[int] | None = None,
        hero_health : int | None = None, 
        hero_name : str = "Hero",
        hero_max_health : int | None = 10,
        hero_overhealth : int | None = 0,
    ) -> None:
    '''
    Prints the hero and villian/s health bars to the screen.
    Depends on screen width.
    '''
    # Type checking
    if not (type(enemy_health) == int or type(enemy_health) == list or enemy_health == None):
        raise Exception("enemy_health is of wrong type")
    if not (type(enemy_max_health) == int or type(enemy_max_health) == list or enemy_max_health == None):
        raise Exception("enemy_max_health is of wrong type")
    if not (type(enemy_name) == str or type(enemy_name) == list):
        raise Exception("enemy_name is of wrong type")
    if not (type(enemy_overhealth) == int or type(enemy_overhealth) == list or enemy_overhealth == None):
        raise Exception("enemy_overhealth is of wrong type")
    if not (type(hero_health) == int or hero_health == None):
        raise Exception("hero_health is of wrong type")
    if not (type(hero_name) == str):
        raise Exception("hero_name is of wrong type")
    if not (type(hero_max_health) == int or hero_max_health == None):
        raise Exception("hero_max_health is of wrong type")
    if not (type(hero_overhealth) == int or hero_overhealth == None):
        raise Exception("hero_overhealth is of wrong type")
    
    # Ensuring the variables are properly setup no matter what valid set of variables given
    if enemy_health != None and type(enemy_health) != list:
        enemy_health = [enemy_health]
    if not enemy_name:
        enemy_name = "Enemy1"
    if not enemy_overhealth:
        enemy_overhealth = 0
    if enemy_name and type(enemy_name) != list:
        enemy_name = [enemy_name]
    if enemy_max_health and type(enemy_max_health) != list:
        enemy_max_health = [enemy_max_health]
    if type(enemy_overhealth) != list:
        enemy_overhealth = [enemy_overhealth]
    if enemy_health != None:
        while len(enemy_health) > len(enemy_max_health):
            enemy_max_health.append(enemy_max_health[len(enemy_max_health)-1])
    for i in range(len(enemy_health)):
        if i >= len(enemy_name):
            enemy_name.append(f"Enemy{i+1}")
    while len(enemy_overhealth) < len(enemy_health):
        enemy_overhealth.append(0)
    for i in range(len(enemy_health)):
        if enemy_health[i] < 0:
            enemy_health[i] = 0
    if hero_health < 0:
        hero_health = 0
    for i in range(len(enemy_overhealth)):
        if enemy_overhealth[i] < 0:
            enemy_overhealth[i] = 0
    if hero_overhealth < 0:
        hero_overhealth = 0


    lines = []
    first_enemy_line_length = 0
    hero_line_length = 0
    smallest_allowed_space_inbetween = 4


    if enemy_health != None:
        # For each enemy
        for i in range(len(enemy_health)):
            # Creating line
            eh = enemy_health[i]
            mh = enemy_max_health[i]
            overhealth = enemy_overhealth[i]
            if eh > mh:
                overhealth = eh - mh
                eh = mh
            lines.append(f"{enemy_name[i]} " + "🟩" * eh + "⬛" * (mh-eh) + "🟨" * overhealth)
            if i == 0: first_enemy_line_length = len(enemy_name[i]) + 1 + (mh + overhealth) * 2

    if hero_health != None:
        # Creating line
        overhealth = hero_overhealth
        if hero_health > hero_max_health:
            overhealth = hero_health - hero_max_health
            hero_health = hero_max_health
        line = "🟨" * overhealth + "⬛" * (hero_max_health-hero_health) + "🟩" * hero_health + f" {hero_name}"

        # Finding where to put line
        hero_line_length = len(hero_name) + 1 + (hero_max_health + overhealth) * 2
        if len(lines) < 1:
            lines.append(" " * (screen_width - hero_line_length - 1) + line)
        elif first_enemy_line_length + hero_line_length + smallest_allowed_space_inbetween < screen_width:
            temp = screen_width - (first_enemy_line_length + hero_line_length + 1)
            lines[0] += " " * temp + line
        else:
            lines.insert(0, " " * (screen_width - hero_line_length - 1) + line)

    # Printing the health bars
    for a in lines:
        print(a)
    print() # Spacer

def print_game_over():
    clear_screen()
    game_over_logo = [
        " --==/ \==-- ",
        "| GAME OVER |",
        " --==\ /==-- ",
    ]
    sw = int((screen_width - len(game_over_logo[0]))/2)
    for _ in range(int((screen_height - len(game_over_logo))/2)):
        print()
    for a in game_over_logo:
        print(" " * sw + a)
    for _ in range(int((screen_height - len(game_over_logo))/2)):
        print()

def print_victory():
    clear_screen()
    game_over_logo = [
        " --==/ \==-- ",
        "|  VICTORY  |",
        " --==\ /==-- ",
    ]
    sw = int((screen_width - len(game_over_logo[0]))/2)
    for _ in range(int((screen_height - len(game_over_logo))/2)):
        print()
    for a in game_over_logo:
        print(" " * sw + a)
    for _ in range(int((screen_height - len(game_over_logo))/2)):
        print()
