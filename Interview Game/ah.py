from __future__ import annotations
from PIL import ImageTk, Image
import urllib.request
import tkinter as tk
import time
import io
from enum import Enum
from code import load_code, Status

global character_mood
character_mood = "normal"

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
    "interview background" : "https://static.wikia.nocookie.net/slimerancher/images/8/8d/Slime_Rancher_Development_Nimble_Valley_1.png/revision/latest/smart/width/498/height/373?cb=20180221005815&path-prefix=ru", 
    "start game screen background" : "https://static.wikia.nocookie.net/slimerancher/images/e/e9/Mochi%27s_Manor_Official_Screenshot.jpg/revision/latest/smart/width/498/height/373?cb=20180621102816&path-prefix=ru", 
}

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
        return self

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
        return self

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

    def __str__(self):
        return f"<width={self.width}, height={self.height}>"

    def generate_from_event(event):
        return Dimentions(event.width, event.height)
    
    def __eq__(self, value: object) -> bool:
        E = Exception("A Dimensions object can only be compared to another Dimensions object, a tuple of two numbers, or a list of two numbers")
        if value == None: return False
        if type(value) == Dimentions:
            return (self.width == value.width and self.height == value.height)
        if type(value) == list or type(value) == tuple:
            if len(value) != 2:
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
        self.code = code
        # Used to allow the user to interupt typing out the character's text
        self.type_called_count = 0
        self.previous_event = None

        self.screen_dimentions = Dimentions(500, 500)
        self.geometry(f'{self.screen_dimentions.width}x{self.screen_dimentions.height}')

        self.page = IntroPage(self)
        self.character_name = "Mochi"
        # self.interivew_page.hide()
        # self.game_over_page = BlankPage(self)
        # self.game_over_page.hide()
        # self.next()

    def run(self):
        self.mainloop()

    # def fill_canvas(self):
    #     self.interivew_page.delete("all")
    #     self.portrait.update(self.screen_dimentions.width, self.screen_dimentions.height)
    #     self.available_size = Dimentions(self.portrait.width, self.portrait.height)
    #     new_offset = Dimentions(int((self.screen_dimentions.width-self.available_size.width)/2), int((self.screen_dimentions.height-self.available_size.height)/2))
    #     self.center_screen_offset = new_offset

    #     self.portrait_spot = self.interivew_page.create_image(
    #         self.center_screen_offset.width + (self.available_size.width - self.portrait.width)/2, 
    #         self.center_screen_offset.height + (self.available_size.height - self.portrait.height)/2, 
    #         image = self.portrait.image, anchor=tk.NW)

    #     self._create_canvas()

    # def _create_canvas(self, small_count : int | None = None):
    #     # self.canvas_objects = []
    #     if not small_count:
    #         self.canvas_textbox.add_to_canvas(self.available_size, self.interivew_page, self.center_screen_offset, self.next)
    #         return
    #     if small_count < 1:
    #         raise Exception("Must have at least one user option")
    #     self.canvas_user_options_textboxes = []
    #     for i in range(small_count):
    #         print(i)
    #         if i >= len(self.canvas_user_options_textboxes):
    #             print("adding textbox")
    #             self.canvas_user_options_textboxes.append(Textbox("Picture1Small.png"))
    #         print("adding to canvas")
    #         self.canvas_user_options_textboxes[i].add_to_canvas(self.available_size, self.interivew_page, self.center_screen_offset, lambda i = i: self.next(str(i+1)), shrink_factor= 4, count=i)

    # def _resize_widgets(self, event):
    #     if self.dont_change_size:
    #         return
    #     width = self.winfo_width()
    #     height = self.winfo_height()
    #     if not self.previous_event == None and self.previous_event[0] == width and self.previous_event[1] == height:
    #         return
    #     print(event)
    #     self.previous_event = (width, height)
    #     # # if not self.previous == (width, height):
    #     #     # self.previous = (width, height)
    #     # self.photo.update(width * 10/10, height * 10/10)
    #     # self.portrait.configure(image=self.photo.image)
    #     # self.displayed_text.configure(
    #     #     width=int(self.winfo_width()/15), 
    #     #     height=int(self.winfo_height()/100), 
    #     #     font=('Times New Roman', int(self.winfo_width()/50), 'bold'), 
    #     # )
    #     # self.spacer.configure(width=int((self.winfo_width() - self.portrait.winfo_width())/20))
    #     self.screen_dimentions = Dimentions(width, height)
    #     self.fill_canvas()

    def type(self, text="text"):
        self.type_called_count +=1
        my_type_called_count = self.type_called_count
        # Clear previous text
        # self.displayed_text["text"] = ""
        self.page.update_text("Mochi", "")
        # self.interivew_page.itemconfigure(self.canvas_textbox.text, text="")
        self.update()
        # Type out new text one character at a time.
        for i in range(len(text)+1):
            if my_type_called_count != self.type_called_count: return
            # self.displayed_text["text"] = text[0: i]
            # self.interivew_page.itemconfigure(self.canvas_textbox.text, text=text[0: i])
            self.page.update_text(self.character_name, text=text[0:i])
            self.update()
            time.sleep(0.05)

    def start_game(self):
        self.page.pack_forget()
        self.page = InterviewPage(self)
        self.page._resize_widgets(event=AllowedSpace(x=0, y=0))
        self.page._resize_widgets(event=AllowedSpace(x=0, y=0))
        self.next()


    def next(self, user_action = None):
        DEBUG = True

        if DEBUG and user_action: print(f"! A USER ACTION WAS GIVEN !\n   {user_action}")
        # if not self.available_size:
        #     self.fill_canvas()
        #     self.dont_change_size = False
        current_actions : dict = self.code.next_line(user_input = user_action)
        if DEBUG: print(current_actions)
        if (current_actions == Status.PAUSED): return
        if (current_actions == Status.COMPLETED) or not current_actions:
            current_actions = {"Note" : "Game Over"}
        keys = current_actions.keys()
        if "character_name_changes" in keys:
            self.character_name = current_actions["character_name_changes"]
        if "character_portrait_changes" in keys:
            character_mood : str = current_actions["character_portrait_changes"]
            # temp = (self.portrait.image.width(), self.portrait.image.height())
            # self.portrait.load_portrait(character_mood)
            # self.portrait.update(temp[0], temp[1])
            # # self.portrait.configure(image=self.photo.image)
            # # self.portrait.image = self.photo.image
            # self.interivew_page.itemconfigure(self.portrait_spot, image = self.portrait.image)
            self.page.update_portrait(character_mood)
        if "user_options" in keys:
            user_options : list[str] = current_actions["user_options"]
            # if len(user_options) > len(self.canvas_user_options_textboxes):
            #     self._create_canvas(small_count=len(user_options))
            # for i in range(len(self.canvas_user_options_textboxes)):
            #     if i < len(user_options):
            #         self.canvas_user_options_textboxes[i].show(canvas=self.interivew_page)
            #         self.canvas_user_options_textboxes[i].update_text(canvas=self.interivew_page, text=user_options[i])
            #     else:
            #         self.canvas_user_options_textboxes[i].hide(canvas=self.interivew_page)
            # # self.create_player_dialogue_frame(current_actions["user_options"])
            self.page.update_options(user_options)
            self.page.switch_to_options()
        # else:
        #     for a in self.canvas_user_options_textboxes:
        #         a.hide(canvas=self.interivew_page)
        if "character_speaks" in keys:
            # self.canvas_textbox.show(canvas=self.interivew_page)
            # self.Type(current_actions["character_speaks"])
            self.page.switch_to_character_speaking()
            self.type(text=current_actions["character_speaks"])
        # else:
        #     self.canvas_textbox.hide(canvas=self.interivew_page)
        if "Note" in keys:
            # self.interivew_page.delete("all")
            # self.interivew_page.create_text(
            #     self.winfo_width()/2,
            #     self.winfo_height()/2,
            #     text=current_actions["note"],
            #     font=('Times New Roman', int(self.winfo_width() * 3/100), 'normal'),
            # )
            self.page.pack_forget()
            self.page = BlankPage(parent=self)

class Page(tk.Canvas):
    def __init__(self, parent, widgets : list | None = None) -> None:
        tk.Canvas.__init__(self)
        self.parent = parent

        self.previous_event_space = None

        if widgets: self.widgets = widgets

        self.parent.bind("<Configure>", self._resize_widgets)

        self.configure(background="red")
        self.show()

        # These are named without _s so that children classes are less likely to cause a name conflict
        self.varsofself = None
        self.allwidgets = []

    def hide(self):
        self.pack_forget()

    def show(self):
        self.pack(fill=tk.BOTH, expand=True)

    def a(self, variable : Widget, so_far : list):
        if (issubclass(type(variable.relative_to), Widget)):
            if variable.relative_to not in so_far:
                self.a(variable.relative_to, so_far)
        if variable not in so_far:
            so_far.append(variable)

    def _get_widgets_that_need_resizing(self):
        DEBUG = False

        output = []
        self.varsofself = vars(self)
        for variable in self.varsofself.values():
                if (issubclass(type(variable), Widget)):
                    self.a(variable, output)
                if type(variable) == list or type(variable) == tuple or type(variable) == set:
                    for subvariable in variable:
                        if (issubclass(type(subvariable), Widget)):
                            self.a(subvariable, output)

        if DEBUG:
            print("Update Order:")
            for a in output:
                print("-", a)

        return output

    def widget_added(self):
        self.allwidgets = self._get_widgets_that_need_resizing()

    def _resize_widgets(self, event = None, force_refresh : bool = False):
        def call_resize(variable : Widget):
            if not variable.resize_status == Resize.NEEDED: return
            variable.resize()
            variable.resize_status = Resize.COMPLETE

        def set_resize_needed(variable : Widget):
            variable.resize_status = Resize.NEEDED

        # Checks if new widgets have been added dynamically
        if self.varsofself != vars(self):
            self.allwidgets = self._get_widgets_that_need_resizing()

        # Makes sure only updates the widget's sizes when needed. 
        #  For SOME REASON, the event sometimes gets fired twice in a row when the window is maximized or de-maximized. If 
        #  resizing is done on only one of these events, the widgets are not in their proper places. If it is done on both, 
        #  they are fine. The second event has x and y set to zero when maximize button pressed. The first has x and y set 
        #  to zero when the window is dragged to or away from the top of the screen as a shortcut for the maximize button.
        if not force_refresh:
            if not (event.x == 0 and event.y == 0):
                # Check to see if same size as before
                current_space = self.get_size()
                if self.previous_event_space == current_space:
                    return
                self.previous_event_space = current_space

        # Resizes all the widgets
        for variable in self.allwidgets:
            set_resize_needed(variable)
        for variable in self.allwidgets:
            call_resize(variable)

    def get_size(self):
        return Dimentions(self.parent.winfo_width(), self.parent.winfo_height())

    def get_position(self):
        return (0, 0)

class Resize(Enum):
    COMPLETE = "This object has been resized"
    IN_PROCESS = "The resize function is being called"
    NEEDED = "This object needs to be resized"
    DONT = "This object does not get resized"

class Positioned(Enum):
    BACKGROUND = "Fills full available space if possible"
    CENTERED = "Centered"
    ABOVE = "Directly above given object"
    RIGHT = "Directly to the right of the given object"
    LEFT = "Directly to the left of the given object"
    BELOW = "Directly below given object"
    INSIDE = "Inside a space with given percent or pixels off upper left corner"

class Alignment(Enum):
    TOPRIGHT = "top right"
    TOPLEFT = "top left"
    BOTTOMRIGHT = "bottom right"
    BOTTOMLEFT = "bottom left"
    TOP = "top"
    RIGHT = "right"
    LEFT = "left"
    BOTTOM = "bottom"
    CENTER = "center"

    def contains(self, alignment) -> bool:
        if alignment == self: return True
        if alignment == Alignment.TOP:
            return self == Alignment.TOPRIGHT or self == Alignment.TOPLEFT
        if alignment == Alignment.BOTTOM:
            return self == Alignment.BOTTOMLEFT or self == Alignment.BOTTOMRIGHT
        if alignment == Alignment.RIGHT:
            return self == Alignment.TOPRIGHT or self == Alignment.BOTTOMRIGHT
        if alignment == Alignment.LEFT:
            return self == Alignment.TOPLEFT or self == Alignment.BOTTOMLEFT
        if alignment == Alignment.CENTER:
            return self == Alignment.TOP or self == Alignment.BOTTOM or self == Alignment.RIGHT or self == Alignment.LEFT


class AllowedSpace(Dimentions):
    def __init__(self, dimensions : Dimentions = None, width: int = 0, height: int = 0, x : float = 0, y : float = 0) -> None:
        super().__init__(dimensions.width if dimensions else width, dimensions.height if dimensions else height)
        self.x : float = x
        self.y : float = y

    def get_size(self):
        return Dimentions(self.width, self.height)

    def get_position(self):
        return (self.x, self.y)

class Side(Enum):
    TOP = 0
    BOTTOM = 1
    LEFT = 2
    RIGHT = 3

class FontDetails():
    def __init__(self, font : str = 'Times New Roman', font_size : int = 10, effect : str = "normal", ):
        self.font = font
        self.font_size = font_size
        self.effect = effect

    def updateFont(self, font_size : int | None = None, font : str | None = None, effect : str | None = None):
        if font: self.font = font
        if font_size: self.font_size = font_size
        if effect: self.effect = effect
        return self

    def to_tuple(self):
        return (self.font, self.font_size, self.effect)

    def to_tuple_pixels(self, relative_to : Widget | AllowedSpace):
        return (self.font, self._convert_font_size_to_pixels(relative_to), self.effect)

    def _convert_font_size_to_pixels(self, relative_to : Widget | AllowedSpace) -> int:
        return int(relative_to.get_size().width/500 * self.font_size)

class Position():
    PINNED = "Attached to a side of the screen"
    def __init__(self, 
            positioned : Positioned = None, 
            x__pixel_offset_from_left : float | int = None, 
            y__pixel_offset_from_top : float | int = None, 
            x__percent_offset_from_left : float | int = None, 
            y__percent_offset_from_top : float | int = None, 
            # x__padding_pixel : float | int = None,
            # y__padding_pixel : float | int = None,
            # x__padding_percent : float | int = None,
            # y__padding_percent : float | int = None,
        ) -> None:
        self.positioned : Positioned = positioned
        self.x_offset : float | int = x__pixel_offset_from_left
        self.y_offset : float | int  = y__pixel_offset_from_top
        self.x_percent : float | int = x__percent_offset_from_left
        self.y_percent : float | int = y__percent_offset_from_top

        # self.x__padding_pixel : float | int = x__padding_pixel
        # self.y__padding_pixel : float | int  = y__padding_pixel
        # self.x__padding_percent : float | int = x__padding_percent
        # self.y__padding_percent : float | int = y__padding_percent

        if self.positioned == Positioned.CENTERED:
            self.positioned = Positioned.INSIDE
            self.x_percent = 1/2
            self.y_percent = 1/2

    def __eq__(self, value: object) -> bool:
        if type(value) != Position:
            return False
        return self.positioned == value.positioned

    def _get_alignment(object_size : Dimentions, alignment : Alignment):
        dx = 0
        dy = 0
        if alignment.contains(Alignment.CENTER):
            dx = -object_size.width/2
            dy = -object_size.height/2
        if alignment.contains(Alignment.TOP):
            dy = 0
        if alignment.contains(Alignment.BOTTOM):
            dy = -object_size.height
        if alignment.contains(Alignment.RIGHT):
            dx = -object_size.width
        if alignment.contains(Alignment.LEFT):
            dx = 0
        return dx, dy

    def _get_position_before_alignment(position : Position, object_size : Dimentions, relative_to : Widget | AllowedSpace | None):
        DEBUG = False

        if relative_to == None:
            if DEBUG: print("self.relative_to == None")
            if position.positioned == Positioned.INSIDE:
                raise Exception("If position set to Position.INSIDE, must give a widget for the widget to be placed inside")
            if position.positioned == Positioned.BACKGROUND:
                return (0, 0)
            x = position.x_offset if position.x_offset != None else 0
            y = position.y_offset if position.y_offset != None else 0
            return (x, y)
        if position.positioned == Positioned.BACKGROUND:
            if DEBUG: print("self.positioned == Positioned.BACKGROUND")
            return relative_to.get_position()
        if position.positioned == Positioned.INSIDE:
            if DEBUG: print("self.positioned == Positioned.INSIDE")
            if DEBUG: print(relative_to)
            x, y = relative_to.get_position()

            # Get size only if needed
            if position.x_percent != None or position.y_percent != None:
                size = relative_to.get_size()

            if position.x_percent != None:
                x += size.width * position.x_percent
            elif position.x_offset != None:
                x += position.x_offset

            if position.y_percent != None:
                y += size.height * position.y_percent
            elif position.y_offset != None:
                y += position.y_offset

            return (x, y)
        if position.positioned == Positioned.BELOW:
            if DEBUG: print("self.positioned == Positioned.BELOW")
            x, y  = relative_to.get_position()
            size = relative_to.get_size()
            y += object_size.height
            if position.x_offset != None:
                x += position.x_offset
            if position.y_offset != None:
                y += position.y_offset
            if position.x_percent != None:
                x += size.width * position.x_percent
            if position.y_percent != None:
                y += size.height * position.y_percent
        if position.positioned == Positioned.ABOVE:
            if DEBUG: print("self.positioned == Positioned.ABOVE")
            x, y  = relative_to.get_position()
            size = relative_to.get_size()
            y -= object_size.height
            if position.x_offset != None:
                x += position.x_offset
            if position.y_offset != None:
                y -= position.y_offset
            if position.x_percent != None:
                x += size.width * position.x_percent
            if position.y_percent != None:
                y += size.height * position.y_percent
            return (x, y)
        if not position.positioned:
            if DEBUG: print("not Positioned")
            return (position.x_offset, position.y_offset)

class ProportionalDimentions(Dimentions):
    def __init__(self, width: float = 0, height: float = 0) -> None:
        super().__init__(width, height)
    
    def to_real_size(self, proportional_to : AllowedSpace | Dimentions | tuple | list):
        if not proportional_to:
            raise Exception("Must provide something to be proportional to")
        pttype = type(proportional_to)
        if pttype == AllowedSpace or pttype == Dimentions:
            return Dimentions(proportional_to.width * self.width, proportional_to.height * self.height)
        return Dimentions(proportional_to[0] * self.width, proportional_to[1] * self.height)

class Widget():
    def __init__(self, 
            canvas : Page, resize : Resize = Resize.NEEDED, position : Position = None, 
            alignment : Alignment = Alignment.CENTER, relative_to : Widget | AllowedSpace = None,
            size : ProportionalDimentions = ProportionalDimentions(width = 1, height = 1), 
            padding : Padding = None
        ):
        self.canvas = canvas
        self.resize_status = resize
        self.position = position if position else Position()
        self.alignment = alignment
        self.relative_to = relative_to if relative_to else canvas
        self.size : ProportionalDimentions = size
        self.padding = padding if padding else Padding()
        self.current_position = None
        self.visible = True

    def get_size(self) -> Dimentions:
        x1, y1, x2, y2 = self.canvas.bbox(self.id)
        return Dimentions(x2 - x1, y2 - y1)

    def is_visible(self) -> bool:
        if not self.visible: return False
        if self.relative_to:
            if issubclass(type(self.relative_to), Widget):
                if not self.relative_to.is_visible(): return False
        return True

    def resize(self, *ids):
        # Not just an optimization. Tkinter throws errors if trying to get the size of a non visible widget
        if not self.is_visible(): return

        # Resizes widget
        self.resize_status = Resize.IN_PROCESS
        for id in ids:
            self._update_current_poisition()
            self.canvas.moveto(id, *self.current_position)

    def set_on_click(self, function):
        if function != None:
            self.canvas.tag_bind(self.id, '<Button-1>', lambda _: function())
        return self

    def get_space_this_widget_takes_up(self):
        size = self.get_size()
        x, y = self.get_position()
        return AllowedSpace(width=size.width, height=size.height, x=x, y=y)

    def get_position(self) -> tuple[int, int]:
        if self.current_position == None:
            print(f"UH OH. RELYS ON SOMETHING THAT HAS NOT BEEN SET UP YET. \nTHIS SHOULD NOT HAPPEN BECAUSE OF THE UPDATE ORDER.")
            return self._update_current_poisition()
        return self.current_position

    def _update_current_poisition(self):
        object_size = self.get_size()
        x, y = Position._get_position_before_alignment(position=self.position, object_size=object_size, relative_to=self.relative_to)
        ax, ay = Position._get_alignment(object_size, self.alignment)
        px, py = self.padding.get_padding_delta(self.position.positioned, object_size, position_so_far=(x + ax, y + ay), available_space=self.relative_to.get_size())
        self.current_position = (x + ax + px, y + ay + py)
        return self.current_position

    def get_widget_size(self) -> Dimentions:
        return self.size.to_real_size(self.relative_to.get_size())

    def _change_visability(self, visibility : bool):
        self.visible = visibility
        self.canvas.itemconfigure(self.id, state='normal' if visibility else 'hidden')

    def show(self):
        return self._change_visability(True)

    def hide(self):
        return self._change_visability(False)

class TextWidget(Widget):
    def __init__(self, 
                 canvas : Page, 
                 text : str = "", 
                 font_details : FontDetails = None,
                 text_alignment : str = "left", 
                 position : Position = None,
                 alignment : Alignment = Alignment.CENTER, 
                 relative_to : Widget | AllowedSpace = None,
                 size : ProportionalDimentions = ProportionalDimentions(width = 1, height = 1),
                 padding : Padding = None
            ) -> None:
        Widget.__init__(self, canvas, position=position, alignment=alignment, relative_to=relative_to, size=size, padding=padding)
        self.font_details : FontDetails = font_details
        self.id = canvas.create_text(0, 0, text=text, font=(self.font_details.font, self.font_details.font_size, self.font_details.effect), justify=text_alignment)

    def __str__(self):
        return f"Text widget ({self.id})"

    def set_font(self, 
            font_size : int | None = None, 
            font : str | None = None, 
            effect : str | None = None,
            new_font : FontDetails | None = None,
        ):
        # Update font
        if new_font:
            self.font_details = new_font
        else:
            self.font_details.updateFont(font_size, font, effect)

        # Update visuals to refect new font
        self.update_font()
        
        if (font_size != None or font != None or effect != None or new_font != None):
            # If font size is different, may need to move the text widget so that it is still properly aligned
            self.resize()
        return self

    def set_text_alignment(self, alignment : str | None = None):
        if alignment != None: 
            self.canvas.itemconfigure(self.id, justify=alignment)
        return self

    def set_text(self, text : str | None = None):
        if text != None:
            self.canvas.itemconfigure(self.id, text = text)
            self.resize()
        return self

    def update_font(self):
        self.canvas.itemconfigure(self.id, font = self.font_details.to_tuple_pixels(self.relative_to))

    def resize(self):
        super().resize(self.id)
        if not self.is_visible(): return

        self.update_font()
        # widget_size : Dimentions = self.get_size()
        # screen : Dimentions = self.canvas.get_size()
        # self.position.relative_to = AllowedSpace(dimensions=screen)
        
        # self.canvas.moveto(self.id, screen.width/2 - widget_size.width/2, screen.height/2 - widget_size.height/2)


class DebugWidget(Widget):
    def __init__(self, canvas: Page, DEBUG : bool = False, vertical_lines : int | bool = True, horizontal_lines : int | bool = True, lines : tuple[int, int] | None = None):
        super().__init__(canvas)
        self.enabled = DEBUG
        if not self.enabled: return

        vertical_lines_count = vertical_lines if type(vertical_lines) == int else (1 if vertical_lines else 0)
        if lines: vertical_lines_count = lines[1]
        self.add_vertical_lines(vertical_lines_count, Dimentions(1, 1))

        horizontal_lines_count = horizontal_lines if type(horizontal_lines) == int else (1 if horizontal_lines else 0)
        if lines: horizontal_lines_count = lines[0]
        self.add_horiztonal_lines(horizontal_lines_count, Dimentions(1, 1))

    def add_vertical_lines(self, count : int, screen : Dimentions):
        self.vertical_lines = []
        number_of_lines = count + 1
        for i in range(count):
            self.vertical_lines.append(self.canvas.create_line((screen.width * (i+1)/number_of_lines, 0), (screen.width * (i+1)/number_of_lines, screen.height), fill="blue"))

    def add_horiztonal_lines(self, count : int, screen : Dimentions):
        self.horizontal_lines = []
        number_of_lines = count + 1
        for i in range(count):
            self.horizontal_lines.append(self.canvas.create_line((0, screen.height * (i+1)/number_of_lines), (screen.width, screen.height * (i+1)/number_of_lines), fill="blue"))

    def resize(self):
        super().resize()

        if not self.enabled: return
        screen = self.canvas.get_size()
        
        vertical_lines_count = len(self.vertical_lines)
        for line in self.vertical_lines:
            self.canvas.delete(line)
        self.add_vertical_lines(vertical_lines_count, screen)

        horizontal_lines_count = len(self.horizontal_lines)
        for line in self.horizontal_lines:
            self.canvas.delete(line)
        self.add_horiztonal_lines(horizontal_lines_count, screen)

class Padding():
    def __init__(self, 
            top__pixels : int = None, 
            top__percent : float = None, 
            bottom__pixels : int = None, 
            bottom__percent : float = None, 
            left__pixels : int = None, 
            left__percent : float = None, 
            right__pixels : int = None, 
            right__percent : float = None, 
        ) -> None:
        self.top__pixels = top__pixels
        self.top__percent = top__percent
        self.bottom__pixels = bottom__pixels
        self.bottom__percent = bottom__percent
        self.left__pixels = left__pixels
        self.left__percent = left__percent
        self.right__pixels = right__pixels
        self.right__percent = right__percent

    def get_padding_delta(self, 
            position : Positioned, 
            widget_size : Dimentions, 
            position_so_far : tuple[float, float],
            available_space : Dimentions,
        ):
        if position == Positioned.INSIDE:
            positioned = []
            x, y = position_so_far
            midway_point_x = available_space.width/2
            midway_point_y = available_space.height/2
            if x > midway_point_x:
                positioned.append(Positioned.RIGHT)
            else:
                positioned.append(Positioned.LEFT)
            if y > midway_point_y:
                positioned.append(Positioned.ABOVE)
            else:
                positioned.append(Positioned.BELOW)
        else:
            positioned = [position]

        dx = 0
        dy = 0
        if Positioned.BELOW in positioned:
            if self.top__pixels:
                dy += self.top__pixels
            if self.top__percent:
                dy += widget_size.height * self.top__percent
        if Positioned.ABOVE in positioned:
            if self.bottom__pixels:
                dy -= self.bottom__pixels
            if self.bottom__percent:
                dy -= widget_size.height * self.bottom__percent
        if Positioned.RIGHT in positioned:
            if self.left__pixels:
                dx += self.left__pixels
            if self.left__percent:
                dx + widget_size.width * self.left__percent
        if Positioned.LEFT in positioned:
            if self.right__pixels:
                dx -= self.right__pixels
            if self.right__percent:
                dx -= widget_size.width * self.right__percent

        return (dx, dy)


class InterviewPage(Page):
    def __init__(self, parent):
        Page.__init__(self, parent)
        self.background = ImageWidget(
            canvas=self,
            photo=Photo().load_portrait("interview background"),
            position=Position(positioned=Positioned.BACKGROUND),
            size=ProportionalDimentions(1, 1),
            alignment=Alignment.TOPLEFT,
            keep_image_ratio=False,
        )
        self.portrait = ImageWidget(
            canvas=self, 
            photo=Photo().load_portrait("confident"), 
            position=Position(positioned=Positioned.CENTERED)
        )
        self.textbox = ImageWidget(
            canvas=self, 
            photo=Photo().load_image("Picture1.png"), 
            position=Position(positioned=Positioned.INSIDE, x__percent_offset_from_left=1/2, y__percent_offset_from_top=1),
            alignment=Alignment.BOTTOM, 
            padding=Padding(bottom__percent=1/30), 
            size = ProportionalDimentions(2/3, 1/3), 
            relative_to=self.portrait, 
            keep_image_ratio=False,
        ).set_on_click(function=parent.next)
        self.character_name = TextWidget(
            canvas=self, text="MOCHI", 
            font_details=FontDetails(font_size=20, effect="bold"), 
            text_alignment="left", 
            position = Position(positioned=Positioned.INSIDE, x__percent_offset_from_left=1/15, y__percent_offset_from_top=1/15),
            relative_to=self.textbox, 
            alignment=Alignment.TOPLEFT,
        )
        self.main_text = TextWidget(
            canvas=self, text="whatever",
            font_details=FontDetails(font_size=20),
            text_alignment="left", 
            position = Position(positioned=Positioned.INSIDE, x__percent_offset_from_left=1/15, y__percent_offset_from_top=1/5),
            relative_to=self.textbox, 
            alignment=Alignment.TOPLEFT,
        )
        self.texts = []
        self.small_textboxes = [
            ImageWidget(
                canvas=self, 
                photo=Photo().load_image("Picture1SmallUpgraded.png"), 
                name = "Bottom textbox",
                position=Position(positioned=Positioned.INSIDE, x__percent_offset_from_left=1/2, y__percent_offset_from_top=1),
                alignment=Alignment.BOTTOM, 
                padding=Padding(bottom__percent=1/10), 
                size = ProportionalDimentions(2/3, 1/10), 
                relative_to=self.portrait, 
                keep_image_ratio=False,
            )
        ]
        self._add_text(0)
        for a in range(2):
            self._add_textbox()
        self.small_textboxes.reverse()
        self.texts.reverse()
        self.DEBUG = DebugWidget(canvas=self, DEBUG = False)
        for a in self.small_textboxes: a.hide()
        for a in self.texts: a.hide()

    def _add_textbox(self):
        self.small_textboxes.append(
                ImageWidget(
                    canvas=self, 
                    photo=Photo().load_image("Picture1SmallUpgraded.png"), 
                    name = f"textbox number {len(self.small_textboxes)}",
                    position=Position(positioned=Positioned.ABOVE),
                    alignment=Alignment.TOPLEFT, 
                    padding=Padding(bottom__percent=1/20), 
                    relative_to=self.small_textboxes[len(self.small_textboxes)-1], 
                    keep_image_ratio=False,
                )
            )
        self._add_text(len(self.small_textboxes)-1)
    
    def _add_text(self, i):
        self.texts.append(TextWidget(
            canvas=self, text="Option 3",
            font_details=FontDetails(font_size=20),
            text_alignment="center",
            position=Position(positioned=Positioned.INSIDE, x__percent_offset_from_left=1/15, y__percent_offset_from_top=1/5),
            relative_to=self.small_textboxes[i],
            alignment=Alignment.TOPLEFT,
            # padding=Padding(top__percent=0.5, left__percent=0.5),
        ))

    def update_options(self, options : list[str]) -> None:
        if len(options) < 1: return
        while not len(options) == len(self.small_textboxes):
            if len(options) > len(self.small_textboxes):
                self.small_textboxes = [
                    ImageWidget(
                        canvas=self, 
                        photo=Photo().load_image("Picture1SmallUpgraded.png"), 
                        name = f"textbox number {len(self.small_textboxes)}",
                        position=Position(positioned=Positioned.ABOVE),
                        alignment=Alignment.TOPLEFT, 
                        padding=Padding(bottom__percent=1/20), 
                        relative_to=self.small_textboxes[0], 
                        keep_image_ratio=False,
                    )
                ] + self.small_textboxes
                self.texts = [TextWidget(
                    canvas=self, text=f"Option {len(self.texts)}",
                    font_details=FontDetails(font_size=20),
                    text_alignment="center",
                    position=Position(positioned=Positioned.INSIDE, x__percent_offset_from_left=1/15, y__percent_offset_from_top=1/5),
                    relative_to=self.small_textboxes[0],
                    alignment=Alignment.TOPLEFT,
                    # padding=Padding(top__percent=0.5, left__percent=0.5),
                )] + self.texts
                self.widget_added()
            elif len(options) < len(self.small_textboxes):
                l : Widget = self.small_textboxes.pop(0)
                self.delete(l)
                l : Widget = self.texts.pop(0)
                self.delete(l)
        for i in range(len(self.texts)):
            self.texts[i].set_text(options[i])
            self.small_textboxes[i].set_on_click(function= lambda i = i: self.parent.next(str(i+1)))

    def update_text(self, character_name, text) -> None:
        self.character_name.set_text(character_name)
        self.main_text.set_text(text)

    def update_portrait(self, new_portrait : str) -> None:
        self.portrait.update_portrait(new_portrait)

    def switch_to_options(self) -> None:
        for a in self.small_textboxes: a.show()
        for a in self.texts:a.show()
        for a in [self.textbox, self.character_name, self.main_text]: a.hide()
        self.update()

    def switch_to_character_speaking(self) -> None:
        for a in self.small_textboxes: a.hide()
        for a in self.texts: a.hide()
        for a in [self.textbox, self.character_name, self.main_text]: a.show()
        self.update()

    def update(self):
        self._resize_widgets(event=AllowedSpace(x = 0, y = 0))
        self._resize_widgets(event=AllowedSpace(x = 0, y = 0))

class IntroPage(Page):
    def __init__(self, parent):
        Page.__init__(self, parent)
        self.background = ImageWidget(
            canvas=self,
            photo=Photo().load_portrait("start game screen background"),
            position=Position(positioned=Positioned.BACKGROUND),
            size=ProportionalDimentions(1, 1),
            alignment=Alignment.TOPLEFT,
            keep_image_ratio=False,
        )
        self.text_textbox= ImageWidget(
            canvas=self, 
            photo=Photo().load_image("Picture1SmallUpgraded.png"), 
            name = "Bottom textbox",
            position=Position(positioned=Positioned.INSIDE, x__percent_offset_from_left=1/2, y__percent_offset_from_top=1/4),
            alignment=Alignment.CENTER, 
            size = ProportionalDimentions(2/3, 1/9), 
            keep_image_ratio=False,
        )
        self.text = TextWidget(
            canvas=self, text="The INTERVIEW",
            font_details=FontDetails(font_size=25, effect="bold"),
            text_alignment="center",
            position = Position(positioned=Positioned.INSIDE, x__percent_offset_from_left=1/2, y__percent_offset_from_top=1/4),
            alignment=Alignment.CENTER
        )
        self.start_button_textbox= ImageWidget(
            canvas=self, 
            photo=Photo().load_image("Picture1SmallUpgraded.png"), 
            name = "Bottom textbox",
            position=Position(positioned=Positioned.INSIDE, x__percent_offset_from_left=1/2, y__percent_offset_from_top=3/4),
            alignment=Alignment.CENTER, 
            size = ProportionalDimentions(1.5/6, 1/10), 
            keep_image_ratio=False,
        )
        self.start_button = TextWidget(
            canvas=self, text="Start",
            font_details=FontDetails(font_size=25, effect="bold"),
            text_alignment="center",
            position = Position(positioned=Positioned.INSIDE, x__percent_offset_from_left=1/2, y__percent_offset_from_top=3/4),
            alignment=Alignment.CENTER
        ).set_on_click(parent.start_game)

class BlankPage(Page):
    def __init__(self, parent):
        Page.__init__(self, parent)
        self.background = ImageWidget(
            canvas=self,
            photo=Photo().load_portrait("start game screen background"),
            position=Position(positioned=Positioned.BACKGROUND),
            size=ProportionalDimentions(1, 1),
            alignment=Alignment.TOPLEFT,
            keep_image_ratio=False,
        )
        self.text = TextWidget(
            canvas=self, text="GAME OVER",
            font_details=FontDetails(font_size=35, effect="bold"),
            text_alignment="center",
            position = Position(positioned=Positioned.INSIDE, x__percent_offset_from_left=1/2, y__percent_offset_from_top=1/2),
            alignment=Alignment.CENTER
        )


class ImageWidget(Widget):
    def __init__(self, 
                canvas: Page, 
                photo: Photo | None,
                name : str = "ImageWidget",
                resize: Resize = Resize.NEEDED, 
                position: Position = None, 
                size : ProportionalDimentions = ProportionalDimentions(width = 1, height = 1), 
                alignment: Alignment = Alignment.CENTER, 
                relative_to : Widget | AllowedSpace = None,
                padding : Padding = None, 
                keep_image_ratio : bool = True,
            ):
        super().__init__(canvas, resize, position, alignment, relative_to=relative_to, size=size, padding=padding)
        self.name = name

        self.keep_image_ratio = keep_image_ratio

        if photo == None:
            raise Exception("Must provide a photo of some kind. Provided None.")
        self.photo = photo

        self.id = self.canvas.create_image(0, 0, image = self.photo.image, anchor=tk.NW)

    def update_portrait(self, new_portrait):
        temp = (self.photo.image.width(), self.photo.image.height())
        self.photo.load_portrait(new_portrait)
        self.photo.update(temp[0], temp[1])
        self.canvas.itemconfigure(self.id, image = self.photo.image)

    def __str__(self):
        return f"{self.id} == {self.name}"

    def resize(self):
        super().resize(self.id)
        if not self.is_visible(): return

        real_size = self.get_widget_size()
        if self.keep_image_ratio:
            self.photo.update(real_size.width, real_size.height)
        else:
            self.photo.force_resize(real_size.width, real_size.height)
        self.canvas.itemconfigure(self.id, image = self.photo.image)

import sys

if __name__ == "__main__":
    window = Window(code=load_code(sys.argv[1] if len(sys.argv) > 1 else "test.py"))
    window.run()
