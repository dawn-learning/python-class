
def update_image(image_name : str):
    from PIL import Image

    im = Image.open(f'..\\{image_name}.png')
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

    with open(f"{image_name.lower()}.txt", "w") as f:
        f.write(updated_file)

    print("updated")

def load_art(image_name : str):
    with open(f"{image_name.lower()}.txt", "r") as f:
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
