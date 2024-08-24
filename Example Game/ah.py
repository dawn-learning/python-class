from enum import Enum
from charms import *

class Color(Enum):
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
    # OFFWHITE = (215, 215, 215)
    OFFWHITE = (255, 238, 211)
    BLACK = (0, 0, 0)
    YELLOW = (255, 255, 0)
    PINK = (255, 25, 150)
    PURPLE = (255, 0, 255)
    BROWN = (160, 80, 45)
    GREY = (150, 150, 150)

    def __mul__(self, other):
        return [self for _ in range(other)]

    def __rmul__(self, other):
        return [self for _ in range(other)]

# # class Colorized:
# #     def __init__(
# #             self, 
# #             text : str = "", 
# #             text_color : Color | None = None, 
# #             background_color : Color | None = None,
# #         ) -> None:
# #         self._text = text
# #         self._text_color : Color | None = text_color
# #         self._background_color : Color | None = background_color

# #         self.__str = ""
# #         self._update_str()

# #     def _update_str(self):
# #         text = self._text
# #         if self._text_color != None:
# #             r, g, b = self._text_color.value
# #             text = f"\033[38;2;{r};{g};{b}m" + text
# #         if self._background_color != None:
# #             r, g, b = self._background_color.value
# #             text = f"\033[48;2;{r};{g};{b}m" + text
# #         if self._text_color != None or self._background_color != None:
# #             text += "\033[0m"
# #         self.__str = text

# #     def update(
# #             self, 
# #             text : str = None, 
# #             text_color : Color | None = "", 
# #             background_color : Color | None = ""
# #         ):
# #         if text != None:
# #             self._text = text
# #         if text_color != "":
# #             self._text_color = text_color
# #         if background_color != "":
# #             self._background_color = background_color
# #         self._update_str()

# #     def __str__(self) -> str:
# #         return self.__str

# #     def merge(given_array : list):
# #         pass

# #     def __add__(self, other):
# #         if type(other) == Colorized:
# #             if other._background_color == self._background_color and other._text_color == self._text_color:
# #                 self._text += other._text
# #                 return self
# #         return self.__str + str(other)

# #     def __radd__(self, other):
# #         if type(other) == Colorized:
# #             if other._background_color == self._background_color and other._text_color == self._text_color:
# #                 self._text = other._text + self._text
# #                 return self
# #         return str(other) + self.__str

# # class ColorizedText:
# #     def __init__(self, text : list[Colorized | str] = []) -> None:
# #         self._text = text

# #     def _to_dict(text, text_color, background_color):
# #         return {
# #             "text": text, 
# #             "text_color": text_color, 
# #             "background_color" : background_color,
# #         }

# #     def _convert_other_to_entry(other):
# #         if type(other) == str:
# #             other = ColorizedText._to_dict(other, None, None)
# #         if type(other) == Colorized:
# #             other = ColorizedText._to_dict(other._text, other._text_color, other._background_color)
# #         if type(other) == list:
# #             if len(other) == 1:
# #                 other = ColorizedText._to_dict(other[0], None, None)
# #             elif len(other) == 2:
# #                 other = ColorizedText._to_dict(other[0], other[1], None)
# #             elif len(other) == 3:
# #                 other = ColorizedText._to_dict(other[0], other[1], other[2])
# #             else:
# #                 raise Exception(f"other can only be of length 3 or less was {len(other)} long, other is {other}")
# #         return other

# #     def __add__(self, other):
# #         self._text.append(ColorizedText._convert_other_to_entry(other))

# #     def __radd__(self, other):
# #         self._text.insert(0, ColorizedText._convert_other_to_entry(other))

# #     def __str__(self):
# #         print("a")


# # class Layer:
# #     def __init__(self, width, height, background = Colorized("██", Color.RED)) -> None:
# #         self.layer = [[background for _ in range(width)] for _ in range(height)]

# #     def __str__(self) -> str:
# #         output = ""
# #         for row in self.layer:
# #             temp = Colorized()
# #             for item in row:
# #                 temp += item
# #             output += temp + "\n"
# #             # repr()
# #         if len(output) > 1:
# #             return output[:len(output)-1]
# #         return output

# # class Screen:
# #     def __init__(self, layers : list[Layer]) -> None:
# #         self.layers = layers

# #     def __str__(self) -> str:
# #         width = len(self.layers[0].layer[0])
# #         height = len(self.layers[0].layer)
# #         spots = []
# #         for row in range(height):
# #             for column in range(width):
# #                 spots.append((column, row))
# #         for a in 
# #         print(spots)

# # l = Screen([Layer(10, 10, None), Layer(10, 10)])

# # print(l)




from math import ceil

class Screen:
    def __init__(self, layers = [], size_x : int | None = None, size_y : int | None = None) -> None:
        self.layers = layers
        self.size_x = size_x
        self.size_y = size_y

    def __str__(self):
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

        # Prints the pixel layer
        return str(PixelLayer(pixels=output_pixels))


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
    
    def __str__(self):
        pixels = self.pixel_array
        output = ""
        for line_pair in range(ceil(len(pixels) / 2)):
            line = ""
            first = line_pair*2
            second = line_pair*2+1

            previous_top = None
            previous_bottom = None

            if second >= len(pixels):
                for column in range(len(pixels[first])):
                    top = pixels[first][column]
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

                        line += character_and_pixel.format(*top, top_character)
                        previous_top = None
                        previous_bottom = None
                    else:
                        if previous_top == top:
                            line += pixel_only
                        else:
                            line += top_pixel_only.format(*top)
                            previous_top = top
            else:
                for column in range(len(pixels[first])):
                    top = pixels[first][column]
                    top_character = None

                    try:
                        bottom = pixels[second][column]
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

                        line += character_and_pixel.format(*text_color, r, g, b, top_character)
                        previous_top = None
                        previous_bottom = None
                    else:
                        if previous_top == top and previous_bottom == bottom:
                            line += pixel_only
                        elif previous_top == top:
                            line += bottom_pixel_only.format(*bottom)
                            previous_bottom = bottom
                        elif previous_bottom == bottom:
                            line += top_pixel_only.format(*top)
                            previous_top = top
                        else:
                            line += top_and_bottom_pixels.format(*top, *bottom)
                            previous_top = top
                            previous_bottom = bottom
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




pixel_only = '▀'
top_pixel_only = '\033[38;2;{};{};{}m▀'
bottom_pixel_only ='\033[48;2;{};{};{}m▀'
top_and_bottom_pixels = '\033[38;2;{};{};{}m\033[48;2;{};{};{}m▀'
character_and_pixel = "\033[38;2;{};{};{}m\033[48;2;{};{};{}m{}"
line_end = "\033[0m"
# print(color_code.format(*, *))

from random import randint, choice

# pixels = []
# for i in range(25):
#     r = randint(0, 2)
#     if r != 0:
#         r = 1 if randint(0, 3) != 0 else None
#         if not r:
#             r = 2 if randint(0, 3) != 0 else 3
#     pixels.append(Color.BLACK * r + Color.WHITE * (25-r))




# pixels = PixelLayer(pixels=pixels)

# print(pixels)

def get_edge_freying_pattern():
    depth_array = []
    depth = 0
    same_count = 0
    for a in range(25):
        prob = 2 if same_count < 3 else 3 if same_count < 5 else 5
        if randint(0, prob) != 0:
            same_count = 0
            if randint(0, 2) == 0:
                if depth > 0:
                    depth -= 1
            else:
                if depth < 3:
                    depth += 1
        else:
            same_count += 1
        depth_array.append(depth)
    return depth_array


def get_edge_freying_pattern():
    edge_lengths = []
    direction = "DOWN"
    offest = randint(0, 3)
    total = 0
    max = 35

    while total < max:
        count = choice([1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 4])
        if total + count > max:
            count = max - total
        for _ in range(count):
            edge_lengths.append(offest)
        total += count
        if direction == "DOWN":
            if offest == 3:
                direction = "UP"
                offest -= 1
            else:
                offest += 1
        else:
            if offest == 0:
                direction = "DOWN"
                offest += 1
            else:
                offest -= 1
    return edge_lengths


# for i in edge_lengths:
#     print("x" * i)


# import math


# l = PixelLayer(pixels=[
#     [Color.PURPLE if randint(0, int(math.sqrt((35/2 - column) * (35/2 - column) + (35/2 - row) * (35/2 - row))/5)) == 0 else None for column in range(35)] for row in range(35)
# ])


# pixels = []
# for a in get_edge_freying_pattern():
#     pixels.append([None for _ in range(a)] + Color.BROWN * (25-a))

# pixels = PixelLayer(pixels=pixels, x = 5, y = 5)

# # print(pixels)
# # print(l)


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


from os import system
from time import sleep

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

health = 10
l = get_health_bar(health=health, max_health=10)

# print(l)


# print(PixelLayer(pixels=Hero().art))


eye_color = Color.PURPLE

male = [None] + Color.OFFWHITE * 7 + [None, None]
female = [None, None] + Color.OFFWHITE * 5 + [None, None]


from status_effects import *

global unique_id
unique_id = 0

class BasicCharacter:
    def __init__(self, name, current_health, max_health, artwork, base_damage = 2, base_healing = 0, character_type = "Enemy") -> None:
        self.name = name
        self.current_health = current_health
        self.max_health = max_health
        self.artwork = artwork
        self.current_status_effects = []
        self.outgoing_status_effects = []
        self.base_damage = base_damage
        self.base_healing = base_healing
        self.character_type = character_type
        self.default_actions = ["Attack", "Attack", "Attack", "Heal"]
        self.healing_pattern = ["Self", "All", "Random", "Self", "Self", "All"]
        self.charms = []
        global unique_id
        self.uniqueID = unique_id
        unique_id += 1

    # def __eq__(self, value: object) -> bool:
    #     return self.uniqueID == value.uniqueID

    def deepcopy(self):
        output = BasicCharacter(
            name=self.name,
            current_health=self.current_health,
            max_health=self.max_health,
            artwork=self.artwork.copy(),
            base_damage=self.base_damage,
            base_healing=self.base_healing,
            character_type=self.character_type,
        )
        output.current_status_effects = self.current_status_effects.copy()
        output.outgoing_status_effects = self.outgoing_status_effects.copy()
        output.default_actions = self.default_actions.copy()
        output.healing_pattern = self.healing_pattern.copy()
        output.charms = self.charms.copy()
        return output

    def height(self):
        return len(self.artwork) + 2 + 2 + 2

    def width(self):
        max_width = -1
        for row in self.artwork:
            if len(row) > max_width:
                max_width = len(row)
        if len(self.name) > max_width:
            max_width = len(self.name)
        if self.max_health > max_width:
            max_width = self.max_health
        return max_width

    def attack(self):
        if len(self.outgoing_status_effects) > 0:
            outgoing_status_effect = self.outgoing_status_effects.pop(0)
            self.outgoing_status_effects.append(outgoing_status_effect)
        else:
            outgoing_status_effect = None
        return (self.base_damage, outgoing_status_effect)

    def take_damage(self, damage):
        self.current_health -= damage
        if self.current_health < 0:
            self.current_health = 0

    def take_healing(self, healing):
        self.current_health += healing
        if self.current_health > self.max_health:
            self.current_health = self.max_health

    def get_next_default_action(self):
        action = self.default_actions.pop(0)
        self.default_actions.append(action)
        return action

    def get_next_in_healing_pattern(self):
        target = self.healing_pattern.pop(0)
        self.healing_pattern.append(target)
        return target

    def end_turn(self):
        for i in range(len(self.current_status_effects)):
            effect : StatusEffect = self.current_status_effects[i]
            if type(effect) != StatusEffect:
                raise Exception(f"status effect is not of type StatusEffect, instead is of type {type(effect)}")
            self.current_status_effects[i].duration = effect.action(self, effect.duration, effect.level)
        def remove_completed_status_effects():
            i = 0
            while i < len(self.current_status_effects):
                if self.current_status_effects[i].duration == None:
                    self.current_status_effects.pop(i)
                    continue
                i += 1
        remove_completed_status_effects()





def get_character_display(basic_character : BasicCharacter, selected : bool):
    def get_offset(obj):
        obj_len = len(obj) if type(obj) != int else obj
        return int((basic_character.width() - obj_len)/2)
    arrow_offset = 3 if selected else 0
    output = [
        PixelLayer(pixels = basic_character.artwork, x = get_offset(basic_character.artwork[0]), y=arrow_offset),
        TextLayer(basic_character.name, x = get_offset(basic_character.name), y = len(basic_character.artwork) + 2 + arrow_offset), 
        get_health_bar(health=basic_character.current_health, max_health=basic_character.max_health).set_pos(y=2 + len(basic_character.artwork) + 2 + arrow_offset, x = get_offset(basic_character.max_health)),
    ]
    if selected:
        arrow = [
            [Color.BROWN, None, None, None, Color.BROWN],
            [None, Color.BROWN, None, Color.BROWN, None],
            [None, None, Color.BROWN, None, None],
        ]
        return [PixelLayer(pixels = arrow, x = get_offset(arrow[0]))] + output
    return output




# print(PixelLayer(pixels=characters._shrink_character(Snake().art)))

screen_width = 83
screen_height = 58
background_layer = PixelLayer(pixels=[[(10, 10, 10) for _ in range(screen_width)] for _ in range(screen_height)])


villian = BasicCharacter(name="villian", current_health=20, max_health=20, artwork=[], base_healing=2)
hero = BasicCharacter(name="hero", current_health=20, max_health=20, artwork=[], character_type="Ally", base_healing=2)
hero.outgoing_status_effects = [StatusEffect(name = "Burn", action = burn, duration = 3, level = 2), None, None, None, None]
# j.current_status_effects.append([burn, 3, 2])
# for _ in range(4):
#     j.end_turn()
#     print(j.current_health, j.current_status_effects)
# j.current_status_effects.append([regen, 3, 2])
# for _ in range(4):
#     j.end_turn()
#     print(j.current_health, j.current_status_effects)
# print(j.base_damage, j.current_status_effects)
# j.current_status_effects.append([damage_boost, False, 2])
# for _ in range(4):
#     j.end_turn()
#     print(j.base_damage, j.current_status_effects)




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
    while True:
        for i in range(len(options)):
            print(f"{i+1} {options[i]}")
        user_input = input()
        try:
            user_input = int(user_input)-1
        except:
            print("Please input a number")
            continue
        return options[user_input]


def get_box(size : int = 5, id : int = 1):
    if type(size) != int:
        raise Exception(f"size must be an int, size is a {type(size)}")
    if type(id) != int:
        raise Exception(f"count must be an int, size is a {type(id)}")

    return PixelLayer(pixels=[
        [None, None] + Color.BROWN * (screen_width-4) + [None, None],
        *[[None, Color.BROWN] + [None for _ in range(screen_width-4)] + [Color.BROWN, None] for _ in range(size)],
        [None, None] + Color.BROWN * (screen_width-4) + [None, None],
    ], y=screen_height-(2 + size + 1) * id)





def reverse_artwork(artwork : list[list]):
    return [[a for a in line.__reversed__()] for line in artwork]










def get_chat(characters : list[BasicCharacter], text : str, continue_text : str):
    text = text.splitlines()
    layers = [
        PixelLayer(pixels=reverse_artwork(characters[0].artwork), x = 10, y = 20),
        *[PixelLayer(pixels=characters[i+1].artwork, x=i * 10 + 50, y= 20) for i in range(len(characters[1:]))],
        *[TextLayer(text[i], y=screen_height - 12 + i*2, x=3) for i in range(len(text))],
        get_box(size=11),
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
        layers.append(get_box(size=4, id=i+1))
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

from tester import wait_for_character_input
from artwork import *


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
        print(f"checking {all_list[i]} vs {turn_counter[options[selected]]} is {all_list[i] == turn_counter[options[selected]]}")
        if all_list[i] == turn_counter[options[selected]]:
            return i

def get_target(enemies, heros, turn_counter, options, heros_or_villians) -> BasicCharacter | None:
    # selected = 0
    # while True:
    #     pos = find_pos_in_list(enemies, heros, turn_counter, options, selected)
    #     print(pos)
    #     print(create_battle_screen(enemies=enemies, heros=heros, selected_character=pos))
    #     user_input = wait_for_character_input()
    #     if user_input == "RIGHT":
    #         if selected < len(options)-1:
    #             selected += 1
    #     elif user_input == "LEFT":
    #         if selected > 0:
    #             selected -= 1
    #     elif user_input == "\\n":
    #         return turn_counter[options[selected]]
    selected = 0
    character_options = heros if heros_or_villians == "Heros" else enemies
    while True:
        pos = selected + len(enemies) if heros_or_villians == "Heros" else selected
        clear_screen()
        print(create_battle_screen(enemies=enemies, heros=heros, selected_character=pos))
        user_input = wait_for_character_input()
        if user_input == "RIGHT":
            if selected < len(character_options)-1:
                selected += 1
        elif user_input == "LEFT":
            if selected > 0:
                selected -= 1
        elif user_input == "\\n":
            print(len(character_options), heros_or_villians, heros_or_villians == "Heros")
            return character_options[selected]

def run_battle_engine(heros : list[BasicCharacter], enemies : list[BasicCharacter]) -> bool:
    '''Returns True if heros won, returns False if enemies won'''
    DEBUG = False

    # Defines the turn order
    turn_counter = [*heros, *enemies]

    if DEBUG: print(f"both_sides_are_standing(turn_counter) is {both_sides_are_standing(turn_counter)}")
    while both_sides_are_standing(turn_counter):
        clear_screen()
        print(create_battle_screen(enemies=enemies, heros=heros))

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
    print(create_battle_screen(enemies=enemies, heros=heros))
    sleep(0.5)

    heros_cumulative_health, enemies_cumulative_health = get_cumulative_healths(turn_counter)
    return (heros_cumulative_health > enemies_cumulative_health)






def get_snake_enemy(scale = 1):
    return BasicCharacter(
        name = "Snake",
        current_health=10 if scale == 1 else 40,
        max_health=10 if scale == 1 else 40,
        artwork=Snake().scaleUp(scale),
        base_damage=1 if scale == 1 else 2,
    )

def get_dragon_enemy(scale = 1):
    return BasicCharacter(
        name="Dragon",
        current_health=8 if scale == 1 else 35,
        max_health=8 if scale == 1 else 35,
        artwork=Dragon().scaleUp(scale),
        base_damage=1 if scale == 1 else 2,
    )

def get_scorpion_enemy(scale = 1):
    return BasicCharacter(
        name="Scorpion",
        current_health=5 if scale == 1 else 19,
        max_health=5 if scale == 1 else 30,
        artwork=Scorpion().scaleUp(scale),
        base_damage=1 if scale == 1 else 2,
    )

# enemies = [enemy, enemy.deepcopy()]


# party = [
#     BasicCharacter(
#         name= "James",
#         current_health=10,
#         max_health=10,
#         artwork=example_artwork,
#         character_type="Ally",
#     ),
#     BasicCharacter(
#         name= "Jeoffry",
#         current_health=10,
#         max_health=10,
#         artwork=example_artwork,
#         character_type="Ally",
#     ),
#     # BasicCharacter(
#     #     name= "Jeorge",
#     #     current_health=10,
#     #     max_health=10,
#     #     artwork=example_artwork,
#     #     character_type="Ally",
#     # )
# ]

# run_battle_engine(heros=party, enemies=enemies)



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
        PixelLayer(pixels=[[(100, 100, 100) for _ in range(screen_width)] for _ in range(screen_height)])
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
        PixelLayer(pixels=[[(100, 100, 100) for _ in range(screen_width)] for _ in range(screen_height)])
    ])

def get_drops_screen(charm : FunctionalCharms | Charms):
    if type(charm) == Charms:
        charm = FunctionalCharms(charm)
    art = charm.artwork
    description : list[str] = prevent_text_overflow(charm.description)
    continue_text = "Press any key"
    return Screen(layers=[
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
            current_health=20,
            max_health=20,
            artwork=load_art("King"),
            character_type="Neutral",
        ),
        main_character
    ]

    clear_screen()
    print(get_chat(
        characters=characters, 
        text="Hello adventurer!\nEvil beasts have taken over this land.\nEliminate the three strongest and the rest will leave.\nWill you help me?",
        continue_text="Press any key"
    ))
    wait_for_character_input()

    clear_screen()
    options = ["Yes", "No"]
    print(get_options(characters=characters, options=options))

    user_input = get_number_selection_from_options(options)

    if user_input == 1:
        clear_screen()
        print(get_chat(
            characters=characters, 
            text="Oh.\nOk.\nBye then.",
            continue_text="Press any key"
        ))
        clear_screen()
        quit()

    clear_screen()
    print(get_chat(
        characters=characters, 
        text="Good luck adventurer!\nDefeat the three beasts and then return here to claim your prize!",
        continue_text="Press any key"
    ))

    wait_for_character_input()




def run_outro_dialogue(main_character : BasicCharacter):
    characters = [
        BasicCharacter(
            name="King",
            current_health=20,
            max_health=20,
            artwork=load_art("King"),
            character_type="Neutral",
        ),
        main_character
    ]

    clear_screen()
    print(get_chat(
        characters=characters, 
        text="Well done adventurer!\nThe evil beasts have been defeated!",
        continue_text="Press any key"
    ))
    wait_for_character_input()

    clear_screen()
    print(get_chat(
        characters=characters, 
        text="Here's a bunch of gold for completing your quest!\n THANKS FOR PLAYING!",
        continue_text="Press any key"
    ))

    wait_for_character_input()


def run_game(DEBUG = False):
    # GAME STARTs


    party = [
        BasicCharacter(
            name= "Wizard",
            current_health=10,
            max_health=10,
            artwork=load_art("Wizard"),
            character_type="Ally",
            base_healing=1
        ),
    ]

    run_intro_dialogue(party[0])

    castle : Area = Area(starting_x=8, starting_y=4, ending_x=22, ending_y=14)
    castle_door = (15, 12)
    encounters : list[tuple[Area, character]] = [
        (Area(starting_x=19, starting_y=37, ending_x=32, ending_y=46), character.SCORPION, 25, 40), 
        (Area(starting_x=20, starting_y=27, ending_x=35, ending_y=34), character.DRAGON, 35, 30), 
        (Area(starting_x=43, starting_y=3, ending_x=66, ending_y=9), character.SNAKE, 55, 2), 
    ]
    map = PixelLayer(pixels=wrap_map(map=load_art("map")))


    # Starts player at door to castle
    player_x = castle_door[0]
    player_y = castle_door[1]

    while True:
        # Displays current player position on map
        clear_screen()
        player = PixelLayer(pixels=[[Color.PURPLE] for _ in range(3)], x = player_x + 3, y = player_y + 3,)
        print(Screen(layers=[player, *[PixelLayer(characters._shrink_character(characters.to_subclass(a[1]).art), x=a[2], y=a[3]) for a in encounters], map]))
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

        # Checks if player's  new position matters
        if len(encounters) == 0:
            # Check to see if in castle
            if castle.in_area(player_x, player_y):
                # Win game
                run_outro_dialogue()
                quit()
        # Checks if player is on encounter location
        encounter_triggered : bool = False
        for encounter in encounters:
            if encounter[0].in_area(player_x, player_y):
                encounter_triggered = True
                # print(f"in encounter {encounter[1]}")
                enemy = encounter[1]
                if enemy == character.SNAKE:
                    enemy = get_snake_enemy(scale=3)
                elif enemy == character.DRAGON:
                    enemy = get_dragon_enemy(scale=3)
                elif enemy == character.SCORPION:
                    enemy = get_scorpion_enemy(scale=3)
                # Start fight
                victory : bool = run_battle_engine(enemies=[enemy], heros=party)
                if victory:
                    clear_screen()
                    print(get_victory_screen())
                    wait_for_character_input()
                    for member in party:
                        member.current_health = member.max_health
                    # If won, remove encounter from list of encounters
                    encounters.remove(encounter)
                    # If scorpion, recruit new party member
                    if enemy.name == "Scorpion":
                        # Recruit new party member
                        pass
                else:
                    clear_screen()
                    print(get_defeat_screen())
                    wait_for_character_input()
                    for member in party:
                        member.current_health = member.max_health
                    player_x = castle_door[0]
                    player_y = castle_door[1]
                break # breaks the loop that checks for encounters

        # Checks if random encounter has triggered
        if not encounter_triggered:
            # print("not in encounter")
            if randint(0, 25) == 0:
                # Start random fight
                distance_to_diagonal = (50 * player_x - 75 * player_y) / 90.138781
                if distance_to_diagonal < 0 and player_x > 25:
                    enemy_type = "Snake"
                    enemies = [get_snake_enemy(scale=1), get_snake_enemy(scale=1)]
                elif distance_to_diagonal > 12:
                    enemy_type = "Dragon"
                    enemies=[get_dragon_enemy(scale=1), get_dragon_enemy(scale=1)]
                else:
                    enemy_type = "Scorpion"
                    enemies=[get_scorpion_enemy(scale=1), get_scorpion_enemy(scale=1)]

                victory : bool = run_battle_engine(enemies=enemies, heros=party)
                if victory:
                    # Indicate victory
                    clear_screen()
                    print(get_victory_screen())
                    wait_for_character_input()
                    for member in party:
                        member.current_health = member.max_health

                    # DROPS
                    random_drop = randint(0, 1)
                    if random_drop == 0:
                        charm = Charms.POWERSPELL if enemy_type == "Scorpion" else Charms.DIRT if enemy_type == "Dragon" else Charms.DIRT
                        clear_screen()
                        print(get_drops_screen(charm))
                        wait_for_character_input()
                        for a in party:
                            a.base_damage *= 2
                    elif random_drop == 1:
                        charm = Charms.DIRT if enemy_type == "Scorpion" else Charms.WATER if enemy_type == "Dragon" else Charms.LAVA
                        clear_screen()
                        print(get_drops_screen(charm))
                        wait_for_character_input()
                    # else: player gets nothing
                else:
                    clear_screen()
                    print(get_defeat_screen())
                    wait_for_character_input()
                    for member in party:
                        member.current_health = member.max_health
                    player_x = castle_door[0]
                    player_y = castle_door[1]

run_game()




