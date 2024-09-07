from enum import Enum

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

def update_image(image_name : str, DEBUG : bool = False):
    from PIL import Image

    im = Image.open(f'..\\..\\{image_name}.png')
    pix = im.load()
    width, height = im.size

    updated_file = "[\n"
    for y in range(height):
        updated_file += " ["
        for x in range(width):
            r, g, b, a = pix[x, y]
            if a == 0:
                text = f"None"
            else:
                text = f"({r},{g},{b})"
            updated_file += text + ", "
        updated_file += "]\n"
    updated_file += "]"

    with open(f"art\\{image_name.lower()}.txt", "w") as f:
        f.write(updated_file)

    if DEBUG: print(f"{image_name}updated")

def load_art(image_name : str):
    with open(f"art\\{image_name.lower()}.txt", "r") as f:
        lines = f.readlines()
    lines.pop(0)
    lines.pop()

    output = []
    for line in lines:
        temp = []
        colors = line.removeprefix(" [").removesuffix(", ]\n").split(", ")
        for color in colors:
            color = color.removeprefix("(").removesuffix(")")
            if color == "None":
                temp.append(None)
            else:
                r, g, b = color.split(",")
                rgb = (int(r), int(g), int(b))
                temp.append(rgb)
        output.append(temp)
    return output

def get_text_as_pixels_big(text):
    def extract_letter(letter, DEBUG = False):
        if letter == " ":
            return [[None for _ in range(5)] for _ in range(10)]

        number_of_letter : int = ord(letter.upper())-64
        if DEBUG: print(letter, number_of_letter)

        if number_of_letter < 1 or number_of_letter > 26:
            raise Exception(f'Cannot show the letter "{letter}" with the get_text_as_pixels_big function')

        position_in_alphabet_graphic = (number_of_letter-1) * 7
        output = []
        for a in alphabet:
            if number_of_letter == 13 or number_of_letter == 23:
                output.append(a[position_in_alphabet_graphic:position_in_alphabet_graphic+8] + [None, None])
            else:
                output.append(a[position_in_alphabet_graphic+1:position_in_alphabet_graphic+7] + [None, None])
        return output

    letters = [extract_letter(a) for a in text]

    text = []
    for i in range(10):
        row = []
        for letter in letters:
            row += letter[i]
        text.append(row[:len(row)-2])
    return text

def update_images(DEBUG : bool = False):
    for image in ["Alphabet", "Whack", "Heal", "Encounter_Map", "Poison", "Freeze"]:
        update_image(image, DEBUG)

def tint_layer(pixels : list[list], color : Color | tuple, amount : float = 0.5) -> list[list]:
    '''Tinits the given pixels the given color by the given amount'''
    if amount > 1 or amount < 0:
        raise Exception(f"Amount is a percent between 0 and 1 (inclusive). Given amount = {amount}")
    if type(color) == Color:
        color = color.value
    color_r, color_g, color_b = color
    output = []
    for i in range(len(pixels)):
        row = []
        for j in range(len(pixels[i])):
            if pixels[i][j] == None:
                row.append(None)
                continue
            if type(pixels[i][j]) == Color:
                pixels[i][j] = pixels[i][j].value
            r, g, b = pixels[i][j]
            row.append(
                (
                    int(r * (1-amount) + color_r * amount), 
                    int(g * (1-amount) + color_g * amount), 
                    int(b * (1-amount)+ color_b * amount)
                )
            )
        output.append(row)
    return output

# Load image data
alphabet = load_art("Alphabet")
