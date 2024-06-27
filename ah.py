# from tkinter import *
# import time


# their_code = []
# with open("test.py", "r") as f:
#     line = f.readline()
#     while line:
#         their_code.append(line)
#         line = f.readline()
# # with open("test.py", "a") as f:
# #     f.write("def say_hi():\n   print('hi')")

# while ("\n" in their_code):
#     their_code.remove("\n")

# remove = []
# for a in their_code:
#     if a.strip()[0] == "#":
#         remove.append(a)

# while (len(remove) > 0):
#     their_code.remove(remove[0])
#     remove.remove(remove[0])

# print(their_code)


variables = {
    "x": "content",
    "y": "5"
}

# t = 'if (x == "hi"):'
# if (t.startswith("if")):
#     t = t.replace(" ", "").rstrip(":").lstrip("if")
#     if (t.startswith("(") and t.endswith(")")):
#         t = t.lstrip(f"(").rstrip(")")
#     left = t.split("==")[0]
#     right = t.split("==")[1]
#     for variable in variables.keys():
#         if (variable in left):
#             left = left.replace(variable, variables[variable])
#         if (variable in right):
#             right = right.replace(variable, variables[variable])
# print(left, right)






# t = 'if (((a == "hi"))):'
# def seporate_equal_sides(t):
#     a, b = t.split("==")

#     a = a.removeprefix("if").strip()
#     b = b.removesuffix(":").strip()

#     while (a.count("(") > a.count(")")) and a.startswith("("):
#         a = a.removeprefix("(")

#     while (b.count("(") < b.count(")")) and b.endswith(")"):
#         b = b.removesuffix(")")
#     return a, b



# # print(seporate_equal_sides(t))


operators = ["+", "-", "*", "/", "%", "**", "//", "=", "==", "!=", "(", ")"]

# content = "a    (x+b)"
# for a in operators:
#     if a in content:
#         content = content.replace(a, f" {a} ")
# content = content.split(" ")


# while "" in content:
#     content.remove("")

# for variable in variables.keys():
#     while(variable in content):
#         content[content.index(variable)] = variables[variable]

# print(content)



def split(text):
    array = [text]
    array_spot = 0
    while (array_spot < len(array)):
        to_deal_with = array.pop(array_spot).strip()
        for text_spot in range(len(to_deal_with)):
            found = False
            for a in ["==", "+=", "-=", "*=", "/=", "(", ")", "*", "=", "+", "/", "or", "and"]:
                if (to_deal_with[text_spot : text_spot + len(a)] == a):
                    before = to_deal_with[0: text_spot]
                    if len(before) > 0:
                        array.append(before)
                        array_spot +=1 
                    array.append(to_deal_with[text_spot : text_spot + len(a)])
                    to_deal_with = to_deal_with[text_spot + len(a) :]
                    found = True
                    break
            if found:
                break
        if len(to_deal_with) > 0:
            array.append(to_deal_with)
        array_spot += 1
        # print(array)
    return array

# print(split("(2 * (b == a)"))


def recurive_parse(array, depth = 0):
    if (array[0] == "("):
        depth += 1
        array = recurive_parse(array[1:], depth)


def squish_array(array : list, DEBUG = False):
    if DEBUG: print("\narray is", array)
    for double_operator in ["+=", "-=", "*=", "/="]:
        while (double_operator in array):
            spot = array.index(double_operator)
            array[spot] = double_operator[1]
            array.insert(spot+1, double_operator[0])
            array.insert(spot+1, array[spot-1])
    if DEBUG: print("- double operators", array)
    while ("(" in array):
        parenthesis = []
        parenthesis_added = False
        if DEBUG: print("checking array:", array)
        for i in range(len(array)):
            if array[i] == "(":
                parenthesis.append(")")
                if str(parenthesis_added) == "False":
                    parenthesis_added = i
                if DEBUG: print(f"open parenthesis index = {i}")
            elif array[i] == ")":
                parenthesis.pop()
                if DEBUG: print(f"close parenthesis index = {i}")
            if str(parenthesis_added) != "False" and (len(parenthesis) == 0):
                if DEBUG: print("Detected largest internal array:", array[parenthesis_added+1 : i])
                result = squish_array(array[parenthesis_added+1 : i], DEBUG=DEBUG)
                array = array[: parenthesis_added] + result + array[i+1:]
                break
                # for _ in range(i - parenthesis_added + 1):
                #     array.pop(parenthesis_added)
                # array.insert(parenthesis_added, result[0])
    # return
    if DEBUG: print("array (-parenthesis) is", array)
    while len(array) > 1:
        # Error checking
        if (len(array) == 2):
            array == [str(array[0]) + str(array[1])]
            break
        # Order of operations
        for operator in ["*", "/", "+", "-", "and", "or", "==", "="]:
            array, worked = check_operator(array, operator)
            if (worked):
                if DEBUG: print("Doing", operator)
                if DEBUG and len(array) > 1: print(array)
                break
    if len(array) == 0: array = [None]
    if DEBUG: print(f"returning array: {array}\n")
    return array


def check_operator(array, operator):
    if operator in array:
        index = array.index(operator)
        left : list = array[index-1]
        if type(left) == str:
            left = left.strip()
        if not operator == "=":
            left = predict_and_convert_to_true_type(left)
        right : list = predict_and_convert_to_true_type(array[index+1])
        if operator == "*":
            array = array[: index-1] + [left * right] + array[index + 2:]
        elif operator == "/":
            array = array[: index-1] + [left / right] + array[index + 2:]
        elif operator == "+":
            array = array[: index-1] + [left + right] + array[index + 2:]
        elif operator == "-":
            array = array[: index-1] + [left - right] + array[index + 2:]
        elif operator == "and":
            array = array[: index-1] + [left and right] + array[index + 2:]
        elif operator == "or":
            array = array[: index-1] + [left or right] + array[index + 2:]
        elif operator == "==":
            # print(f"left {left} of type {type(left)} is being compared to right {right} of type {type(right)}")
            array = array[: index-1] + [left == right] + array[index + 2:]
        elif operator == "=":
            # print(f"variable {left} is being set to {right} or type {type(right)}")
            variables[left] = right
            array = array[: index-1] + array[index + 2:]
        return array, True
    return array, False


def predict_and_convert_to_true_type(unknown : str):
    if type(unknown) != str:
        return unknown
    unknown = unknown.strip()
    if (unknown.startswith("'") and unknown.endswith("'")) or (unknown.startswith('"') and unknown.endswith('"')):
        return str(unknown[1 : -1])
    if "." in unknown:
        try:
            return float(unknown)
        except:
            pass
    try:
        return int(unknown)
    except:
        pass
    if (unknown == "True"): return True
    if (unknown == "False"): return False
    for variable in variables.keys():
        if unknown == variable:
            # print(f"Replacing {variable} with {variables[variable]}")
            return variables[variable]
    return unknown

# statement = "if ((5 / 2) + y * (5/2)) * 0 == 0:"
# statement = "if (y /= 5):"

# If statement is true, do all indented statements under it and delete all else statments at same level.
# If statement is false, skip to next not indented statement.





import urllib.request
import tkinter as tk
from PIL import ImageTk, Image
import time
import io


character_portraits = {
    "normal" : "https://static.wikia.nocookie.net/slimerancher/images/2/2b/MochiDefault.png/revision/latest/scale-to-width-down/1000?cb=20180317174715", 
    "angry" : "https://static.wikia.nocookie.net/slimerancher/images/d/d6/MochiAngry.png/revision/latest/scale-to-width-down/1000?cb=20180317174315", 
    "boastful" : "https://static.wikia.nocookie.net/slimerancher/images/9/9e/MochiBoastful.png/revision/latest/scale-to-width-down/1000?cb=20180317174331", 
    "charming" : "https://static.wikia.nocookie.net/slimerancher/images/1/15/MochiCharming.png/revision/latest/scale-to-width-down/1000?cb=20180317174352", 
    "confident" : "https://static.wikia.nocookie.net/slimerancher/images/8/8a/MochiConfident.png/revision/latest/scale-to-width-down/1000?cb=20180317174404", 
    "discouraged" : "https://static.wikia.nocookie.net/slimerancher/images/7/74/MochiDiscouraged.png/revision/latest/scale-to-width-down/1000?cb=20180317174418", 
    "very discouraged" : "https://static.wikia.nocookie.net/slimerancher/images/5/5e/MochiDiscouraged2.png/revision/latest/scale-to-width-down/1000?cb=20180317174429", 
    "mocking" : "https://static.wikia.nocookie.net/slimerancher/images/2/21/MochiMocking.png/revision/latest/scale-to-width-down/1000?cb=20180317174440", 
    "sad" : "https://static.wikia.nocookie.net/slimerancher/images/1/13/MochiSad1.png/revision/latest/scale-to-width-down/1000?cb=20180317174500", 
    "sad mad" : "https://static.wikia.nocookie.net/slimerancher/images/0/0b/MochiSad2.png/revision/latest/scale-to-width-down/1000?cb=20180317174518", 
    "shy" : "https://static.wikia.nocookie.net/slimerancher/images/4/4c/MochiShy.png/revision/latest/scale-to-width-down/1000?cb=20180317174545", 
}

def load_portrait(mood):
    url = character_portraits[mood]
    with urllib.request.urlopen(url) as u:
        raw_data = u.read()
    image = ImageTk.PhotoImage(Image.open(io.BytesIO(raw_data)).resize((350, 350)))
    return image

def get_portrait_options():
    return list(character_portraits.keys())



character_mood = "normal"

actions : list[dict]= [
    # {
    #     "character_speaks" : "their sentence. their 2nd sentence. their 2nd sentence again. their 2nd sentence again. their 2nd sentence again. their 2nd sentence again.",
    #     "character_portrait_changes" : "angry",
    # }, 
    # {
    #     "character_speaks" : "their new sentence",
    # }, 
    # {
    #     "user_options" : ["stuff", "things", "3"]
    # }
]


class Window(tk.Tk):
    def __init__(self) -> None:
        tk.Tk.__init__(self)

        # Used to allow the user to interupt typing out the character's text
        self.type_called_count = 0

        self.image_height = 3

        self.image = load_portrait(character_mood)
        self.portrait = tk.Label(self, image=self.image)
        self.portrait.grid(row=0, column=0, rowspan=self.image_height, columnspan=2)

        self.displayed_text = tk.Label(self, text="", justify="left", wraplength=200) # wraplength is in pixels not characters
        self.displayed_text.grid(row=0, column=1)

        self.create_player_dialogue_frame()

        button_frame = tk.Frame(self, width=100, height=100, bg="#621947")
        button_frame.grid(row=self.image_height + 1, column=0, columnspan=2)
        tk.Button(button_frame, text = 'Run', command = lambda : self.Type("text")).grid(row=0, column=0)
        tk.Button(button_frame, text = '>>', command = lambda : self.next()).grid(row=0, column=2)

    def create_player_dialogue_frame(self, dialogue_options : list[str] = []):
        self.player_dialogue_frame = tk.Frame(self, height=100, bg="#621947")
        self.player_dialogue_frame.grid(row=self.image_height-1, column=0, columnspan=2)
        for i in range(len(dialogue_options)):
            label = tk.Button(self.player_dialogue_frame, text=dialogue_options[i], command= lambda i = i : self.dialogue_option_pressed(i))
            label.pack()

    def Type(self, text="text"):
        self.type_called_count +=1
        my_type_called_count = self.type_called_count
        # Clear previous text
        self.displayed_text["text"] = ""
        self.update()
        # Type out new text one character at a time.
        for i in range(len(text)+1):
            if my_type_called_count != self.type_called_count: return
            self.displayed_text["text"] = text[0: i]
            self.update()
            time.sleep(0.05)

    def dialogue_option_pressed(self, i):
        # prep for next
        print(i)

        self.next()



    def next(self):
        if len(actions) == 0: return
        current_actions : dict = actions.pop(0)
        if (current_actions == None): return
        keys = current_actions.keys()
        if "character_portrait_changes" in keys:
            character_mood = current_actions["character_portrait_changes"]
            image = load_portrait(character_mood)
            self.portrait.configure(image=image)
            self.portrait.image = image
        if "character_speaks" in keys:
            self.Type(current_actions["character_speaks"])
        # print()
        # print(len(actions))
        if "user_options" in keys:
            self.create_player_dialogue_frame(current_actions["user_options"])


# Window()
# tk.mainloop()




def parse_function(line, function_name):
    line : str = line.strip().removeprefix(function_name).removesuffix(")").strip().removeprefix("(")
    return [a.strip() for a in line.split(",")]




def get_their_code():
    their_code = []
    with open("test.py", "r") as f:
        while True:
            line = f.readline()
            if not line: break
            # Removes lines that are not code
            if (line == "\n"): continue
            if line.lstrip().startswith("#"): continue
            if "#" in line:
                line = line[:line.index("#")]
            # Removes import statements
            if "import" in line and not ( "'" in line or '"' in line): continue
            # Appends the rest
            their_code.append(line[:-1])
    return their_code


# to_parse = [their_code]
# to_parse_location = 0
# parsed = []
# lines = to_parse[to_parse_location]
# for line in lines:
#     if "if" in lines:
#         print("found")


def line_of_i(their_code_active, line_i):
    return their_code_active[line_i] if line_i < len(their_code_active) else "EOF"

def parse(their_code : list, user_selection = None, DEBUG = False) -> tuple[list, str]:
    """
    returns status Paused or Ended
    """
    if their_code == []: return [], "Ended"
    their_code_active = their_code[len(their_code)-1][0]
    line_i = their_code[len(their_code)-1][1]
    if DEBUG: print(f"Starting new parse run with code of length {len(their_code_active)}")

    if user_selection != None:
        their_code_active[line_i] = their_code_active[line_i].replace("input()", f'"{user_selection}"')

    options = []
    while (len(their_code) > 0):
        their_code_active = their_code[len(their_code)-1][0]
        line_i = their_code[len(their_code)-1][1]
        while line_i < len(their_code_active):
            line = their_code_active[line_i]
            # if DEBUG: print(f"{line_i}/{len(their_code_active)}")
            # if DEBUG: print(line)
            # Check to see if line is print_player
            if ("print_player" in line):
                parts = parse_function(line, "print_player")
                whole = ""
                for a in parts:
                    whole = " " + a
                if whole != "":
                    whole = whole[1:]
                options.append(whole)
            else:
                # If it is not another print_player, add all print_players up to this point to last action
                if len(options) > 0:
                    if (len(actions) < 1): 
                        actions.append({"user_options" : options})
                    else:
                        actions[len(actions)-1]["user_options"] = options
                    options = []
                # Other possible line contents
                if ("input" in line and not ("'" in line or '"' in line)):
                    their_code[len(their_code)-1][1] = line_i
                    return their_code, "Paused"
                elif ("print_character" in line):
                    if DEBUG: print(line)
                    parts = parse_function(line, "print_character")
                    if len(parts) < 1:
                        parts.append("")
                    if len(parts) > 2:
                        raise Exception(f"{line_i} : The function print_character takes at most two arguments")
                    dictionary = {
                        "character_speaks" : parts[0]
                    }
                    if len(parts) > 1:
                        dictionary["character_portrait_changes"] = parts[1]
                    actions.append(dictionary)
                    if DEBUG: print("action added")
                else:
                    if line.startswith("else"):
                        if not (line.strip() == "else:"):
                            raise Exception('Incorrectly formated "else:"')
                        line = "if True:"
                    if line.startswith("if") or line.startswith("elif"):
                        if not line.endswith(":"):
                            raise Exception("If statement does not include a semicolon at the end")
                        if line.startswith("if"):
                            line = line.removeprefix("if")
                        elif line.startswith("elif"):
                            line = line.removeprefix("elif")
                        line = line.removesuffix(":").strip()
                        line = squish_array(split(line), DEBUG=False)[0]
                        if line == None:
                            raise Exception('An "if" statement cannot be empty.\n You probably used "=" instead of "==".')
                        if line:
                            if DEBUG: print("If statement IS true")
                            if DEBUG: print(f" and line_i is {line_i}")
                            if DEBUG: print(f" and the line is {line_of_i(their_code_active, line_i)}")
                            child_statements = []
                            line_i += 1
                            while(line_i < len(their_code_active) and their_code_active[line_i].startswith("    ")):
                                child_statements.append(their_code_active[line_i].removeprefix("    "))
                                line_i += 1
                            while line_i < len(their_code_active) and (their_code_active[line_i].startswith("elif") or their_code_active[line_i].startswith("else")):
                                line_i +=1
                                while(their_code_active[line_i].startswith("    ")):
                                    line_i += 1
                                    if (line_i >= len(their_code_active)):
                                        break
                                    # else:
                                    #     if DEBUG: print(their_code_active[line_i])
                                if line_i >= len(their_code_active):
                                    break
                            if DEBUG: print(f"{len(their_code_active)}")
                            if DEBUG: print(f"line_i  is {line_i } ({line_of_i(their_code_active, line_i)})")
                            their_code[len(their_code)-1][1] = line_i
                            their_code.append([child_statements, 0])
                            if DEBUG: print(f"running parse again with {len(child_statements)} child statements")
                            their_code, result  = parse(their_code)
                            # if (result == "Paused"):
                            return their_code, result
                            # their_code.pop()
                            # their_code_active = their_code[len(their_code)-1][0]
                            # line_i = their_code[len(their_code)-1][1]
                            # line_i += 1
                            continue
                        else:
                            if DEBUG: print(f"If statement {line_of_i(their_code_active, line_i)} is false")
                            line_i += 1
                            while(line_i < len(their_code_active) and their_code_active[line_i].startswith("    ")):
                                line_i += 1
                            if DEBUG: print(f" and the next line not a part of the if is {line_of_i(their_code_active, line_i)}")
                            line_i -= 1
                    else:
                        line = squish_array(split(line), DEBUG=False)[0]
            if DEBUG: print("+1")
            line_i += 1
        their_code.pop()





                # split_line = split(line)


                # for i in range(len(split_line)):
                #     for variable in variables.keys():
                #         if split_line[i].strip() == variable:
                #             split_line[i] = variables[variable]
                # print(f" split line = {split_line}")
                # # print(line)
                # if len(split_line) == 3:
                #     if (split_line[1] == "="):
                #         variables[split_line[0].strip()] = split_line[2]
                #         print(variables)
    # If it is not another print_player, add all print_players up to this point to last action
    if len(options) > 0:
        if (len(actions) < 1): 
            actions.append({"user_options" : options})
        else:
            actions[len(actions)-1]["user_options"] = options
        options = []
    if len(their_code) > 0:
        print(f"len of their code {len(their_code)}")
        their_code[len(their_code)-1][1] = line_i
    return their_code, "Ended"


def print_actions():
    # print()

    # for a in range(line_i):
    #     print(their_code[a])

    # print()

    for a in actions:
        print(a)








their_code = [[get_their_code(), 0]]

status = None
while status == "Paused" or status == None:
    while len(actions) > 0:
        print(actions.pop(0))
    if status == None:
        their_code, status = parse(their_code)
    else:
        their_code, status = parse(their_code, user_selection=input())

while len(actions) > 0:
    print(actions.pop(0))


# print_actions()
# for a in their_code:
#     print(f"length = {len(a[0])}, i = {a[1]}")








































