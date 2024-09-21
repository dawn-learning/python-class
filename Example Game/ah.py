# Imports from existing packages
from math import ceil
from os import system
from enum import Enum
from time import sleep
from random import randint, choice

# Imports from my other files
from charms import *
from artwork import *
from status_effects import *
from tester import wait_for_character_input
from characters import *
import status_effects


pixel_only = '▀'
top_pixel_only = '\033[38;2;{};{};{}m▀'
bottom_pixel_only ='\033[48;2;{};{};{}m▀'
top_and_bottom_pixels = '\033[38;2;{};{};{}m\033[48;2;{};{};{}m▀'
character_and_pixel = "\033[38;2;{};{};{}m\033[48;2;{};{};{}m{}"
line_end = "\033[0m"

player_inventory = []

# player_inventory = [Win()]
# update_images(DEBUG=True)

class Screen:
    def __init__(self, layers = [], size_x : int | None = None, size_y : int | None = None) -> None:
        self.layers = layers
        self.size_x = size_x
        self.size_y = size_y

    def flatten(self):
        # Squashes layers into one Pixel Layer
        output_pixels = []

        # Get largest layer
        width = -1
        height = -1
        for layer in self.layers:
            layer_height = len(layer.pixel_array)
            if layer_height > height:
                height = layer_height
            if layer_height <= 0:
                continue
            layer_width = len(layer.pixel_array[0])
            if layer_width > width:
                width = layer_width
        if self.size_x and width < self.size_x:
            width = self.size_x
        if self.size_y and height < self.size_y:
            height = self.size_y

        # Find the correct pixel color for each spot on the screen
        for h in range(height):
            row = []
            for w in range(width):
                depth = 0
                pixel = None
                text = None
                # Finds the pixel value for each position on the screen, if value is None, the pixel on that layer is 
                #  assumed to be "clear" and moves down to find the pixel on the layer below it
                while depth < len(self.layers):
                    targeted_layer = self.layers[depth].pixel_array

                    # Applies the layer's internal offset
                    offest_h = h - self.layers[depth].screen_position_y
                    offset_w = w - self.layers[depth].screen_position_x

                    # Checks to see if position is within the layer's pixel value space
                    if offest_h < 0 or offest_h >= len(targeted_layer):
                        depth += 1
                        continue
                    if offset_w < 0 or offset_w >= len(targeted_layer[0]):
                        depth += 1
                        continue

                    targeted_pixel = targeted_layer[offest_h][offset_w]
                    # If there is an overlap of multiple TextPixels, takes only the top one
                    if type(targeted_pixel) == TextPixel and text != None:
                        targeted_pixel = targeted_pixel.top_pixel_color
                    # If pixel value at this position for this layer, adds to final image and moves on
                    if targeted_pixel != None:
                        if type(targeted_pixel) == TextPixel:
                            if targeted_pixel.top_pixel_color:
                                pixel = targeted_pixel
                                break
                            else:
                                text = targeted_pixel.character
                                depth += 1
                                continue
                        if not text:
                            pixel = targeted_pixel
                        else:
                            pixel = TextPixel(character=text, top_pixel_color=targeted_pixel)
                        break

                    # If layer's pixel value at position is None aka clear, moves down to next layer and repeats process
                    depth += 1
                if not pixel and text:
                    pixel = TextPixel(character=text, top_pixel_color=None)
                row.append(pixel)
            output_pixels.append(row)

        return output_pixels

    def __str__(self):
        # Prints the pixel layer
        return str(PixelLayer(pixels=self.flatten()))


class Layer:
    def __init__(self, x = 0, y = 0) -> None:
        self.screen_position_x = x
        self.screen_position_y = y
        pass

    def set_pos(self, x : int | None = None, y : int | None = None):
        '''Moves layer to new position. Can take X only, Y only, or both.\n\nReturns updated self.'''
        if x != None:
            if type(x) != int:
                raise Exception(f"x position must be an integer, was a {type(x)}")
            self.screen_position_x = x
        if y != None:
            if type(y) != int:
                raise Exception(f"y position must be an integer, was a {type(y)}")
            self.screen_position_y = y
        return self

    def update_pos(self, x : int | None = None, y : int | None = None):
        '''Moves layer to new position. Can take X only, Y only, or both.\n\nReturns updated self.'''
        if x != None:
            if type(x) != int:
                raise Exception(f"x position must be an integer, was a {type(x)}")
            self.screen_position_x += x
        if y != None:
            if type(y) != int:
                raise Exception(f"y position must be an integer, was a {type(y)}")
            self.screen_position_y += y
        return self

class PixelLayer(Layer):
    def __init__(self, pixels = [], x = 0, y = 0) -> None:
        super().__init__(x, y)
        self.pixel_array = pixels

    def get_pixel_pair(pixel_array, first_line, second_line, element_index):
        if second_line == None:
            top = pixel_array[first_line][element_index]

            top_character = None
            if type(top) == TextPixel:
                top_character = top.character
                top = top.top_pixel_color

            if not top:
                top = Color.BLACK
            if type(top) == Color:
                top = top.value

            if top_character:
                # Text color is black on light colors and white on dark colors
                r, g, b, = top
                if r + g + b > (255 + 255 + 255)/2:
                    text_color = (0, 0, 0)
                else:
                    text_color = (255, 255, 255)

                return character_and_pixel.format(*text_color, *top, top_character)
                # previous_top = None
                # previous_bottom = None
            else:
                # if previous_top == top:
                #     line += pixel_only
                # else:
                return top_pixel_only.format(*top)
                    # previous_top = top
        else:
            top = pixel_array[first_line][element_index]
            top_character = None

            try:
                bottom = pixel_array[second_line][element_index]
            except:
                bottom = None

            if type(top) == TextPixel and type(bottom) == TextPixel:
                raise Exception("OVERLAPPING TEXT")

            if type(top) == TextPixel:
                top_character = top.character
                top = top.top_pixel_color

            if type(bottom) == TextPixel:
                top_character = bottom.character
                bottom = bottom.top_pixel_color

            if not top:
                top = Color.BLACK
            if type(top) == Color:
                top = top.value
            
            if not bottom:
                bottom = Color.BLACK
            if type(bottom) == Color:
                bottom = bottom.value

            if top_character:
                r = int((top[0] + bottom[0])/2)
                g = int((top[1] + bottom[1])/2)
                b = int((top[2] + bottom[2])/2)

                # Text color is black on light colors and white on dark colors
                if r + g + b > (255 + 255 + 255)/2:
                    text_color = (0, 0, 0)
                else:
                    text_color = (255, 255, 255)

                return character_and_pixel.format(*text_color, r, g, b, top_character)
                # previous_top = None
                # previous_bottom = None
            else:
                # if previous_top == top and previous_bottom == bottom:
                #     line += pixel_only
                # elif previous_top == top:
                #     line += bottom_pixel_only.format(*bottom)
                #     previous_bottom = bottom
                # elif previous_bottom == bottom:
                #     line += top_pixel_only.format(*top)
                #     previous_top = top
                # else:
                return top_and_bottom_pixels.format(*top, *bottom)
                    # previous_top = top
                    # previous_bottom = bottom


    def __str__(self):
        pixels = self.pixel_array
        output = ""
        for line_pair in range(ceil(len(pixels) / 2)):
            line = ""
            first = line_pair*2
            second = line_pair*2+1

            # previous_top = None
            # previous_bottom = None

            for column in range(len(pixels[first])):
                line += PixelLayer.get_pixel_pair(self.pixel_array, first, None if second >= len(pixels) else second, column)

            output += line + line_end + "\n"
        return output[:len(output)-1]

    def __len__(self):
        return len(self.pixel_array)

class TextPixel():
    def __init__(self, character : str, top_pixel_color : Color | list | tuple | None = None) -> None:
        self.character = character
        self.top_pixel_color = top_pixel_color

    def __len__(self):
        return 1

class TextLayer(Layer):
    def __init__(self, text = "", background_color = None, x = 0, y = 0) -> None:
        super().__init__(x, y)
        self.pixel_array = []
        for char in text:
            self.pixel_array.append(TextPixel(character=char, top_pixel_color=background_color))
        self.pixel_array = [self.pixel_array]





# s = Screen(layers=[pixels, l])

# all_contents = []
# for row in range(35):
#     contents = []
#     for element in range(35):
#         selected = None
#         for a in s.layers:
#             if row-a.screen_position_x < 0 or element-a.screen_position_y < 0:
#                 continue
#             try:
#                 if a.pixel_array[row-a.screen_position_x][element-a.screen_position_y] != None:
#                     selected = a.pixel_array[row-a.screen_position_x][element-a.screen_position_y]
#                     break
#             except:
#                 pass
#         contents.append(selected)
#     all_contents.append(contents)

# print(PixelLayer(pixels=all_contents))




def center(color_list : list[Color], count : int):
    sides = count - len(color_list)
    side = sides // 2
    output = [None for _ in range(side)]
    output += color_list
    output += [None for _ in range(side)]
    return output






def wrap_map(map):
    '''Wraps the given map in a fancy border.\n\nNote: Map must be of at least 9x9.'''

    # Returns a reversed version of the aray without reversing the original
    def temp_reverse_array(array):
        return [a for a in array.__reversed__()]

    # Border pattern
    tl1 = [Color.BROWN, Color.BROWN, None, Color.BROWN, None, Color.BROWN, Color.BROWN]
    tl2 = [Color.BROWN, Color.BROWN, None, None, Color.BROWN, None, None,]
    tl3 = [None, None, Color.BROWN, Color.BROWN, Color.BROWN, Color.BROWN, Color.BROWN]
    tl4 = [Color.BROWN, None, Color.BROWN]
    tl5 = [None, Color.BROWN, Color.BROWN]

    # Adds the border to the given map
    length = len(map[0])
    return [
        tl1 + (Color.BROWN * (length - 8)) + temp_reverse_array(tl1),
        tl2 + (Color.BROWN * (length - 8)) + temp_reverse_array(tl2),
        tl3 + (Color.BROWN * (length - 8)) + temp_reverse_array(tl3),
        tl4 + map[0] + temp_reverse_array(tl4),
        tl5 + map[1] + temp_reverse_array(tl5),
        tl4 + map[2] + temp_reverse_array(tl4),
        tl4 + map[3] + temp_reverse_array(tl4),
        *[Color.BROWN * 3  + map[i + 4] + Color.BROWN * 3 for i in range(len(map)-8)],
        tl4 + map[len(map)-4] + temp_reverse_array(tl4),
        tl4 + map[len(map)-3] + temp_reverse_array(tl4),
        tl5 + map[len(map)-2] + temp_reverse_array(tl5),
        tl4 + map[len(map)-1] + temp_reverse_array(tl4),
        tl3 + (Color.BROWN * (length - 8)) + temp_reverse_array(tl3),
        tl2 + (Color.BROWN * (length - 8)) + temp_reverse_array(tl2),
        tl1 + (Color.BROWN * (length - 8)) + temp_reverse_array(tl1),
    ]



def clear_screen():
    system("cls | clear")

def get_health_bar(health, max_health):
    # Deals with negative numbers
    if health < 0:
        health = 0

    # Deals with overhealth
    overhealth = 0
    if health > max_health:
        overhealth = health - max_health
        health = max_health

    # Generates the display
    pairs = int(health/2)
    display = [[Color.GREEN, (0, 240, 0)] * pairs + Color.GREEN * (health - pairs * 2) + Color.GREY * (max_health-health) + Color.YELLOW * overhealth]
    return PixelLayer(pixels= display + display)


class character(Enum):
    SNAKE = "Snake"
    SCORPION = "Scorpion"
    DRAGON = "Dragon"

class characters():
    def to_subclass(potential_character):
        if potential_character == character.SNAKE:
            return Snake()
        elif potential_character == character.SCORPION:
            return Scorpion()
        elif potential_character == character.DRAGON:
            return Dragon()

    def _shrink_character(character):
        smaller_version = []
        for i in range(int(len(character)/2)):
            new_row = []
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
                new_row.append(max)
            smaller_version.append(new_row)
        return smaller_version

    def scaleUp(self, scale):
        scaled_up_artwork = []
        for row in self.art:
            for _ in range(scale):
                new_row = []
                for element in row:
                    for _ in range(scale):
                        new_row.append(element)
                scaled_up_artwork.append(new_row)
        return scaled_up_artwork

    def is_a_character(obj):
        return True

class Snake(characters):
    def __init__(self) -> None:
            self.type = "Fire"
            self.art = [
            [None,None,None,None,Color.RED,Color.RED,None,None,Color.RED,Color.RED,None,None,None,None,],
            [None,None,None,None,Color.RED,Color.RED,None,None,Color.RED,Color.RED,None,None,None,None,],
            [None,None,Color.RED,Color.RED,Color.RED,Color.RED,Color.RED,Color.RED,Color.RED,Color.RED,Color.RED,Color.RED,None,None,],
            [None,Color.RED,Color.RED,Color.RED,Color.RED,Color.RED,Color.RED,Color.RED,Color.RED,Color.RED,Color.RED,Color.RED,Color.RED,None,],
            [Color.RED,Color.RED,Color.RED,Color.RED,None,Color.RED,Color.RED,Color.RED,Color.RED,Color.RED,None,None,Color.RED,Color.RED,],
            [Color.RED,Color.RED,Color.RED,Color.RED,None,None,Color.RED,Color.RED,Color.RED,Color.RED,None,None,Color.RED,Color.RED,],
            [Color.RED,Color.RED,Color.RED,Color.RED,None,None,None,None,None,Color.RED,Color.RED,Color.RED,Color.RED,Color.RED,],
            [Color.RED,Color.RED,Color.RED,Color.RED,None,None,None,None,None,None,Color.RED,Color.RED,Color.RED,None,],
            [Color.RED,Color.RED,Color.RED,Color.RED,Color.RED,None,None,None,None,None,None,None,None,None,],
            [Color.RED,Color.RED,Color.RED,Color.RED,Color.RED,Color.RED,Color.RED,None,None,None,None,None,None,None,],
            [None,Color.RED,Color.RED,Color.RED,Color.RED,Color.RED,Color.RED,Color.RED,Color.RED,None,None,None,None,None,],
            [None,None,Color.RED,Color.RED,Color.RED,Color.RED,Color.RED,Color.RED,Color.RED,Color.RED,Color.RED,None,None,None,],
            [None,None,None,None,Color.RED,Color.RED,Color.RED,Color.RED,Color.RED,Color.RED,Color.RED,Color.RED,Color.RED,None,],
            [None,Color.RED,Color.RED,Color.RED,Color.RED,Color.RED,Color.RED,Color.RED,Color.RED,Color.RED,Color.RED,Color.RED,Color.RED,Color.RED,],
        ]

    def animation(self, step):
        step = 13-step
        new_art = self.art.copy()
        for _ in range(step):
            new_art.insert(0, [None for _ in len(new_art[0])])
        for _ in range(step):
            new_art.pop()
        return new_art

class Scorpion(characters):
    def __init__(self) -> None:
        self.type = "Earth"
        self.art = [
            [None,None,Color.BROWN,Color.BROWN,Color.BROWN,Color.BROWN,Color.BROWN,Color.BROWN,None,None,None,None,None,None],
            [None,Color.BROWN,Color.BROWN,Color.BROWN,Color.BROWN,Color.BROWN,Color.BROWN,Color.BROWN,Color.BROWN,None,None,None,None,None],
            [Color.BROWN,Color.BROWN,Color.BROWN,Color.BROWN,None,None,None,Color.BROWN,Color.BROWN,Color.BROWN,None,None,None,None],
            [Color.BROWN,Color.BROWN,Color.BROWN,None,None,None,None,None,Color.BROWN,Color.BROWN,None,None,None,None],
            [Color.BROWN,Color.BROWN,None,None,None,None,None,None,None,None,None,None,None,None],
            [Color.BROWN,Color.BROWN,None,None,None,None,None,None,None,None,None,None,None,None],
            [Color.BROWN,Color.BROWN,Color.BROWN,Color.BROWN,Color.BROWN,Color.BROWN,None,None,None,None,None,None,None,None],
            [Color.BROWN,Color.BROWN,Color.BROWN,Color.BROWN,Color.BROWN,Color.BROWN,None,None,None,None,None,None,None,None],
            [None,None,Color.BROWN,Color.BROWN,Color.BROWN,Color.BROWN,Color.BROWN,Color.BROWN,Color.BROWN,Color.BROWN,None,None,None,None],
            [None,None,Color.BROWN,Color.BROWN,Color.BROWN,Color.BROWN,Color.BROWN,Color.BROWN,Color.BROWN,Color.BROWN,None,None,None,None],
            [Color.BROWN,Color.BROWN,None,None,Color.BROWN,Color.BROWN,Color.BROWN,Color.BROWN,None,None,Color.BROWN,Color.BROWN,Color.BROWN,Color.BROWN],
            [Color.BROWN,Color.BROWN,None,None,Color.BROWN,Color.BROWN,Color.BROWN,Color.BROWN,None,None,Color.BROWN,Color.BROWN,Color.BROWN,Color.BROWN],
            [Color.BROWN,Color.BROWN,None,None,Color.BROWN,Color.BROWN,None,None,Color.BROWN,Color.BROWN,Color.BROWN,Color.BROWN,None,None],
            [Color.BROWN,Color.BROWN,None,None,Color.BROWN,Color.BROWN,None,None,Color.BROWN,Color.BROWN,Color.BROWN,Color.BROWN,None,None],
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
            [None,None,None,Color.BLUE,Color.BLUE,Color.BLUE,None,None,None,None,None,None,None,None],
            [None,None,None,None,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,None,None,Color.BLUE,Color.BLUE,None,None],
            [None,None,None,None,None,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,None,None,Color.BLUE,Color.BLUE],
            [None,None,None,None,None,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,None,None,Color.BLUE,Color.BLUE],
            [None,None,None,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE],
            [None,None,None,None,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,None,None,None],
            [None,None,None,None,None,None,Color.BLUE,Color.BLUE,Color.BLUE,None,None,None,None,None],
            [None,None,None,None,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,None,None,None,None],
            [None,None,None,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,None],
            [None,None,None,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,None,None],
            [Color.BLUE,None,None,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,None,None,None,None],
            [Color.BLUE,Color.BLUE,None,None,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,None,None,None,None],
            [None,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,None,None,None],
            [None,None,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,Color.BLUE,None,None,Color.BLUE,Color.BLUE,Color.BLUE,None,None],
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
                spot = randint(0, len(self.art[i])-1)
                # print("before", new_art[i], spot)
                new_art[i] = new_art[i][0 : spot] + "🤍" + new_art[i][spot+1:]
                # print("after ", new_art[i])
        return new_art
        # return []






def get_character_display(basic_character : BasicCharacter, selected : bool):
    def get_offset(obj):
        obj_len = len(obj) if type(obj) != int else obj
        return int((basic_character.width() - obj_len)/2)
    arrow_offset = 3 if selected else 0
    output = [
        PixelLayer(pixels = basic_character.artwork, x = get_offset(basic_character.artwork[0]), y=arrow_offset),
        TextLayer(basic_character.name, x = get_offset(basic_character.name), y = len(basic_character.artwork) + 2 + arrow_offset), 
        get_health_bar(health=basic_character.current_health, max_health=basic_character.stats.max_health).set_pos(y=2 + len(basic_character.artwork) + 2 + arrow_offset, x = get_offset(basic_character.stats.max_health)),
    ]
    if selected:
        arrow = [
            [Color.BROWN, None, None, None, Color.BROWN],
            [None, Color.BROWN, None, Color.BROWN, None],
            [None, None, Color.BROWN, None, None],
        ]
        return [PixelLayer(pixels = arrow, x = get_offset(arrow[0]))] + output
    return output



screen_width = 83
screen_height = 58
background_layer = PixelLayer(pixels=[[(10, 10, 10) for _ in range(screen_width)] for _ in range(screen_height + 8)])


# villian = BasicCharacter(name="villian", current_health=20, max_health=20, artwork=[], base_healing=2)
# hero = BasicCharacter(name="hero", current_health=20, max_health=20, artwork=[], character_type="Ally", base_healing=2)
# hero.outgoing_status_effects = [StatusEffect(name = "Burn", action = burn, duration = 3, level = 2), None, None, None, None]




def get_character_of_type(character_type : str, turn_counter : list[BasicCharacter]) -> BasicCharacter | None:
    for a in turn_counter:
        if a.character_type == character_type and a.current_health > 0:
            return a
    return None


def get_cumulative_healths(turn_counter):
    '''returns (total_hero_health, total_enemy_health)'''
    total_hero_health = 0
    total_enemy_health = 0
    for a in turn_counter:
        if a.character_type == "Ally":
            total_hero_health += a.current_health
        else:
            total_enemy_health += a.current_health
    return (total_hero_health, total_enemy_health)

def both_sides_are_standing(turn_counter):
    total_hero_health, total_enemy_health = get_cumulative_healths(turn_counter)
    return (total_hero_health > 0) and (total_enemy_health > 0)

def get_locations_of_characters_of_type(character_type : str, turn_counter : list[BasicCharacter]):
    output = []
    for i in range(len(turn_counter)):
        if turn_counter[i].character_type == character_type:
            output.append(i)
    return output

def get_i_from_user_from_list_of_options(options : list):
    layers=[]
    for i in range(len(options)):
        # print(f"{i+1} {options[i]}")
        layers += [
            TextLayer(options[i], x = 1 + 11 * i, y = 2),
            TextLayer(str(i+1), x=10-2 + 11 * i, y=8-3),
            PixelLayer(pixels=[
                [None for _ in range(10)],
                [None] + Color.BROWN * 8 + [None],
                [Color.BROWN] + [None for _ in range(8)] + [Color.BROWN],
                [Color.BROWN] + [None for _ in range(8)] + [Color.BROWN],
                [Color.BROWN] + [None for _ in range(8)] + [Color.BROWN],
                [Color.BROWN] + [None for _ in range(8)] + [Color.BROWN],
                [None] + Color.BROWN * 8 + [None],
                [None for _ in range(10)],
            ], x = 11 * i),
        ]
    display(Screen(layers, size_x = 25), height_override=4)
    while True:
        user_input = wait_for_character_input()
        try:
            user_input = int(user_input)-1
            if user_input < 0 or user_input >= len(options):
                continue
        except:
            # print("Please input a number")
            continue
        return options[user_input]


def get_box(height : int = 5, width : int | None = None, id : int = 1):
    if type(height) != int:
        raise Exception(f"size must be an int, size is a {type(height)}")
    if type(id) != int:
        raise Exception(f"count must be an int, size is a {type(id)}")
    
    if width == None:
        width = screen_width
    else:
        width += 4

    return PixelLayer(pixels=[
        [None, None] + Color.BROWN * (width-4) + [None, None],
        *[[None, Color.BROWN] + [None for _ in range(width-4)] + [Color.BROWN, None] for _ in range(height)],
        [None, None] + Color.BROWN * (width-4) + [None, None],
    ], y=screen_height-(2 + height + 1) * id)





def reverse_artwork(artwork : list[list]):
    return [[a for a in line.__reversed__()] for line in artwork]










def get_chat(characters : list[BasicCharacter], text : str, continue_text : str):
    text = text.splitlines()
    layers = [
        PixelLayer(pixels=reverse_artwork(characters[0].artwork), x = 10, y = 20),
        *[PixelLayer(pixels=characters[i+1].artwork, x=i * 10 + 50, y= 20) for i in range(len(characters[1:]))],
        *[TextLayer(text[i], y=screen_height - 12 + i*2, x=3) for i in range(len(text))],
        get_box(height=11),
        background_layer,
    ]
    if continue_text:
        layers.insert(0, TextLayer(continue_text, y =screen_height-4, x =screen_width-2-len(continue_text)))

    return Screen(layers=layers)

def get_options(characters : list[BasicCharacter], options : list[str]):
    layers = [PixelLayer(pixels=reverse_artwork(characters[0].artwork), x = 10, y = 20)]
    layers += [PixelLayer(pixels=characters[i+1].artwork, x=i * 10 + 50, y= 20) for i in range(len(characters[1:]))]
    temp_options = options.copy()
    temp_options.reverse()
    for i in range(len(temp_options)):
        layers.append(TextLayer(temp_options[i], y=screen_height-5 - 7*i, x= 3))
        layers.append(TextLayer(str(len(temp_options)-i), y=screen_height-4 - 7*i, x=screen_width-3))
        layers.append(get_box(height=4, id=i+1))
    layers.append(background_layer)
    return Screen(layers=layers)

class Area:
    def __init__(self, starting_x, ending_x, starting_y, ending_y) -> None:
        self.starting_x = starting_x
        self.ending_x = ending_x
        self.starting_y = starting_y
        self.ending_y = ending_y

    def in_area(self, x, y):
        return (x >= self.starting_x and x <= self.ending_x) and (y >= self.starting_y and y <= self.ending_y)


def create_battle_screen(enemies : list[BasicCharacter], heros : list[BasicCharacter], selected_character : int | None = None):
    layers=[]
    enemies_total_width = 0
    for i in range(len(enemies)):
        enemy = enemies[i]
        selected_offest = 3 if (i == selected_character) else 0
        for a in [x.update_pos(x = enemies_total_width, y=screen_height-enemy.height()-2*i-selected_offest) for x in get_character_display(enemy, selected = (i == selected_character) if selected_character != None else None)]:
            layers.append(a)
        enemies_total_width += enemy.width() + 1
    hero_total_width = 0
    for i in range(len(heros)):
        hero = heros[i]
        selected_offest = 3 if (i + len(enemies) == selected_character) else 0
        hero_total_width += hero.width() + 1
        for a in [x.update_pos(x = screen_width-hero_total_width, y=screen_height-hero.height()-2*i-selected_offest) for x in get_character_display(hero, selected = (i + len(enemies) == selected_character) if selected_character != None else None)]:
            layers.append(a)
    layers.append(background_layer)
    return Screen(layers)

def find_pos_in_list(enemies, heros, turn_counter, options, selected):
    all_list = [*enemies, *heros]
    for i in range(len(all_list)):
        # print(f"checking {all_list[i]} vs {turn_counter[options[selected]]} is {all_list[i] == turn_counter[options[selected]]}")
        if all_list[i] == turn_counter[options[selected]]:
            return i

def get_target(enemies, heros, turn_counter, options, heros_or_villians) -> BasicCharacter | None:
    selected = 0
    character_options = heros if heros_or_villians == "Heros" else enemies
    while True:
        pos = selected + len(enemies) if heros_or_villians == "Heros" else selected
        display(create_battle_screen(enemies=enemies, heros=heros, selected_character=pos))
        user_input = wait_for_character_input()
        if user_input == "RIGHT":
            if selected < len(character_options)-1:
                selected += 1
        elif user_input == "LEFT":
            if selected > 0:
                selected -= 1
        elif user_input == "\\n":
            # print(len(character_options), heros_or_villians, heros_or_villians == "Heros")
            return character_options[selected]

def run_battle_engine(heros : list[BasicCharacter], enemies : list[BasicCharacter]) -> bool:
    '''Returns True if heros won, returns False if enemies won'''
    DEBUG = False

    # Defines the turn order
    turn_counter = [*heros, *enemies]

    if DEBUG: print(f"both_sides_are_standing(turn_counter) is {both_sides_are_standing(turn_counter)}")
    while both_sides_are_standing(turn_counter):
        display(create_battle_screen(enemies=enemies, heros=heros))

        # Get the character whose turn it is
        current_character = turn_counter.pop(0)
        turn_counter.append(current_character)
        if DEBUG: print("-" * 10)
        if DEBUG: print(f"{current_character.name}'s turn: ", end="")

        # Moves on if selected character is out of the fight
        if current_character.current_health <= 0:
            if DEBUG: print(f"{current_character.name} is knocked out")
            continue

        # Determines what their next action is
        if current_character.character_type == "Enemy":
            # Enemies come preloaded with a list of actions they loop over in order
            action = current_character.get_next_default_action()
        else:
            if DEBUG: print("What do?")
            action = get_i_from_user_from_list_of_options(options = ["Attack", "Heal"])
        if DEBUG: print(f"{action}ing")

        # Has them take their action
        if action == "Attack":
            raw_damage, applying_status_effect = current_character.attack()
            target_type = "Ally" if current_character.character_type == "Enemy" else "Enemy"

            if current_character.character_type == "Enemy":
                # Defaults the next character in the turn order
                affected : BasicCharacter | None = get_character_of_type(target_type, turn_counter)
            else:
                # user must choose a target to attack
                options = get_locations_of_characters_of_type("Enemy", turn_counter)
                if len(options) == 0:
                    # If can't attack someone, moves on
                    continue
                elif len(options) == 1:
                    # Defaults to only option if one option
                    affected : BasicCharacter | None = turn_counter[options[0]]
                else:
                    if DEBUG: print("Who?")
                    # Ask for target from user
                    affected : BasicCharacter | None = get_target(enemies, heros, turn_counter, options, "Villians")
                if DEBUG: print(affected.name)

            if affected:
                if DEBUG: print(f"Attacked {affected.name} for {raw_damage} damage")
                affected.take_damage(raw_damage)
                if applying_status_effect:
                    if DEBUG: print(f"Applied status effect {str(applying_status_effect.name)} to {affected.name}")
                    if type(applying_status_effect) != StatusEffect:
                        raise Exception(f"Should be a StatusEffect, is a {type(applying_status_effect)}")
                    affected.current_status_effects.append(applying_status_effect)

        elif action == "Heal":
            if current_character.character_type == "Enemy":
                target = current_character.get_next_in_healing_pattern()
                if DEBUG: print(f"Healing {target}")
                if target == "Self":
                    current_character.take_healing(current_character.base_healing)
                elif target == "All":
                    for char in turn_counter:
                        if char.character_type == current_character.character_type:
                            char.take_healing(current_character.base_healing)
                elif target == "Random":
                    target = get_character_of_type(current_character.character_type, turn_counter)
                    target.take_healing(current_character.base_healing)
                else:
                    raise Exception(f"healing pattern has something wrong, namely: {target}")
            else:
                # Asks for target from user
                options = get_locations_of_characters_of_type("Ally", turn_counter)
                if len(options) == 0:
                    continue
                elif len(options) == 1:
                    to_be_healed = turn_counter[options[0]]
                else:
                    # to_be_healed = turn_counter[get_i_from_user_from_list_of_options(options)]
                    to_be_healed : BasicCharacter | None = get_target(enemies, heros, turn_counter, options, "Heros")
                to_be_healed.take_healing(current_character.base_healing)

        current_character.end_turn()

        # Show changes
        if DEBUG:
            for a in turn_counter:
                print(a.name, a.current_health)
    if DEBUG: print("-" * 10)
    display(create_battle_screen(enemies=enemies, heros=heros))
    sleep(0.5)

    heros_cumulative_health, enemies_cumulative_health = get_cumulative_healths(turn_counter)
    return (heros_cumulative_health > enemies_cumulative_health)






def get_snake_enemy(scale = 1):
    return BasicCharacter(
        name = "Snake",
        stats= CharacterStats(
            max_health=10 if scale == 1 else 45,
            damage=4 if scale == 1 else 7,
        ),
        artwork=Snake().scaleUp(scale),
        abilities=[Whack()],
    )

def get_dragon_enemy(scale = 1):
    return BasicCharacter(
        name="Dragon",
        stats= CharacterStats(
            max_health=8 if scale == 1 else 35,
            damage=3 if scale == 1 else 6,
        ),
        artwork=Dragon().scaleUp(scale),
        abilities=[Whack()],
    )

def get_scorpion_enemy(scale = 1):
    output = BasicCharacter(
        name="Scorpion",
        stats= CharacterStats(
            max_health=5 if scale == 1 else 25,
            damage=1 if scale == 1 else 2,
        ),
        artwork=Scorpion().scaleUp(scale),
        abilities=[Whack()],
    )
    if scale != 1: output.current_health = 15
    return output



def get_number_selection_from_options(options):
    while True:
        user_input = wait_for_character_input()
        try:
            user_input = int(user_input)-1
            if user_input > len(options):
                continue
            return user_input
        except:
            continue

def prevent_text_overflow(text, size = 60):
    output = [text]
    while (True in [len(a) > size for a in output]):
        for i in range(len(output)):
            if len(output[i]) > size:
                split_point = size
                while split_point > 0:
                    if output[i][split_point] == " ":
                        break
                    else:
                        split_point -= 1
                dash = False
                if split_point < size - 10:
                    split_point = size -1
                    dash = True
                output.insert(i+1, output[i][split_point:].lstrip())
                output[i] = output[i][:split_point]
                if dash: output[i] += "-"
                break
    return output




def screen_center(item : list | str | int, horizontal=False, vertical=False):
    if horizontal and vertical:
        raise Exception("Must pick either horizontal or vertical")
    elif not horizontal and not vertical:
        raise Exception("Must pick either horizontal or vertical")
    if horizontal:
        if type(item) == list or type(item) == str:
            item = len(item)
        return int((screen_width - item)/2)
    elif vertical:
        if type(item) == list or type(item) == str:
            item = len(item)
        return int((screen_height - item)/2)


def get_victory_screen():
    victory_text = load_art("Victory_text")
    continue_text = "Press any key"
    return Screen(layers=[
        PixelLayer(victory_text, x=screen_center(victory_text[0], horizontal=True), y=int((screen_height - len(victory_text)-16)/2)),
        TextLayer("Health restored!", x = screen_center("Health restored!", horizontal=True), y=screen_center(1, vertical=True)-2),
        TextLayer(continue_text, x = screen_width-len(continue_text) - 3, y=screen_height-3),
        background_layer,
    ])

def get_defeat_screen():
    victory_text = load_art("Defeat_text")
    text1 = "Knocked out."
    text2 = "Returning to castle to heal up..."
    continue_text = "Press any key"
    return Screen(layers=[
        PixelLayer(victory_text, x=screen_center(victory_text[0], horizontal=True), y=int((screen_height - len(victory_text)-16)/2)),
        TextLayer(text1, x = screen_center(text1, horizontal=True), y=screen_center(1, vertical=True)-2),
        TextLayer(text2, x = screen_center(text2, horizontal=True), y=screen_center(1, vertical=True)),
        TextLayer(continue_text, x = screen_width-len(continue_text) - 3, y=screen_height-3),
        background_layer,
    ])

def get_drops_screen(charm : FunctionalCharms | Charms):
    if charm == None:
        raise Exception("ERROR! charm was none")
    drops_text : str = "The monster dropped a new ability:"
    if type(charm) == Charms:
        charm = FunctionalCharms(charm)
    art = charm.artwork
    description : list[str] = prevent_text_overflow(charm.description)
    continue_text = "Press any key"
    return Screen(layers=[
        TextLayer(drops_text, x=screen_center(drops_text, horizontal=True), y=2),
        PixelLayer(art, x=screen_center(art[0], horizontal=True), y=screen_center(art, vertical=True) - int(len(art)/2)),
        TextLayer(charm.name, x=screen_center(charm.name, horizontal=True), y=screen_center(1, vertical=True) + 2),
        *[TextLayer(description[i], x=screen_center(description[i], horizontal=True), y=screen_center(1, vertical=True) + 6 + 2*i) for i in range(len(description))],
        TextLayer(continue_text, x = screen_width-len(continue_text) - 3, y=screen_height-3),
        background_layer
    ])


def run_intro_dialogue(main_character : BasicCharacter):
    characters = [
        BasicCharacter(
            name="King",
            artwork=load_art("King"),
            character_type="Neutral",
        ),
        main_character
    ]

    display(get_chat(
        characters=characters, 
        text="Hello adventurer!\nEvil beasts have taken over this land.\nEliminate the three strongest and the rest will leave.\nWill you help me?",
        continue_text="Press any key"
    ))
    wait_for_character_input()

    options = ["Yes", "No"]
    display(get_options(characters=characters, options=options))

    user_input = get_number_selection_from_options(options)

    if user_input == 1:
        display(get_chat(
            characters=characters, 
            text="Oh.\nOk.\nBye then.",
            continue_text="Press any key"
        ))
        quit()

    display(get_chat(
        characters=characters, 
        text="Good luck adventurer!\nDefeat the three beasts and then return here to claim your prize!",
        continue_text="Press any key"
    ))

    wait_for_character_input()




def run_outro_dialogue(main_character : list[BasicCharacter]):
    characters = [
        BasicCharacter(
            name="King",
            artwork=load_art("King"),
            character_type="Neutral",
        ),
        *main_character
    ]

    adventurer_or_adventurers = "adventurer" if len(main_character) == 1 else "adventurers"

    display(get_chat(
        characters=characters, 
        text=f"Well done {adventurer_or_adventurers}!\nThe evil beasts have been defeated!",
        continue_text="Press any key"
    ))

    input = None
    while not input:
        input = wait_for_character_input()
        if input == "UP" or input == "LEFT" or input == "RIGHT" or input == "DOWN":
            input = None

    display(get_chat(
        characters=characters, 
        text="Here's a bunch of gold for completing your quest!\n THANKS FOR PLAYING!",
        continue_text="Press any key"
    ))

    wait_for_character_input()


def run_recruiting_druid_dialogue(main_character):
    characters = [
        BasicCharacter(
            name="Druid",
            artwork=load_art("Druid"),
            character_type="Neutral",
        ),
        main_character
    ]

    display(get_chat(
        characters=characters, 
        text="Great job with that giant scorpion!\nI tried, myself, but it was too tough for me.",
        continue_text="Press any key"
    ))
    wait_for_character_input()

    options = ["Thanks!", "Go way, I have work to do."]
    display(get_options(characters=characters, options=options))

    user_input = get_number_selection_from_options(options)

    if user_input == 1:
        display(get_chat(
            characters=characters, 
            text="Fair enough.\nGood luck with the others",
            continue_text="Press any key"
        ))
        wait_for_character_input()
        return False

    display(get_chat(
        characters=characters, 
        text="You're welcome!\nCould you use a hand with the other monsters?\nI'm not that good at whacking 'em, but I can keep you alive pretty well.",
        continue_text="Press any key"
    ))
    wait_for_character_input()

    options = ["Sure!", "Nah, I'm good."]
    display(get_options(characters=characters, options=options))

    user_input = get_number_selection_from_options(options)

    if user_input == 0:
        display(get_chat(
            characters=characters, 
            text="Sweet!\nLets go!",
            continue_text="Press any key"
        ))
        wait_for_character_input()
        return True
    else:
        display(get_chat(
            characters=characters, 
            text="Ok.\nGood luck!",
            continue_text="Press any key"
        ))
        print(user_input)
        wait_for_character_input()
        return False



# def display(screen : Screen, width_override : int = None, height_override : int = None) -> None:
#     width = screen_width if width_override == None else width_override
#     height = screen_height if height_override == None else height_override
#     print(f"\u001b[{width}D" + f"\u001b[{height}A" + str(screen))


global previous
previous = None

def display(screen : Screen, width_override : int = None, height_override : int = None, DEBUG = False) -> None:
    def get_text_color(background_color):
        if Color.brightness_value(background_color) > 0.5:
            text_color = (0, 0, 0)
        else:
            text_color = (255, 255, 255)
        return text_color

    # Move back to start
    width = screen_width if width_override == None else width_override
    height = screen_height if height_override == None else height_override
    output : str = f"\u001b[{100}D" + f"\u001b[{100+8}A"
    # Find and replace differences
    global previous
    pixels : list[list[tuple]] = screen.flatten()
    if previous == None:
        output += str(PixelLayer(pixels))
    else:
        last_change = (0, 0)
        count_y = 0
        for row_pair_index in range(ceil(len(pixels)/2)):
            row_pair_index *= 2
            top_row = pixels[row_pair_index]
            bottom_row = pixels[row_pair_index+1] if row_pair_index +1 < len(pixels) else None
            count_x = 0
            for element_index in range(len(top_row)):
                if top_row[element_index] != previous[row_pair_index][element_index] or (False if not bottom_row else (bottom_row[element_index] != previous[row_pair_index+1][element_index])):
                    if count_y > 0:
                        output += f"\u001b[{count_y}B" + f"\u001b[{100}D"
                        count_y = 0
                    if count_x > 0:
                        output += f"\u001b[{count_x}C"
                        count_x = 0
                    # output += "1"
                    output += PixelLayer.get_pixel_pair(pixels, row_pair_index, row_pair_index+1, element_index)
                #     # A difference was found
                #     if DEBUG: print(f"difference detected was {previous[row_pair_index][element_index]} and {previous[row_pair_index+1][element_index]} is {top_row[element_index]} and {bottom_row[element_index]} at {element_index-last_change[0]} and {row_pair_index-last_change[1]}")
                #     move_y = row_pair_index-last_change[1]
                #     if move_y > 0:
                #         output += f"\u001b[{move_y-1}B\u001b[{width}D"
                #     move_x = element_index-last_change[0]-1
                #     if move_x > 0:
                #         output += f"\u001b[{move_x}C"
                else:
                    count_x += 1
                    # output += f"\u001b[{0}C"
                    # output += "0"
                    # if bottom_row:
                    #     if type(top_row[element_index]) == TextPixel:
                    #         pixel = top_row[element_index]
                    #         output += character_and_pixel.format(
                    #             *get_text_color(pixel.top_pixel_color), 
                    #             *Color.combine(pixel.top_pixel_color, bottom_row[element_index]), 
                    #             "H"
                    #         )
                    #     elif type(bottom_row[element_index]) == TextPixel:
                    #         pixel = bottom_row[element_index]
                    #         output += character_and_pixel.format(
                    #             *get_text_color(pixel.top_pixel_color), 
                    #             *Color.combine(pixel.top_pixel_color, top_row[element_index]), 
                    #             "H"
                    #         )
                    #     else:
                    #         output += top_and_bottom_pixels.format(*top_row[element_index], *bottom_row[element_index])
                    # else:
                    #     if type(top_row[element_index]) == TextPixel:
                    #         pixel = top_row[element_index]
                    #         output += character_and_pixel.format(*get_text_color(pixel.top_pixel_color), *pixel.top_pixel_color, "H")
                    #     else:
                    #         output += top_pixel_only.format(*top_row[element_index])
                    # last_change = (element_index, row_pair_index)
            count_y += 1
    print(output + line_end)
    previous = pixels


def boxify(text : str, number : int, x_offest : int = 3):
    return [
        TextLayer(text, x = x_offest, y = screen_height + 3),
        TextLayer(str(number), x = x_offest + len(text) + 3, y = screen_height + 4),
        get_box(height=5, width=len(text) + 5).set_pos(x= x_offest-3, y = screen_height),
    ]











# print(PixelLayer(get_text_as_pixels_big("YOU WON")))


# layer = PixelLayer(load_art("Druid"))


# print(layer)
# print(PixelLayer(tint_layer(layer.pixel_array, Color.GREEN)))



# import abilities

# test_hero = BasicCharacter(
#     name= "Wizard",
#     stats= CharacterStats(damage=3, max_health=12),
#     artwork=load_art("Wizard"),
#     character_type="Ally",
#     abilities= [Whack(), Heal(), Poison()],
# )

# enemy = BasicCharacter(
#     name="Test Dummy",
#     stats=CharacterStats(max_health=15),
#     artwork=Scorpion().art,
#     character_type="Enemy",
#     abilities=[Whack(), Heal()],
# )
# test_hero.current_status_effects.append(status_effects.DamageBoost())


class TurnEngine():
    def __init__(self, heros, enemies) -> None:
        self.turn_order : list[BasicCharacter] = [*heros, *enemies]
        self.position_in_turn_order : int = -1

    def next_up(self):
        self.position_in_turn_order += 1
        if self.position_in_turn_order >= len(self.turn_order):
            self.position_in_turn_order = 0
        return self.turn_order[self.position_in_turn_order]

    def ended(self):
        if len(self.turn_order) <= 0: return True
        detected = self.turn_order[0].character_type
        for char in self.turn_order:
            if char.character_type != detected:
                return False
        return True

    def skip_turn(self, character):
        pass

    def remove_from_turn_order(self, character):
        spot = self.turn_order.index(character)
        # If character to be removed is before the current position in the turn order, the current position needs to be moved back one
        if spot < self.position_in_turn_order:
            self.position_in_turn_order -= 1
        self.turn_order.remove(character)
        # If the removed character was the last character, the current position needs to be updated to the first character
        if self.position_in_turn_order >= len(self.turn_order):
            self.position_in_turn_order = 0


def printthings(heros, enemies, acting, selected = None):
    for a in heros:
        display = ""
        if a == selected:
            display += ">"
        else:
            display += " "
        if a == acting:
            display += f"[{a.name}]"
        else:
            display += f" {a.name}"
        print(display)
    for a in enemies:
        display = ""
        if a == selected:
            display += ">"
        else:
            display += " "
        if a == acting:
            display += f"[{a.name}]"
        else:
            display += f" {a.name}"
        print(display)




class PsudeoLayer():
    def __init__(self, layers : list[Layer | int] = []) -> None:
        self.layers : list[Layer | int] = layers

    def get_height(self):
        height = 0
        for a in self.layers:
            if type(a) == int:
                height += a
            elif type(a) == PixelLayer:
                height += len(a.pixel_array)
            else:
                height += 2
        return height

    def get_width(self):
        widest = 0
        for a in self.layers:
            if type(a) == int:
                continue
            if len(a.pixel_array[0]) > widest:
                widest = len(a.pixel_array[0])
        return widest

    def as_list(self):
        widest = self.get_width()

        offset = 0
        for a in self.layers:
            if type(a) == int:
                offset += a
                continue
            a.update_pos(y=offset, x = int((widest - len(a.pixel_array[0]))/2))
            if type(a) == PixelLayer:
                offset += len(a.pixel_array)
            else:
                offset += 2

        return [a for a in self.layers if type(a) != int]

    def update_pos(self, x : int = 0, y : int = 0):
        for a in self.layers:
            if type(a) == int:
                continue
            a.update_pos(x, y)
        return self


def get_psudo_layer(character : BasicCharacter, selected : bool, stick_to_left_side_of_screen = False, turn = False, text : str = None):
    if character.current_health <= 0:
        artwork = tint_layer(character.artwork, Color.GREY)
    elif character.skip_next_turn:
        artwork = tint_layer(character.artwork, (165, 205, 255))
    elif status_effects.Poisoned() in character.current_status_effects:
        artwork = tint_layer(character.artwork, Color.GREEN)
    else:
        artwork = character.artwork
    output_layer = PsudeoLayer(
        ([TextLayer(text),
        1,] if text != None else [])
         +
        ([PixelLayer([
            [Color.WHITE, None, None, None, Color.WHITE],
            [None, Color.WHITE, None, Color.WHITE, None],
            [None, None, Color.WHITE, None, None],
        ]),
        1,] if selected else [])
         +
        [
        PixelLayer(artwork),
        2,
        TextLayer(text= f"> {character.name} <" if turn else character.name, background_color= Color.BLUE if turn else None),
        get_health_bar(character.current_health, character.stats.max_health),
    ])
    output_layer.update_pos(
        x = screen_width-output_layer.get_width() if stick_to_left_side_of_screen else 0,
        y=screen_height-output_layer.get_height()
    )
    return output_layer

# allies = [test_hero, test_hero.deepcopy()]

def get_layers(character_list : list[BasicCharacter], right : bool, selected : BasicCharacter, turn : BasicCharacter, with_text : BasicCharacter = None, text : str = None):
    layers = []
    for i in range(len(character_list)):
        char = character_list[len(character_list)-1-i]
        layer = get_psudo_layer(char, char == selected, right, char == turn, text if char == with_text else None)
        layers.extend(
            layer.update_pos(x = i * (layer.get_width() + 1) * (-1 if right else 1) + (-1 if right else 1)).as_list()
        )
    return layers


# enemies = [enemy, enemy.deepcopy()]

def manufacture_layer(allies : list[BasicCharacter], enemies : list[BasicCharacter], turn : BasicCharacter, selected = None, damage_done = None, damage_target = None, show_abilities : bool = True):
    allies = [a for a in allies.__reversed__()]
    layers : list[PixelLayer] = get_layers(allies, True, selected, turn, damage_target, damage_done)
    layers.extend(get_layers(enemies, False, selected, turn, damage_target, damage_done))

    edge_offset = (screen_width/4-18)/2

    if turn.character_type == "Ally" and show_abilities:
        for i in range(4):
            if i >= len(turn.abilities):
                continue
            layers.append(get_box(height=4, width=14).set_pos(x = int(screen_width/4 * i + edge_offset), y = screen_height+8-7))
            layers.append(TextLayer(turn.abilities[i].name, x=int(screen_width/4 * i + edge_offset) + 3, y=screen_height+8-6))
            if turn.abilities[i].on_cooldown:
                layers.append(TextLayer("On Cooldown", x=int(screen_width/4 * i + edge_offset) + 5, y=screen_height+8-4))
            else:
                layers.append(TextLayer(str(i+1), x=int(screen_width/4 * i + edge_offset) + 15, y=screen_height+8-4))

    if damage_target:
        if damage_target in enemies:
            index = enemies.index(damage_target)

    return Screen(layers=[
        *layers,
        PixelLayer(tint_layer(background_layer.pixel_array, Color.BLACK))
    ])







def get_from_options(print_things_arguments, options_list, targeting_character : bool = False):
    position = 0
    while True:
        if targeting_character:
            display(manufacture_layer(*print_things_arguments, options_list[position], show_abilities=False))
        else:
            display(manufacture_layer(*print_things_arguments), show_abilities=False)
        match wait_for_character_input():
            case "LEFT":
                if position < len(options_list)-1:
                    position += 1
            case "RIGHT":
                if position > 0:
                    position -= 1
            case "\\n":
                break
    return options_list[position]

def run_conflict(heros : list[BasicCharacter] = [], enemies : list[BasicCharacter] = []):
    DEBUG = False


    turn_engine : TurnEngine = TurnEngine(heros, enemies)

    while not turn_engine.ended():
        acting_character : BasicCharacter = turn_engine.next_up()

        if acting_character.skip_next_turn:
            acting_character.end_turn()
            continue

        display(manufacture_layer(heros, enemies, acting_character, None))
        # printthings(heros, enemies, acting_character)

        if DEBUG:
            print("\n-----------------")
            print(f"It is {acting_character.name}'s turn")

        # Determines what to do
        selected_action : Ability | None = None

        usable_abilities = [a for a in acting_character.abilities if not a.on_cooldown]
        if len(usable_abilities) == 0:
            continue
            # raise Exception(f"{acting_character.name} has no abilities")

        if acting_character.character_type == "Ally":
            if DEBUG: print("Select an action")
            if DEBUG: print(" " + "\n ".join([ability.name + ("" if not ability.on_cooldown else f" - {ability.on_cooldown}") for ability in acting_character.abilities if not ability.on_cooldown]))
            while selected_action == None:
                user_input = wait_for_character_input()
                try:
                    selected_action = usable_abilities[int(user_input)-1]
                except:
                    selected_action = None
        elif acting_character.character_type == "Enemy":
            selected_action = usable_abilities[randint(0, len(usable_abilities)-1)]
        if selected_action == None:
            print(f"{acting_character.name} did nothing this round.")
            continue
        if DEBUG: print(f" Selected {selected_action.name} as action")

        # Determines who it can be done to
        targetable_characters : list[BasicCharacter] = []
        my_allies = heros if acting_character.character_type == "Ally" else enemies
        my_enemies = enemies if acting_character.character_type == "Ally" else heros
        match selected_action.target_type:
            case TargetType.ALLY:
                targetable_characters = [a for a in my_allies if a.current_health > 0]
            case TargetType.ALLIES_RANDOM:
                temp = [a for a in my_allies if a.current_health > 0]
                targetable_characters = [temp[randint[0, len(temp)-1]]]
            case TargetType.ENEMY:
                targetable_characters = [a for a in my_enemies if a.current_health > 0]
            case TargetType.ENEMIES_RANDOM:
                temp = [a for a in my_enemies if a.current_health > 0]
                targetable_characters = [temp[randint[0, len(temp)-1]]]
            case TargetType.ALL:
                targetable_characters = [a for a in my_allies if a.current_health > 0] + [a for a in my_enemies if a.current_health > 0]
            case TargetType.SELF:
                targetable_characters = [acting_character]
        if len(targetable_characters) <= 0:
            print(f"{acting_character.name} had no targets for {selected_action}.")
            continue
        if DEBUG: print(f" Can target {[a.name for a in targetable_characters]}")

        # Determines who to do it to (from that list)
        if len(targetable_characters) == 1:
            target = targetable_characters[0]
        else:
            target : BasicCharacter = None
            if acting_character.character_type == "Ally":
                # print("Select a target")
                # print(" " + "\n ".join([c.name for c in targetable_characters]))
                target = get_from_options([heros, enemies, acting_character], targetable_characters, True)
            elif acting_character.character_type == "Enemy":
                target = targetable_characters[randint(0, len(targetable_characters)-1)]
        if DEBUG: print(f" Target is {target.name}")

        # Does it
        result = selected_action.activate(
            using_characters_stats= acting_character.stats,
            using_characters_effects= acting_character.current_status_effects,
            effected_character= target,
            DEBUG=DEBUG,
        )

        if acting_character.character_type == "Enemy":
            sleep(1)

        display(manufacture_layer(heros, enemies, acting_character, None, result, target, False))

        if target.current_health <= 0:
            turn_engine.remove_from_turn_order(target)

        # Character ends their turn
        acting_character.end_turn(DEBUG=DEBUG)
        if acting_character.current_health <= 0:
            turn_engine.remove_from_turn_order(acting_character)

        if DEBUG:
            print()
            for a in heros:
                print(a)
                print()
            for a in enemies:
                print(a)
                print()

        sleep(1)

    for a in heros:
        for b in a.abilities:
            b.on_cooldown = 0

    # Returns True if the characters that are still standing (when all the not elimated characters are on one team) are on the hero's side
    for a in heros:
        if a.current_health > 0:
            return True
    return False



# test_hero.abilities[0].activate(test_hero.stats, test_hero.current_status_effects, enemy)

# run_conflict(heros=[test_hero], enemies=[enemy, enemy.deepcopy()])
# clear_screen()




def get_ability_change_screen(heros):
    x = 0
    y = 0

    while True:
        layer = []
        for i in range(len(heros)):
            layer.append(PixelLayer(heros[i].artwork, x = 2, y = 22 * i))
            for j in range(4):
                if j < len(heros[i].abilities):
                    text = f"> {heros[i].abilities[j].name} <" if y == i and x == j else heros[i].abilities[j].name
                else:
                    text = "> EMPTY <" if y == i and x == j else "EMPTY"
                layer.append(TextLayer(
                    text,
                    x=(j+1) * 15 + int((15-len(text))/2),
                    y = 16 + 22 * i,
                    background_color=Color.BLUE if y == i and x == j else None,
                ))

            layer.extend([
                *[PixelLayer(heros[i].abilities[j].artwork, x=(j+1) * 15, y = 22 * i) for j in range(len(heros[i].abilities))],
                *[TextLayer(
                        "REMOVE?" if j < len(heros[i].abilities) else "ADD?",
                        x=(j+1) * 15 + int((15-len("REMOVE?" if j < len(heros[i].abilities) else "ADD"))/2),
                        y = 18 + 22 * i,
                    ) for j in range(4) if y == i and x == j
                ],
            ])

        display(Screen([
            *layer, 
            get_box(height=5, width=9).set_pos(y = screen_height),
            TextLayer("Back", x = 3, y = screen_height + 3),
            TextLayer("1", x = 10, y = screen_height + 4),
            background_layer,
        ]))

        user_input = wait_for_character_input()
        if user_input == "RIGHT":
            if x < 3:
                x += 1
        elif user_input == "LEFT":
            if x > 0:
                x -= 1
        if user_input == "UP":
            if y > 0:
                y -= 1
        elif user_input == "DOWN":
            if y < len(heros)-1:
                y += 1
        elif user_input == "\\n":
            if x < len(heros[y].abilities):
                ability = heros[y].abilities.pop(x)
                player_inventory.append(ability)
            else:
                item = get_inventory_item()
                if item == None:
                    continue
                player_inventory.remove(item)
                heros[y].abilities.append(item)
        elif user_input == "1":
            return


# player_inventory = [Win()]


def get_inventory_item():
    if len(player_inventory) == 0:
        return None

    x = 0
    y = 0
    selected = None
    while not selected:

        layer = []
        for i in range(3):
            for j in range(5):
                spot = i * 5 + j
                if spot < len(player_inventory):
                    layer.append(PixelLayer(player_inventory[spot].artwork, x = j * 17, y = i * 20))
                    text = f"> {player_inventory[spot].name} <" if i == y and j == x else player_inventory[spot].name
                    layer.append(TextLayer(
                        text, 
                        x = j * 17 + int((15-len(text))/2), 
                        y = i * 20 + 16,
                        background_color= Color.BLUE if i == y and j == x else None
                    ))

        display(Screen([*layer, background_layer]))

        user_input = wait_for_character_input()
        if user_input == "RIGHT":
            if x < len(player_inventory) - y * 5-1 and x < 4:
                x += 1
        elif user_input == "LEFT":
            if x > 0:
                x -= 1
        if user_input == "UP":
            if y > 0:
                y -= 1
        elif user_input == "DOWN":
            if y < 2 and y < int(len(player_inventory)/5):
                y += 1
                if x >= len(player_inventory) - y * 5-1:
                    x = len(player_inventory) - y * 5-1
        elif user_input == "\\n":
            return player_inventory[y * 5 + x]


# get_ability_change_screen()

Encounter_Map = load_art("Encounter_Map")

def run_game(DEBUG = False):
    # GAME STARTs
    clear_screen()


    party = [
        BasicCharacter(
            name= "Wizard",
            stats = CharacterStats(
                max_health=10,
                damage=2,
                healing=1,
            ),
            artwork=load_art("Wizard"),
            character_type="Ally",
            abilities=[Whack(), Heal()],
        ),
    ]

    run_intro_dialogue(party[0])

    castle : Area = Area(starting_x=8, starting_y=4, ending_x=22, ending_y=14)
    castle_door = (15, 12)
    encounters : list[tuple[Area, character]] = [
        (Area(starting_x=19, starting_y=37, ending_x=32, ending_y=46), character.SCORPION, 25, 40), 
        (Area(starting_x=20, starting_y=27, ending_x=35, ending_y=34), character.DRAGON, 35, 30), 
        (Area(starting_x=43, starting_y=3, ending_x=66, ending_y=9), character.SNAKE, 54, 3), 
    ]
    map = PixelLayer(pixels=wrap_map(map=load_art("map")), x=1)
    # print(len(map.pixel_array[0]))
    # quit()


    # Starts player at door to castle
    player_x = castle_door[0]
    player_y = castle_door[1]

    while True:
        # Displays current player position on map
        player = PixelLayer(pixels=[[Color.PURPLE] for _ in range(3)], x = player_x + 3, y = player_y + 3,)
        display(Screen(layers=[
            player, 
            *[PixelLayer(characters._shrink_character(characters.to_subclass(a[1]).art), x=a[2], y=a[3]) for a in encounters], 
            *boxify("Change Abilties", 1),
            *boxify("Quit", 2, 30),
            map, 
            background_layer
        ]))
        if DEBUG: print(player_x, player_y)
        
        # Gets how the player moves
        user_input = wait_for_character_input()
        if user_input == "UP" and player_y > 0:
            player_y -= 1
        elif user_input == "DOWN" and player_y < 50:
            player_y += 1
        elif user_input == "LEFT" and player_x > 0:
            player_x -= 1
        elif user_input == "RIGHT" and player_x < 75:
            player_x += 1
        elif user_input == "1":
            get_ability_change_screen(party)
            continue
        elif user_input == "2":
            clear_screen()
            quit()
        else:
            continue

        # Checks if player's  new position matters
        if len(encounters) == 0:
            # Check to see if in castle
            if castle.in_area(player_x, player_y):
                # Win game
                run_outro_dialogue(party)
                quit()

        # Checks if player is on boss encounter location
        boss_encounter_triggered : bool = False
        for encounter in encounters:
            if encounter[0].in_area(player_x, player_y):
                boss_encounter_triggered = True
                # print(f"in encounter {encounter[1]}")
                enemy = encounter[1]
                if enemy == character.SNAKE:
                    enemy = get_snake_enemy(scale=3)
                elif enemy == character.DRAGON:
                    enemy = get_dragon_enemy(scale=3)
                elif enemy == character.SCORPION:
                    enemy = get_scorpion_enemy(scale=3)
                # Start fight
                victory : bool = run_conflict(heros=party, enemies=[enemy])
                if victory:
                    sleep(0.5)
                    display(get_victory_screen())
                    wait_for_character_input()
                    for member in party:
                        member.full_heal()
                    # If won, remove encounter from list of encounters
                    encounters.remove(encounter)
                    # If scorpion, recruit new party member
                    if enemy.name == "Scorpion":
                        # Recruit new party member
                        recruited : bool = run_recruiting_druid_dialogue(party[0])
                        if recruited:
                            party.insert(
                                0,
                                BasicCharacter(
                                    name= "Druid",
                                    stats= CharacterStats(damage=1, healing=5),
                                    artwork=load_art("Druid"),
                                    character_type="Ally",
                                )
                            )
                        pass
                else:
                    display(get_defeat_screen())
                    wait_for_character_input()
                    for member in party:
                        member.full_heal()
                    player_x = castle_door[0]
                    player_y = castle_door[1]
                break # breaks the loop that checks for encounters

        # Checks if random encounter has triggered
        if not boss_encounter_triggered:
            # print("not in encounter")
            if randint(0, 25) == 0:
                # Start random fight
                if Encounter_Map[player_y][player_x] == (255, 0, 0):
                    enemy_type = "Snake"
                    enemies = [get_snake_enemy(scale=1), get_snake_enemy(scale=1)]
                elif Encounter_Map[player_y][player_x] == (63, 72, 204):
                    enemy_type = "Dragon"
                    enemies=[get_dragon_enemy(scale=1), get_dragon_enemy(scale=1)]
                elif Encounter_Map[player_y][player_x] == (95, 62, 29):
                    enemy_type = "Scorpion"
                    enemies=[get_scorpion_enemy(scale=1), get_scorpion_enemy(scale=1)]
                else:
                    continue

                victory : bool = run_conflict(heros=party, enemies=enemies)
                if victory:
                    # Indicate victory
                    display(get_victory_screen())
                    wait_for_character_input()
                    for member in party:
                        member.full_heal()

                    # DROPS
                    random_drop = randint(0, 1)
                    if random_drop == 0:
                        charm = DamageBoost() if enemy_type == "Scorpion" else Freeze() if enemy_type == "Dragon" else Poison()
                        if charm in player_inventory:
                            continue
                        display(get_drops_screen(charm))
                        wait_for_character_input()
                        player_inventory.append(charm)
                        # for a in party:
                        #     a.base_damage *= 2
                    elif random_drop == 1:
                        charm = Charms.DIRT if enemy_type == "Scorpion" else Charms.WATER if enemy_type == "Dragon" else Charms.LAVA
                        display(get_drops_screen(charm))
                        wait_for_character_input()
                    # else: player gets nothing
                else:
                    display(get_defeat_screen())
                    wait_for_character_input()
                    for member in party:
                        member.full_heal()
                    player_x = castle_door[0]
                    player_y = castle_door[1]

if __name__ == "__main__":
    run_game()

