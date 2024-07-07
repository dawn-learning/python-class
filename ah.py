from PIL import ImageTk, Image
import urllib.request
from enum import Enum
import tkinter as tk
import time
import io

global character_mood
character_mood = "normal"

actions : list[dict]= []
variables = {}

character_portraits = {
    "normal" : "https://static.wikia.nocookie.net/slimerancher/images/2/2b/MochiDefault.png/revision/latest/scale-to-width-down/1000?cb=20180317174715", 
    # "normal" : "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.solidbackgrounds.com%2Fimages%2F2560x1440%2F2560x1440-blue-solid-color-background.jpg&f=1&nofb=1&ipt=d0b034ef2889b452d604bebc5d1421b6f921356bd47650a96bb69c33436164d5&ipo=images",
    "icon" : "https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fvignette3.wikia.nocookie.net%2Fslimerancher%2Fimages%2F8%2F80%2FMochi_update.png%2Frevision%2Flatest%2Fscale-to-width-down%2F350%3Fcb%3D20160420041618&f=1&nofb=1&ipt=32f4792edf02a1309221f888c328fcbab975cb48c475284fb8a3d985201e871a&ipo=images",
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
            print(f"variable {left} is being set to {right} or type {type(right)}")
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

def get_portrait_options():
    return list(character_portraits.keys())

class Photo():
    def __init__(self, file : str | None = None) -> None:
        if file:
            self.load_image(file)
        else:
            self.image = None
            self.width = None
            self.height = None

    def load_portrait(self, mood : str):
        url = character_portraits[mood]
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()
        # image = ImageTk.PhotoImage(Image.open().resize((350, 350)))
        # return image
        self.load_image(io.BytesIO(raw_data))

    def load_image(self, file : any, inital_resize_factor : tuple[float, float] = None):
        self._just_loaded_image = Image.open(file)
        if inital_resize_factor:
            w = int(self._just_loaded_image.width * inital_resize_factor[0])
            h = int(self._just_loaded_image.height * inital_resize_factor[1])
            self._just_loaded_image = self._just_loaded_image.resize((w, h))
        self._unchanged_image = self._just_loaded_image.copy()
        self.image = ImageTk.PhotoImage(self._just_loaded_image)
        self._initial_height = self.image.height()
        self._initial_width = self.image.width()
        self._update_height_and_width()

    def update(self, given_width : int, given_height : int):
        given_space_width = given_width * 1.0
        given_space_height = given_height * 1.0
        if self._initial_width > self._initial_height:
            new_height = given_space_width/self._initial_width * self._initial_height
            new_width = given_space_width * 1.0
        else:
            new_width = given_space_height/self._initial_height * self._initial_width
            new_height = given_space_height * 1.0
        if new_width > given_width:
            new_height = given_width/self._initial_width * self._initial_height
            new_width = given_width
        elif new_height > given_height:
            new_width = given_width/self._initial_width * self._initial_height
            new_height = given_height
        new_width = int(new_width)
        new_height = int(new_height)
        self.image = ImageTk.PhotoImage(self._unchanged_image.resize((new_width, new_height)))
        self._update_height_and_width()

    def force_resize(self, given_width : int, given_height : int):
        self.image = ImageTk.PhotoImage(self._unchanged_image.resize((int(given_width), int(given_height))))
        self._update_height_and_width()

    def _update_height_and_width(self):
        self.height = self.image.height()
        self.width = self.image.width()

class Dimentions():
    def __init__(self, width : int = 0, height : int = 0) -> None:
        self.width = width
        self.height = height

    def generate_from_event(event):
        return Dimentions(event.width, event.height)
    
    def __eq__(self, value: object) -> bool:
        E = Exception("A Dimensions object can only be compared to another Dimensions object, a tuple of two numbers, or a list of two numbers")
        if value == None: return False
        if type(value) == Dimentions:
            return (self.width == value.width and self.height == value.height)
        if type(value) == list or type(value) == tuple:
            if len(list) != 2:
                raise E
            return (self.width == value[0] and self.height == value[1])
        raise E

def split_text(text : str) -> list[str]:
    leng = 34
    if len(text) <= leng:
        return [text]
    hard_split = text[:leng]
    if "\n" in hard_split:
        spot = text.index("\n") + 1
        while (text[spot] == " "):
            spot += 1
        return [text[:spot]] + split_text(text[spot:])
    split_point = leng
    while (text[split_point] != " " and text[split_point] != "\t"):
        if split_point == 0:
            split_point = leng
            break
        split_point -= 1
    return [text[:split_point]] + split_text(text[split_point+1:])

def squish_text_array(text_array : list[str]) -> str:
    output = ""
    for a in text_array:
        if not a.endswith("\n"):
            output += "\n"
        output += a
    return output[1:]

class Textbox():
    def __init__(self, imagename : str) -> None:
        self.text = None
        self.background_image = Photo(imagename)
    
    def add_to_canvas(
            self, available_size : Dimentions, canvas : tk.Canvas, center_screen_offset : Dimentions, 
            function, shrink_factor : int = 1 , count : int = 0,
        ):
        self.background_image.force_resize(available_size.width * 4/5, available_size.width / (4 * shrink_factor))
        background_x = (available_size.width-self.background_image.width)/2
        background_y = available_size.height-self.background_image.height * (count+1) - (self.background_image.height / 25) * count
        self.background_object = canvas.create_image(
            center_screen_offset.width + background_x, 
            center_screen_offset.height + background_y, 
            image = self.background_image.image, anchor=tk.NW)
        canvas.tag_bind(self.background_object, '<Button-1>', lambda _: function())
        self.text = canvas.create_text(
            center_screen_offset.width + background_x * 1.35,
            center_screen_offset.height + (background_y * 1.03 if shrink_factor == 1 else background_y * 1.01),
            justify="left",
            anchor=tk.NW,
            font=('Times New Roman', int(available_size.width * 3 /100), 'normal'),
            text=squish_text_array(split_text("AHHHHH")))

    def show(self, canvas : tk.Canvas):
        self._change_visibility(canvas, visibility=True)

    def hide(self, canvas : tk.Canvas):
        self._change_visibility(canvas, visibility=False)

    def _change_visibility(self, canvas : tk.Canvas, visibility : bool):
        canvas.itemconfigure(self.background_object, state='normal' if visibility else 'hidden')
        canvas.itemconfigure(self.text, state='normal' if visibility else 'hidden')

    def update_text(self, canvas : tk.Canvas, text : str):
        canvas.itemconfigure(self.text, text = text)

class Window(tk.Tk):
    def __init__(self, code) -> None:
        tk.Tk.__init__(self)
        # self.geometry("400x400")

        self.code = code

        # Used to allow the user to interupt typing out the character's text
        self.type_called_count = 0

        # self.image_height_rows = 3
        self.previous_event = None

        # self.photo = Photo()
        # self.photo.load_portrait(character_mood)
        # self.portrait = tk.Label(self, image=self.photo.image)
        # self.portrait.grid(row=0, column=1, sticky="nsew", rowspan=self.image_height_rows)
        # # , columnspan=2

        self.bind("<Configure>", self._resize_widgets)

        # # for i in range(4):
        # # self.columnconfigure(0, weight=1)
        # # self.rowconfigure(0, weight=1)
        #     # self.columnconfigure(i, weight=1)
        #     # self.rowconfigure(i, weight=1)

        # # self.displayed_text = tk.Label(self, text="",justify="right", wraplength=200, bg="lightgray", fg="purple", padx=10, pady=10, borderwidth=5, relief="solid") # wraplength is in pixels not characters
        # # self.displayed_text.grid(row=0, column=1, sticky="w", padx=20)

        # # self.create_player_dialogue_frame()
        # # label = tk.Label(self, text="Hello, Tkinter!                                                            ", bg="lightgray", fg="purple", padx=10, pady=10, borderwidth=5, relief="solid")
        # # label.grid(row=0, column=1)

        # # button_frame = tk.Frame(self, width=100, height=100, bg="#621947")
        # # button_frame.grid(row=self.image_height_rows + 1, column=0, columnspan=2)
        # # tk.Button(self, text = 'Run', command = lambda : self.Type("text")).grid(row=0, column=1)


        # # self.text_background = Photo()
        # # self.text_background.load_image("Picture1.png", (0.1, 0.1))
        # # tk.Label(self, image=self.text_background.image).grid(row=self.image_height_rows-1, column=1)
        # self.displayed_text = tk.Label(
        #     self, 
        #     text="jkflejlajfelkaljkfjdlkal", 
        #     justify="right", 
        #     wraplength=200, 
        #     bg="lightgray", 
        #     fg="purple", 
        #     # width=25,
        #     height=5,
        #     # padx=10, 
        #     # pady=5, 
        #     borderwidth=5, 
        #     relief="solid",
        #     font=('Times New Roman', 15, 'bold'),
        # )
        # self.displayed_text.grid(row=self.image_height_rows-1, column=1, sticky="s") # wraplength is in pixels not characters
        # self.spacer = tk.Label(width=0)
        # self.spacer.grid(row=0, column=0)
        # tk.Button(self, text = '>>', command = lambda : self.next()).grid(row=self.image_height_rows-1, column=1, sticky="se")

        self.screen_dimentions = Dimentions(500, 500)
        self.geometry(f'{self.screen_dimentions.width}x{self.screen_dimentions.height}')


        self.portrait = Photo()
        self.portrait.load_portrait("normal")
        self.canvas = tk.Canvas(self, background="red")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.available_size : Dimentions = None
        self.canvas_textbox : Textbox = Textbox("Picture1.png")
        self.canvas_user_options_textboxes : list[Textbox] = []
        self.inital_text = self.canvas.create_text(
                self.winfo_width()/2,
                self.winfo_height()/2,
                text="INTERVIEW GAME",
                font=('Times New Roman', int(self.winfo_width() * 3/100), 'bold'),
        )
        self.dont_change_size = True
        self.canvas.tag_bind(self.inital_text, '<Button-1>', lambda _: self.next())
        # self.fill_canvas()
        

    def fill_canvas(self):
        self.canvas.delete("all")
        self.portrait.update(self.screen_dimentions.width, self.screen_dimentions.height)
        self.available_size = Dimentions(self.portrait.width, self.portrait.height)
        new_offset = Dimentions(int((self.screen_dimentions.width-self.available_size.width)/2), int((self.screen_dimentions.height-self.available_size.height)/2))
        self.center_screen_offset = new_offset

        self.portrait_spot = self.canvas.create_image(
            self.center_screen_offset.width + (self.available_size.width - self.portrait.width)/2, 
            self.center_screen_offset.height + (self.available_size.height - self.portrait.height)/2, 
            image = self.portrait.image, anchor=tk.NW)

        self._create_canvas()

    def _create_canvas(self, small_count : int | None = None):
        # self.canvas_objects = []
        if not small_count:
            self.canvas_textbox.add_to_canvas(self.available_size, self.canvas, self.center_screen_offset, self.next)
            return
        if small_count < 1:
            raise Exception("Must have at least one user option")
        self.canvas_user_options_textboxes = []
        for i in range(small_count):
            print(i)
            if i >= len(self.canvas_user_options_textboxes):
                print("adding textbox")
                self.canvas_user_options_textboxes.append(Textbox("Picture1Small.png"))
            print("adding to canvas")
            self.canvas_user_options_textboxes[i].add_to_canvas(self.available_size, self.canvas, self.center_screen_offset, lambda i = i: self.dialogue_option_pressed(i), shrink_factor= 4, count=i)

    def _resize_widgets(self, event):
        if self.dont_change_size:
            return
        width = self.winfo_width()
        height = self.winfo_height()
        if not self.previous_event == None and self.previous_event[0] == width and self.previous_event[1] == height:
            return
        print(event)
        self.previous_event = (width, height)
        # # if not self.previous == (width, height):
        #     # self.previous = (width, height)
        # self.photo.update(width * 10/10, height * 10/10)
        # self.portrait.configure(image=self.photo.image)
        # self.displayed_text.configure(
        #     width=int(self.winfo_width()/15), 
        #     height=int(self.winfo_height()/100), 
        #     font=('Times New Roman', int(self.winfo_width()/50), 'bold'), 
        # )
        # self.spacer.configure(width=int((self.winfo_width() - self.portrait.winfo_width())/20))
        self.screen_dimentions = Dimentions(width, height)
        self.fill_canvas()

    def Type(self, text="text"):
        self.type_called_count +=1
        my_type_called_count = self.type_called_count
        # Clear previous text
        # self.displayed_text["text"] = ""
        self.canvas.itemconfigure(self.canvas_textbox.text, text="")
        self.update()
        # Type out new text one character at a time.
        for i in range(len(text)+1):
            if my_type_called_count != self.type_called_count: return
            # self.displayed_text["text"] = text[0: i]
            self.canvas.itemconfigure(self.canvas_textbox.text, text=text[0: i])
            self.update()
            time.sleep(0.05)

    def dialogue_option_pressed(self, i):
        if len(actions) == 0:
            # prep for next
            status = self.code.run_to_pause_or_end(str(i+1))
            if status == Status.COMPLETED:
                actions.append({"note": "Game Over."})
        self.next()

    def next(self, user_action = None):
        if not self.available_size:
            self.fill_canvas()
            self.dont_change_size = False
        if len(actions) == 0: 
            if user_action == None: return
            parse(self.code, user_selection=user_action)
            print(actions)
            if len(actions) == 0: return
        current_actions : dict = actions.pop(0)
        print(current_actions)
        if (current_actions == None): return
        keys = current_actions.keys()
        if "character_portrait_changes" in keys:
            character_mood = current_actions["character_portrait_changes"]
            temp = (self.portrait.image.width(), self.portrait.image.height())
            self.portrait.load_portrait(character_mood)
            self.portrait.update(temp[0], temp[1])
            # self.portrait.configure(image=self.photo.image)
            # self.portrait.image = self.photo.image
            self.canvas.itemconfigure(self.portrait_spot, image = self.portrait.image)
        if "user_options" in keys:
            user_options = current_actions["user_options"]
            if len(user_options) > len(self.canvas_user_options_textboxes):
                self._create_canvas(small_count=len(user_options))
            for i in range(len(self.canvas_user_options_textboxes)):
                if i < len(user_options):
                    self.canvas_user_options_textboxes[i].show(canvas=self.canvas)
                    self.canvas_user_options_textboxes[i].update_text(canvas=self.canvas, text=user_options[i])
                else:
                    self.canvas_user_options_textboxes[i].hide(canvas=self.canvas)
            # self.create_player_dialogue_frame(current_actions["user_options"])
        else:
            for a in self.canvas_user_options_textboxes:
                a.hide(canvas=self.canvas)
        if "character_speaks" in keys:
            self.canvas_textbox.show(canvas=self.canvas)
            self.Type(current_actions["character_speaks"])
        else:
            self.canvas_textbox.hide(canvas=self.canvas)
        if "note" in keys:
            self.canvas.delete("all")
            self.canvas.create_text(
                self.winfo_width()/2,
                self.winfo_height()/2,
                text=current_actions["note"],
                font=('Times New Roman', int(self.winfo_width() * 3/100), 'normal'),
            )

def parse_function(line, function_name):
    line : str = line.strip().removeprefix(function_name).removesuffix(")").strip().removeprefix("(")
    return [a.strip() for a in line.split(",")]

def get_their_code(filename : str = "test.py"):
    their_code = []
    with open(filename, "r") as f:
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

class Status(Enum):
    COMPLETED = 0
    PAUSED = 1
    CONTINUING = 2

class Code():
    def __init__(self, code : str, DEBUG : bool = False) -> None:
        self.DEBUG = DEBUG
        self._code : list[CodeSegment] = [CodeSegment(code)]
        self._update_active()

    def _update_active(self) -> None:
        self._active_code : CodeSegment = self._code[len(self._code)-1]
        if self.DEBUG: print("New focused line:")
        if self.DEBUG: print(f" {self._active_code.position}/{len(self._active_code.lines)}")
        if self.DEBUG: print(f" {self._active_code.lines[self._active_code.position]}")

    def indent(self, indent_code : list[str]) -> None:
        self._code.append(CodeSegment(indent_code))
        self._update_active()

    def change_DEBUG(self, DEBUG : bool) -> None:
        self.DEBUG = DEBUG

    def next(self) -> Status:
        self._active_code.next()
        while self._active_code.completed:
            if self.pop() == Status.COMPLETED:
                return Status.COMPLETED
        return Status.CONTINUING

    def is_if_statement(self):
        return self._active_code.is_if_statement()

    def pop(self) -> Status:
        self._code.pop()
        if self._code == []:
            return Status.COMPLETED
        self._update_active()
        return Status.CONTINUING

    def find_next_not_indented(self) -> Status:
        if self._active_code.find_next_not_indented() == Status.COMPLETED:
            return self.pop()
        return Status.CONTINUING

    def run_if_statement(self, boolean : bool):
        result = self._active_code.run_if_statement(boolean)
        if result == None: return
        if not type(result) == CodeSegment:
            raise Exception(f"Result should be a None or a CodeSegment\n result = {result}")
        self.indent(result)


    def replace_input_with(self, user_input):
        return self._active_code.replace_input_with(user_input)

    def is_completed(self):
        return self._code == []

    def detect_pause(self):
        return self._active_code.detect_pause()

    def run_to_pause_or_end(self, user_input : str = None):
        def check_functions(segment):
            for function in [print_character, print_player]:
                if segment.check_for_and_run_function(function):
                    return True
            return False

        if user_input:
            self.replace_input_with(user_input)
        while not self.is_completed():
            try:
                self._active_code.get_line()
            except:
                print(len(self._code))
                print(len(self._active_code.lines))
                print(self._active_code.position)

            if self.detect_pause():
                return Status.PAUSED
            elif check_functions(self._active_code): 
                self.next()
                continue
            elif (result := self.is_if_statement()) != None:
                print("is an if statement")
                if (result := self._active_code.run_if_statement(result)) != None:
                    self.indent(result)
                continue
            else:
                print(f"if statement result is {result}")
                print("Assuming must be of another line type")
                self._active_code.other_line_type()
            self.next()
        return Status.COMPLETED

class CodeSegment():
    def __init__(self, lines : list[str], position : int = 0, repeat = False, DEBUG : bool = False) -> None:
        self.lines = lines
        self.position = position
        self.repeat = repeat
        self.DEBUG = DEBUG
        self.completed = False

    def check_for_and_run_function(self, function):
        DEBUG = False
        def sort_parameters(full_list):
            def check_if_named(line):
                if "=" not in line:
                    return False
                temp = line[:line.index("=")]
                if "'" in temp or '"' in temp:
                    return False
                return True

            unnamed_parameters = []
            named_parameters = {}
            while len(full_list) > 0:
                input = full_list.pop(0)
                if check_if_named(input):
                    parameter, value = input.split("=")
                    named_parameters[parameter] = predict_and_convert_to_true_type(value)
                    continue
                else:
                    unnamed_parameters.append(predict_and_convert_to_true_type(input))
            return unnamed_parameters, named_parameters

        # Check if the line contains the function
        function_name = function.__name__
        if DEBUG: print(f"Checking line to see if it calls {function_name}...", end="")
        line = self.lines[self.position]
        if not line.startswith(function_name):
            if DEBUG: print(" Nope")
            return False
        if DEBUG: print(" Yep")
        # Extract the parameters
        full_list = parse_function(line, function_name)
        if DEBUG: print(f" All parameters: [{full_list}]")
        unnamed_parameters, named_parameters = sort_parameters(full_list)
        if DEBUG: print(f" Sorted into unnamed: {unnamed_parameters} and named: {named_parameters}")
        # Run the function
        function(*unnamed_parameters, **named_parameters)
        return True

    def change_DEBUG(self, DEBUG : bool) -> None:
        self.DEBUG = DEBUG

    def next(self) -> None:
        """
        Moves the position to the next line.\n
        - Returns COMPLETED if reaches end of CodeSegment by doing so.\n
        - Returns CONTINUING otherwise.
        """
        self.position += 1
        if self.position >= len(self.lines):
            self.completed = True
            return Status.COMPLETED
        Status.CONTINUING

    def get_line(self) -> str:
        return self.lines[self.position]

    def is_if_statement(self):
        """
        - returns None if not an if statement
        - returns the True/False falue of the statement if is an if statement
        note: if, elif, and else statements all count as a type of if statement for this function's purposes
        """
        def turn_line_into_True_or_False(line : str) -> bool:
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
            return line

        line = self.get_line()
        startsw = line.startswith("if")
        if line.startswith("else"):
            if not (line.strip() == "else:"):
                raise Exception('Incorrectly formated "else:"')
            line = "if True:"
        if not (line.startswith("if") or line.startswith("elif")):
            return None
        return turn_line_into_True_or_False(line)

    def run_if_statement(self, boolean):
        if self.DEBUG: print(f"If statement is {boolean}")
        if self.DEBUG: print(f" and line_i is {self.position}")
        if self.DEBUG: print(f" and the line is {print_line(self.lines, self.position)}")
        if boolean:
            # If statement is true
            self.next()
            if self.completed:
                raise Exception("If type statements must have some code under them.")
            # Grab all lines in the if
            indeneted_statements = []
            while(self.lines[self.position].startswith("    ")):
                indeneted_statements.append(self.lines[self.position].removeprefix("    "))
                self.next()
                if self.completed: break
            if self.completed:
                # Return the CodeSegment that was under the if
                return indeneted_statements
            # Skip over any elif or else statements after the if
            while self.lines[self.position].startswith("elif") or self.lines[self.position].startswith("else"):
                self.find_next_not_indented()
                if self.completed: break
            # Return the CodeSegment that was under the if
                # if self.DEBUG: print(f"{len(self.lines)}")
                # if self.DEBUG: print(f"line_i  is {self.position} ({print_line(self.lines, self.position)})")
            return indeneted_statements
        else:
            # If statement is false
            # Skip over all lines in the if
            self.find_next_not_indented()
            return None

    def find_next_not_indented(self) -> Status:
        """
        Moves the position to the next line that is not indented.\n
        - Returns COMPLETED if reaches end of CodeSegment by doing so.\n
        - Returns CONTINUING otherwise.
        """
        # At an if or elif statement
        # +1 moves to first line in the indent (1 line must exist, otherwise error in code editor)
        self.next()
        # Skip over each line with an indent
        while(self.position < len(self.lines) and self.lines[self.position].startswith("    ")):
            if self.next() == Status.COMPLETED:
                # Could have hit end of file
                return Status.COMPLETED
        # self.position should be set to next line not a part of the if or elif satement
        if self.DEBUG: print(f" and the next line not a part of the if is {print_line(self.lines, self.position)}")
        return Status.CONTINUING

    def detect_pause(self):
        line = self.get_line()
        return "input" in line and not ("'" in line or '"' in line)

    def replace_input_with(self, new_content):
        if (type(new_content)) == str:
            new_content = f'"{new_content}"'
        self.lines[self.position] = self.get_line().replace("input()", new_content)

    def other_line_type(self):
        DEBUG = True
        self.lines[self.position] = squish_array(split(self.get_line()), DEBUG=DEBUG)[0]

def print_line(lines, position):
    return lines[position] if position < len(lines) else "EOF"

def parse(their_code : list, user_selection = None, DEBUG = False) -> tuple[list, Status]:
    """
    """
    if their_code == []: return [], Status.COMPLETED
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
                    return their_code, Status.PAUSED
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
                            if DEBUG: print(f" and the line is {print_line(their_code_active, line_i)}")
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
                            if DEBUG: print(f"line_i  is {line_i } ({print_line(their_code_active, line_i)})")
                            their_code[len(their_code)-1][1] = line_i
                            their_code.append([child_statements, 0])
                            if DEBUG: print(f"running parse again with {len(child_statements)} child statements")
                            their_code, result  = parse(their_code)
                            # if (result == status.PAUSED):
                            return their_code, result
                            # their_code.pop()
                            # their_code_active = their_code[len(their_code)-1][0]
                            # line_i = their_code[len(their_code)-1][1]
                            # line_i += 1
                            continue
                        else:
                            if DEBUG: print(f"If statement {print_line(their_code_active, line_i)} is false")
                            line_i += 1
                            while(line_i < len(their_code_active) and their_code_active[line_i].startswith("    ")):
                                line_i += 1
                            if DEBUG: print(f" and the next line not a part of the if is {print_line(their_code_active, line_i)}")
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
    return their_code, Status.COMPLETED

def print_actions():
    # print()

    # for a in range(line_i):
    #     print(their_code[a])

    # print()

    for a in actions:
        print(a)

def flatten_text(*text):
    content : str = ""
    for i in range(len(text)):
        if i != 0:
            content += " "
        content += str(text[i])
    return content

def print_character(*text, mood : str = None):
    DEBUG = False
    parts = list(text)
    if len(parts) < 1:
        parts.append("")
    dictionary = {"character_speaks" : flatten_text(*text)}
    if mood:
        dictionary["character_portrait_changes"] = mood
        if DEBUG: print("mood changed")
    actions.append(dictionary)
    if DEBUG: print("action added")

def print_player(*text):
    DEBUG = False
    if len(actions) == 0: actions.append({})
    if "user_options" in actions[len(actions)-1].keys():
        actions[len(actions)-1]["user_options"] += [flatten_text(*text)]
    else:
        # actions[len(actions)-1]["user_options"] = [flatten_text(*text)]
        actions.append({"user_options" : [flatten_text(*text)]})
    if DEBUG: print("option added")

if __name__ == "__main__":
    their_code = Code(get_their_code())
    status = their_code.run_to_pause_or_end()
    Window(their_code)
    tk.mainloop()
