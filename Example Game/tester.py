from __future__ import annotations
import msvcrt
from os import system
from random import randint

def wait_for_character_input():
    text = msvcrt.getch()
    if text == b'\xe0':
        text = msvcrt.getch().decode("utf-8")
        match (text):
            case "H":
                text = "UP"
            case "M":
                text = "RIGHT"
            case "K":
                text = "LEFT"
            case "P":
                text = "DOWN"
            case "S":
                text = "DELETE"
    elif str(text).startswith("b'\\"):
        text = str(text).lstrip("b'").rstrip("'")
        if text == "\\r":
            text = "\\n"
        elif text == "\\x08":
            text = "BACKSPACE"
        elif text == "\\x03":
            exit()
    else:
        text = text.decode("utf-8")
    return text

def wait_for_line_input():
    return input()


class Color():
    WHITE = 0
    BLACK = 1
    RED = 2
    BLUE = 3
    ORANGE = 4
    YELLOW = 5
    GREEN = 6
    PURPLE = 7
    BROWN = 8

    def get_circular_emoji(color):
        return "⚪⚫🔴🔵🟠🟡🟢🟣🟤"[color]

    def get_square_emoji(color):
        return "⬛⬜🟥🟦🟧🟨🟩🟪🟫"[color]

class ColorEmoji():
    def __init__(self, color : Color) -> None:
        self.base = Color.get_circular_emoji(color)
        self.selected = Color.get_square_emoji(color)

class Gem():
    def __init__(self, x = -1, name = None, description = None, color = Color.BROWN) -> None:
        self.x = x
        self.name = name
        self.description = description
        self.color = ColorEmoji(color)

# while True:
#     wait_for_character_input()

screen_width = 40
wand_height = 21
wand_width = 3 * 2

gems_list = [
    [Gem(x=randint(0, screen_width), name="Power", description="x3 damage", color=Color.PURPLE), Gem(x=randint(0, screen_width), name="Poison", description="1 extra damage every round", color=Color.ORANGE)],
    [Gem(x=randint(0, screen_width), name="Poison", description="1 extra damage every round", color=Color.GREEN)],
    [Gem(x=randint(0, screen_width), name="Poison", description="1 extra damage every round", color=Color.PURPLE)],
    [Gem(x=randint(0, screen_width), name="Poison", description="1 extra damage every round", color=Color.RED)],
    [Gem(x=randint(0, screen_width), name="Poison", description="1 extra damage every round", color=Color.ORANGE)],
]


def clear_screen():
    system("cls | clear")



def print_wand():
    def get_line(side, center):
        RIGHT_SIDE = False
        line = ""
        for _ in range(side):
            line += " "
        line += "🟫" + center +"🟫"
        if RIGHT_SIDE:
            for _ in range(side):
                line += " "
            if side != (screen_width - wand_width)/2:
                line += " "
        return line

    clear_screen()
    side = int((screen_width - wand_width)/2)
    print(get_line(side, "🟫"))
    for i in range(int(wand_height/2)).__reversed__():
        if i >= len(gems):
            line = get_line(side, "🟫")
            print(line + "\n" + line)
            continue
        line = get_line(side, gems[i].color.base)
        if gems[i].name != None:
            print(line.rstrip() + "   " + gems[i].name)
            print(get_line(side, "🟫") + "    " + gems[i].description)
        else:
            print(line)
            print(get_line(side, "🟫"))


def print_gems(spot_y, spot_x):
    for i in range(len(gems_list)):
        line = " " * screen_width
        for j in range(len(gems_list[i])):
            a = gems_list[i][j]
            line = line[0:a.x] + (a.color.base if i != spot_y or j != spot_x else a.color.selected) + line[a.x+2:]
        print(line)
        gems = [a[0] for a in gems_list]
        between_lines = []
        if i < len(gems)-1:
            next_gem = gems[i+1].x
            difference = abs(gems[i].x - next_gem)
            smaller = gems[i].x if gems[i].x < next_gem else next_gem
            if difference > 10:
                if smaller == gems[i].x:
                    next_gem = next_gem - 5
                else:
                    next_gem = next_gem + 5
            difference = abs(gems[i].x - next_gem)
            smaller = gems[i].x if gems[i].x < next_gem else next_gem
            if difference <= 3:
                if smaller == gems[i].x:
                    between_lines.append(" " * (smaller + 1) + "|")
                    between_lines.append(" " * (smaller + 1) + " |")
                else:
                    between_lines.append(" " * (smaller + 1) + " |")
                    between_lines.append(" " * (smaller + 1) + "|")
                continue
            slash = "\\"
            if gems[i].x > next_gem:
                slash = "/"
            if smaller == gems[i].x:
                between_lines.append(" " * (smaller+1) + slash)
            else:
                between_lines.append(" " * (smaller) + " " * (difference) + slash)
            between_lines.append(" " * (smaller+1) + " " + "-" * (difference-2))
            if smaller == gems[i].x:
                between_lines.append(" " * (smaller) + " " * (difference) + slash)
            else:
                between_lines.append(" " * (smaller+1) + slash)

        for a in between_lines:
            print(a)

class TextLayer():
    def __init__(self, width, text_array = []) -> None:
        self.width = width
        self.text_array = text_array

    def append(self, text):
        self.text_array.append(text)

    def insert(self, position, text):
        self.text_array.insert(position, text)

    def __str__(self) -> str:
        if len(self.text_array) == 0:
            return "EMPTY"
        output = ""
        for a in self.text_array:
            output += a
            output += "\n"
        return output[:len(output)-1]

    def get_longest_line(self):
        longest_line = -1
        for a in self.text_array:
            length = true_len(a)
            if length > longest_line:
                longest_line = length
        return longest_line

    def next_to(self, other : TextLayer, offset = 0, offset_string = " ", align = "TOP", fill : int | None = None):
        if fill:
            self.width = fill
        else:
            self.width += other.width

        longest_line = self.get_longest_line()
        other_longest_line = other.get_longest_line()

        other = other.text_array

        extra = offset_string * offset
        if fill:
            extra = " " * (fill - (longest_line + other_longest_line))

        for i in range(len(other)):
            if i < len(self.text_array):
                self.text_array[i] += " " * (longest_line - true_len(self.text_array[i])) + extra + other[i]
            else:
                self.text_array.append(" " * longest_line + extra + other[i])

    def align_to_right(self):
        longest_line = self.get_longest_line()
        left_padding = self.width - longest_line
        if left_padding <= 0:
            return
        for i in range(len(self.text_array)):
            self.text_array[i] = " " * left_padding + self.text_array[i]


def decolorize(text):
    output = text
    while "\x1b" in output:
        start = output.index("\x1b")
        end = output[start:].index("m")+start+1
        output = output[:start] + output[end:]
    return output

def true_len(text):
    colorless_text = decolorize(text)
    length = len(colorless_text)
    # if "\x1b[0m" in a:
    #     length -= len("\x1b[4m\x1b[0m")
    for b in ["🟩", "⬛", "🔥", "🤢"]:
        if b in colorless_text:
            length += colorless_text.count(b)
    return length



def print_gems(gems_x = 0, gems_y = 0):
    textlayer = TextLayer(width=25)
    for i in range(len(gems_list)):
        if i == gems_y:
            gems_display = ""
            for j in range(len(gems_list[i])):
                if j == gems_x:
                    gems_display += gems_list[i][j].color.base + "   "
                else:
                    gems_display += " " * 5
            textlayer.append("| " + gems_display + " " * (textlayer.width-(5 * len(gems_list[i]))-1) + "|")
        else:
            textlayer.append("|" + " " * textlayer.width + "|")
        gems_display = ""
        for j in range(len(gems_list[i])):
            if j == gems_x and i == gems_y:
                gems_display += "     "
            else:
                gems_display += gems_list[i][j].color.base + "   "
        textlayer.append("| " + gems_display + " " * (textlayer.width-(5 * len(gems_list[i]))-1) + "|")
        textlayer.append("|" + "‾" * textlayer.width + "|")


    textlayer2 = TextLayer(width=20)

    textlayer2.append("")
    textlayer2.append(gems_list[gems_y][gems_x].name)
    textlayer2.append(gems_list[gems_y][gems_x].description)
    textlayer.next_to(textlayer2, offset=3)
    print(textlayer)






# spot_y = 0
# spot_x = 0
# while (True):
#     clear_screen()
#     print_gems(spot_x, spot_y)
#     input = wait_for_character_input()
#     print(input, spot_y)
#     if input == "DOWN":
#         if spot_y < len(gems_list)-1:
#             spot_y += 1
#             if spot_x >= len(gems_list[spot_y]):
#                 spot_x = len(gems_list[spot_y])-1
#     if input == "UP":
#         if spot_y > 0:
#             spot_y -= 1
#     if input == "RIGHT":
#         if spot_x < len(gems_list)-1:
#             spot_x += 1
#     if input == "LEFT":
#         if spot_x > 0:
#             spot_x -= 1



# hi = "HI"
# print(f"\033[93m {hi}\033[40m {hi}")




def colorize(text : str, color : str):
    '''
    Prints the text in the given color if available
    If not, prints normally

    Options
     - "default", "grey", "red", "green", "yellow", "blue", "purple", "cyan", "white"
    '''
    def get_color_value(color : str):
        match color.lower():
            case "grey":
                return 30
            case "gray":
                return 30
            case "red":
                return 31
            case "green":
                return 32
            case "yellow":
                return 33
            case "blue":
                return 34
            case "purple":
                return 35
            case "cyan":
                return 36
            case "white":
                return 37

    if color not in ["grey", "red", "green", "yellow", "blue", "purple", "cyan", "white"]:
        return(text)
        return

    return(f'\x1b[1;{get_color_value(color)};40m{text}\x1b[0m')





# def print_format_table():
#     """
#     prints table of formatted text format options
#     """
#     for a in range(8):
#         for fg in range(30, 38):
#             s1 = ''
#             for bg in range(40, 48):
#                 format = ';'.join([str(a), str(fg), str(bg)])
#                 s1 += '\x1b[%sm %s \x1b[0m' % (format, format)
#             print(s1)

# print_format_table()


class Character():
    def __init__(self, name, type = "Enemy", portrait : list[str] | None = None, max_health = 10, gems = [], color = "white") -> None:
        self.portrait = portrait
        self.name = name
        self.type = type
        self.max_health = max_health
        self.health = max_health
        self.gems = gems
        self.remaining_turns_of_sheild = 0
        self.color = color
        self.status_effects = []

    def on_fire(self, boolean):
        if boolean and "🔥" not in self.status_effects:
            self.status_effects.append("🔥")
        elif "🔥" in self.status_effects:
            self.satus_effects.remove("🔥")

    def poisoned(self, boolean):
        if boolean and "🤢" not in self.status_effects:
            self.status_effects.append("🤢")
        elif "🤢" in self.status_effects:
            self.satus_effects.remove("🤢")

    def damage(self, amount):
        if self.remaining_turns_of_sheild > 0:
            self.remaining_turns_of_sheild -= 1
            return
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def border_portrait(character_portrait):
        output = [" ___________ "]
        for a in character_portrait:
            output.append(f"|{a} |")
        output.append(" ‾‾‾‾‾‾‾‾‾‾‾ ")
        return output


Miku = Character(
    portrait= [
            "  🟦🟦🟦  ",
            "🟦🟦⬜⬜🟦",
            "🟦⬛⬜⬛🟦",
            "🟦⬜⬜⬜🟦",
        ],
    name="Hatsune Miku",
    type="Healer",
    gems=[
        Gem(name="More Healing", color=Color.YELLOW),
        Gem(name="Bleed", color=Color.RED),
        Gem(name="Cast Sheild", color=Color.BLUE),
    ],
    max_health=7,
    color = "blue",
)


wizard = Character(
    portrait= [
            "    🟫    ",
            "  🟫🟫🟫  ",
            "🟫🟫🟫🟫🟫",
            "  🔳⬜🔳  ",
        ],
    name="Wizard",
    type="Damage",
    gems=[
        Gem(name="Whack them", color=Color.YELLOW),
        Gem(name="Bleed", color=Color.RED),
        Gem(name="Cast Sheild", color=Color.BLUE),
    ],
    max_health=7,
    color="purple",
)

def print_character_info(character : Character, display_size=45):
    '''
    display_size
     - 35 is smallest size for 10 health
     - 45 is smallest size for 15 health
    '''
    a = Character.border_portrait(character.portrait)
    for i in range(len(a)):
        if i == 0:
            print(a[i] + "▁" * (display_size-1))
        elif i == len(a)-1:
            print(a[i] + "▔" * (display_size-1)) # ‾
        else:
            text = ""
            text_len = 0
            if i == 1:
                text = "- " + character.name + " -"
                # text_len -= len(colorize("", color="blue"))-1
            elif i == 2:
                text = character.type
            elif i == 3:
                text = "Health: "
                if character.remaining_turns_of_sheild < 1:
                    text += "|" + "🟩" * character.health + "⬛" * (character.max_health-character.health) + " |"
                else:
                    text += "🟦" * character.max_health + f" x{character.remaining_turns_of_sheild}"
                text_len += character.max_health
            elif i == 4:
                text = "Equiped:"
                for gem in character.gems:
                    text += gem.color.base + " "
                text_len += len(character.gems)
            text_len += len(text)
            print(a[i] + " " + text + " " * ((display_size-2) - text_len) + "|")



# clear_screen()
# print_character_info(Miku)
# print_character_info(wizard)



def mini_character_info(characters : Character, reverse : bool = False):
    output = []

    def get_longest_name():
        longest_name = -1
        for character in characters:
            if len(character.name) > longest_name:
                longest_name = len(character.name)
        return longest_name + 6

    def get_longest_max_health():
        longest_max_health = -1
        for character in characters:
            if character.max_health > longest_max_health:
                longest_max_health = character.max_health
        return longest_max_health

    for character in characters:
        name = character.name # if reverse else colorize(character.name, color=character.color)
        name_text = f" {name} "
        for effect in character.status_effects:
            name_text += f"{effect}"
        name_text += " " * (get_longest_name()  - 2*len(character.status_effects) - len(character.name))
        health_text = colorize("█" * character.health, "green") + colorize("█" * (character.max_health-character.health), "grey")
        health_text += " " * (get_longest_max_health() - true_len(health_text))
        if reverse:
            output.append([
                health_text,
                name_text
            ])
        else:
            output.append([
                name_text,
                health_text
            ])

    return output

wizard.health = 1
Miku.max_health = 15
Miku.health = 15
# Miku.on_fire(True)
# Miku.poisoned(True)


def underline(text):
    return f'\x1b[4m{text}\x1b[0m'

def get_mini_character_info(characters : list[Character], text : str, selected = -1, reversed : bool = False) -> TextLayer:

    def get_longest_line():
        longest_line = -1
        for a in output:
            if true_len(a) > longest_line:
                longest_line = true_len(a) + a.count("🟩") + a.count("⬛")
        return longest_line-2


    output = mini_character_info(characters=characters, reverse=reversed)


    for i in range(len(output)):
        new_line = ""
        for b in output[i]:
            new_line += "⏐" + b
        new_line += "⏐"
        output[i] = new_line

    longest_line = get_longest_line()

    output.insert(0, " " + "▁" + underline(text) + "▁" * (longest_line - true_len(text) - 1) + " ")
    output.append(" " + "▔" * longest_line + " ") # ‾
    # output.insert(0, underline(" " * 4 + text + " " * (longest_line - len(text) - 2)))
    # last_line = output[len(output)-1]
    # output[len(output)-1] = last_line[0:1] + underline(last_line[1:len(last_line)-1]) + last_line[len(last_line)-1:]

    selected += 1
    if selected > 0 and selected < len(output):
        output[selected] += " <"


    # for a in output:
    #     print(a)

    return TextLayer(width=longest_line, text_array=output)



enemy1 = Character(
    name="Enemy 1",
    max_health=10,
)

from enum import Enum

class Color(Enum):
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
    OFFWHITE = (215, 215, 215)
    BLACK = (0, 0, 0)
    YELLOW = (255, 255, 0)
    PINK = (255, 25, 150)
    PURPLE = (255, 0, 255)
    BROWN = (160, 80, 45)


class ColorStr:
    def __init__(self, *starting_text) -> None:
        self.internal_list = [*starting_text]
        pass

    def __str__(self) -> str:
        output = ""
        for element in self.internal_list:
            if type(element) == str:
                output += element
            elif type(element) == list or type(element) == tuple:
                if len(element) == 2:
                    if type(element[1]) == list or type(element[1]) == tuple:
                        r, g, b = element[1]
                    elif type(element[1]) == str:
                        for color in list(Color):
                            if element[1].upper() == color.name:
                                r, g, b = color.value
                                break
                    elif type(element[1]) == Color:
                        r, g, b = element[1].value
                    else:
                        raise Exception("Must give a color")
                if len(element) == 4:
                    r = element[1]
                    g = element[2]
                    b = element[3]
                output += f"\u001b[38;2;{r};{g};{b}m" + element[0] + "\x1b[0m"
        return output

    def __add__(self, other) -> None:
        if type(other) == DisplayPixel:
            other = other.to_colorstr()
        if type(other) == str or type(other) == list or type(other) == tuple:
            self.internal_list.append(other)
            return self
        if type(other) == ColorStr:
            for segment in other.internal_list:
                self.internal_list.append(segment)
            return self
        raise Exception(f"Cannot add a ColorStr to an object of type {type(other)}")

    def __radd__(self, other) -> None:
        if type(other) == str or type(other) == list or type(other) == tuple:
            self.internal_list.insert(0, other)
            return self
        if type(other) == ColorStr:
            other.internal_list.reverse()
            for segment in other.internal_list:
                self.internal_list.insert(0, segment)
            return self
        raise Exception(f"Cannot add an object of type {type(other)} to a ColorStr")

    def __len__(self) -> int:
        length = 0
        for a in self.internal_list:
            if type(a) == str:
                length += len(a)
            else:
                length += len(a[0])
        return length

    def replace(self, target, new):

        def get_replacement(item, *surroundings):
            output = []

            def add(item):
                if len(surroundings) > 0:
                    output.append((item, *surroundings))
                else:
                    output.append(item)

            # item is string
            if target not in item:
                add(item)
                return output
            # target in item
            elif type(new) == str:
                # item and new are strings
                add(item.replace(target, new))
                return output
            else:
                # item is string, new is not a string
                while target in item:
                    index = item.index(target)
                    everything_before_target = item[:index]
                    if everything_before_target != "":
                        add(everything_before_target)
                    item = item[index:].rstrip(target)
                    output.append(new)
                add(item)

            return output

        output = []
        for i in range(len(self.internal_list)):
            item = self.internal_list[i]
            if item == target:
                output.append(target)
                continue
            if type(item) == str:
                output += get_replacement(item)
            else:
                extra = []
                for i in range(len(item)):
                    if i != 0:
                        extra.append(item[i])
                output += get_replacement(item[0], *extra)
        self.internal_list = output
        return self



            # self.internal_list[i][0] = self.internal_list[i][0].replace(target, new)
            # output.append(self.internal_list[i][0])
            # continue





# # Miku.on_fire(True)
# # Miku.poisoned(True)




from math import floor, ceil



screen_width = 100
screen_height = 20


# clear_screen()

# # print(f"\u001b[38;2;{255};{255};{0}m")
# text = "HI"
# print("▁" * (floor((screen_width-len(text))/2)) + text + "▁" * (ceil((screen_width-len(text))/2)))
# health = 13
# total_health = 26
# print(" " * floor((screen_width-total_health)/2) + colorize("█" * (health), "green") + colorize("█" * (health), "grey"))
# print("▔" * screen_width)

# for i in range(screen_height-3):
#     h = ColorStr()
#     for _ in range(screen_width):
#         # v = int(i/3)
#         # selected = 0 if randint(0, v) == 0 else 1 if randint(0, v) == 0 else 2 if randint(0, v) == 0 else 3 if randint(0, v) == 0 else 4
#         h += ("░▒▓█"[3:4], (0, 0, 255))
#     print(h)
# print(colorize("█" * screen_width, "green"))


# def print_characters():
#     heros = get_mini_character_info(characters=[Miku, wizard], text = "Team", selected=0, reversed=True)
#     villians = get_mini_character_info(characters=[enemy1], text = "Enemies")
#     villians.next_to(heros, fill=screen_width)
#     print(villians)


# print_characters()
# from time import sleep
# sleep(1)



class DisplayPixel:
    RIGHT = "RIGHT"
    LEFT = "LEFT"
    FULL = "FULL"
    HALF = "HALF"

    BLANK = "  "

    def __init__(self, count = 1, color = Color.WHITE, pixel_type = "FULL") -> None:
        self.pixel_type = pixel_type
        self.count = count
        if type(color) != list:
            self.colors = [color]
        else:
            self.colors = color

    def type_to_str(type):
        if type == DisplayPixel.RIGHT:
            return " █"
        if type == DisplayPixel.LEFT:
            return "█ "
        if type == DisplayPixel.FULL:
            return "██"
        if type == DisplayPixel.HALF:
            return "█"


    def __add__(self, other):
        if type(other) == DisplayPixel and self.colors == other.colors and self.pixel_type == other.pixel_type:
            self.count += other.count
            return self
        return self.to_colorstr() + other

    def __radd__(self, other):
        if type(other) == DisplayPixel and self.colors == other.colors and self.pixel_type == other.pixel_type:
            self.count += other.count
            return self
        return other + self.to_colorstr()

    def to_colorstr(self):
        pixel = DisplayPixel.type_to_str(self.pixel_type)
        output = "" if int(self.count) == self.count else ColorStr((DisplayPixel.type_to_str(DisplayPixel.HALF), self.colors[0]))
        if len(self.colors) == 1:
            output += ColorStr((pixel*int(self.count), self.colors[0]))
            return output
        else:
            output += ColorStr()
            if int(self.count) == self.count:
                self.colors.append(Color.WHITE)
            for i in range(int(self.count)):
                output += (pixel[0], self.colors[2*i])
                output += (pixel[1], self.colors[2*i + 1])
            return output

    def __str__(self) -> ColorStr:
        return str(self.to_colorstr())




def pixels(count : int = 1, color : Color | tuple | None = None):
    if type(count) != int and not str(count).endswith(".5"):
        raise Exception(f"count must be of type int or float ending in 0.5.\n Is of type {type(count)}")
    if type(color) != Color and type(color) != tuple and color != None:
        raise Exception(f"color must be of type Color, tuple or None.\n Is of type {type(count)}")

    if count < 0:
        return ""

    pixel = "██"
    if count == 0:
        count = 1
        pixel = "  "

    if not color:
        return pixel * count

    return ColorStr((pixel * count, color))




space = floor(screen_height * 2/3)


# for i in range(space):
#     i+=1
#     if i >= (space+2)/2:
#         i = (space+2)-i-1
#     thinness = space % 2
#     print("  " * int(((space+2)-(i*2))/2 - (1-thinness)) + pixels(count=i*2-thinness, color=Color.RED))


def magic_border(input : list):
    def get_magic(percent):
        r = randint(2 if percent < 50 else 1 if percent < 60 else 0, 3)
        return ColorStr(("▓▒░ "[r:r+1], Color.PURPLE)) if randint(0, 99) < percent else " "



    def get_row(length, percent):
        top = ""
        for _ in range(length):
            top += get_magic(percent)
        return top


    def border(input, percent):
        length = len(input[0])
        input.insert(0, get_row(length, percent))
        input.insert(0, get_row(length, percent-35))
        input.append(get_row(length, percent))
        input.append(get_row(length, percent-35))
        for i in range(len(input)):
            input[i] = get_magic(percent) + input[i] + get_magic(percent)
            input[i] = get_magic(percent-20) + input[i] + get_magic(percent-20)
            input[i] = get_magic(percent-40) + input[i] + get_magic(percent-40)
        return input

    for i in range(len(input)):
        r = randint(0, 2)
        pixel = "▒▓" if r == 0 else "▓▒" if r == 1 else "██"
        # input[i] = input[i].replace("  ", (pixel, Color.PURPLE))
        # .replace(" ", ColorStr((["█","▓"][1 if randint(0, 3) == 0 else 0], Color.PURPLE)))
    # return border(border(input, 75), 25)
    return border(input, 75)


def offestColor(color, count = None, by_pixels = True):
    if not count:
        r, g, b = color.value
        offest = randint(-3, 3)
        return (r+offest, g+offest, b+offest)
    if by_pixels:
        output = []
        for _ in range(count):
            output.append(offestColor(color))
            output.append(offestColor(color))
        return output
    return [offestColor(color) for _ in range(count)]


if __name__ == "__main__":

    pattern = [False, True, True, False, False, True, False, True, True]

    book_color = Color.OFFWHITE
    x, y, z = book_color.value

    book_width = 10
    book = [DisplayPixel(book_width, offestColor(book_color, book_width)) if a else DisplayPixel.BLANK + DisplayPixel(book_width-1, offestColor(book_color, (book_width-1))) for a in pattern]
    text = "Poison Blast"

    book[1] = DisplayPixel(1.5, offestColor(book_color, 3)) + f"\u001b[48;2;{x};{y};{z}m{ColorStr((text, Color.BLACK))}\u001b[0m" + DisplayPixel(((book_width-1.5)*2 - len(text))/2, book_color)

    book = magic_border(book)

    for a in book:
        print(a)
























# -----------------------------------

# TODO Average instead of sample

# from PIL import Image

# im = Image.open('C:\\Users\\jgill\\Downloads\\424f4ec43b4eca3d168b1c69cb383ac4.jpeg')
# pix = im.load()
# width, height = im.size

# shrink_factor = int(width/25)

# for i in range(int(height/shrink_factor)):
#     row = ""
#     for j in range(int(width/shrink_factor)+1):
#         x = j*shrink_factor # if j*shrink_factor <= width else width
#         y = i*shrink_factor # if i*shrink_factor <= height else height
#         if len(pix[x, y]) == 4:
#             r, g, b, a = pix[x, y]
#             value = round(a/250 * 4)
#             if value == 0:
#                 row += "  "
#             else:
#                 row += f"\u001b[38;2;{r};{g};{b}m" + " ░▒▓█"[value:value+1] + " ░▒▓█"[value:value+1]
#         else:
#             r, g, b = pix[x, y]
#             # r, g, b = (0, 0, 0)
#             # for sf1 in range(shrink_factor):
#             #     for sf2 in range(shrink_factor):
#             #         x_temp = x + sf1 if x + sf1 <= width else width
#             #         y_temp = y + sf2 if y + sf2 <= height else height
#             #         r_temp, g_temp, b_temp, = pix[x, y]
#             #         r += r_temp
#             #         g += g_temp
#             #         b += b_temp
#             # r, g, b = (r/shrink_factor, g/shrink_factor, b/shrink_factor)
#             row += f"\u001b[38;2;{r};{g};{b}m" + "██"

#     print(row)

# -----------------------------------
