import tkinter as tk
from PIL import ImageTk, Image

class suspect():
    def __init__(self, name, location, default_dialogue, questions = ["?", "?", "?"], answers=["?", "?", "?"], is_villian = False):
        self.name = name
        self.location = location
        self.default_dialogue = default_dialogue
        self.questions = questions
        self.answers = answers
        self.selected = []
        self.is_villian = is_villian

class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.resizable(False, False)
        self._frame = None
        self.geometry("460x550")
        self.switch_frame(StartPage)
        self.configure(bg='#fefbdc')

    def switch_frame(self, frame_class, suspect = None):
        """Destroys current frame and replaces it with a new one."""
        if self._frame is not None:
            self._frame.destroy()
        if (suspect):
            self._frame = frame_class(self, suspect)
        else:
            self._frame = frame_class(self)
        self._frame.pack()

class StartPage(tk.Frame):
    def __init__(self, app):
        tk.Frame.__init__(self, app)
        # Create the image
        self.image = load_image('Artwork\\Title Image Pixel Art.png', (460, 550))
        img_label = tk.Label(self, image=self.image, borderwidth=0)
        img_label.grid(row=0, column=0, rowspan=3)

        l = tk.Label(self, text="DETECTIVE GAME", font=('Helvetica', 32, "bold"))
        l.grid(row=0, column=0)

        b = tk.Button(self, text="Start", command=lambda: app.switch_frame(MapPage), font=('Helvetica', 12))
        b.grid(row=2, column=0)

class MapPage(tk.Frame):
    def __init__(self, app):
        tk.Frame.__init__(self, app)
        tk.Frame.configure(self, bg='#fefbdc')

        # Create the image
        self.imageBorder = load_image(f'Artwork\\imageBorder.png', (400, 400))
        img_border = tk.Label(self, image=self.imageBorder, borderwidth=0, background='#fefbdc')
        img_border.grid(row=1, column=0, rowspan=20, columnspan=20, pady=10)
        self.image = load_image('Artwork\\House Layout.png', (381, 381))
        img_label = tk.Label(self, image=self.image, borderwidth=0)
        img_label.grid(row=1, column=0, rowspan=20, columnspan=20, pady=10)

        self.title_background = load_image(f'Artwork\\bigTextBar.png', (225, 50))
        l = tk.Label(self, text="The Map", font=('Helvetica', 24, "bold"), image=self.title_background, compound="center", background='#fefbdc', borderwidth=0)
        l.grid(row=0, column=0, columnspan=20)

        for a in suspects:
            b = tk.Button(self, text=a.name, command=lambda suspect = a: app.switch_frame(SuspectPage, suspect), fg="black", background="#947bad")
            b.grid(row=a.location[0], column=a.location[1])

        self.accuse_button = load_image(f'Artwork\\bigTextBar.png', (150, 35))
        l = tk.Button(self, text="Accuse", font=('Helvetica', 15), command=lambda : app.switch_frame(AccusePage), image=self.accuse_button, compound="center", background='#fefbdc', borderwidth=0)
        l.grid(row=21, column=0, columnspan=20)

class SuspectPage(tk.Frame):
    def __init__(self, app, suspect):
        tk.Frame.__init__(self, app)
        tk.Frame.configure(self, bg='#fefbdc')

        def switch_buttons(button):
            if (button == 0):
                app.switch_frame(MapPage)
            elif (button == 1):
                app.switch_frame(NotesPage, suspect)
            else:
                app.switch_frame(MapPage)
        
        def update_dialogue(suspect, i):
            self.text_box["text"] = suspect.answers[i]
            suspect.selected.append(i)

        # Create three buttons
        for i in range(3):
            if (i == 0):
                self.backbutton = load_image(f'Artwork\\BackButton.png', (75, 75))
                temp_button = self.backbutton
            if (i == 1):
                self.notesbutton = load_image(f'Artwork\\NotesButton.png', (75, 75))
                temp_button = self.notesbutton
            if (i == 2):
                self.homebutton = load_image(f'Artwork\\HomeButton.png', (75, 75))
                temp_button = self.homebutton
            button = tk.Button(self, command=lambda input_var=i: switch_buttons(input_var), image=temp_button, borderwidth=0, background='#fefbdc')
            # button = tk.Button(self, text=f'Button {i+1}', command=lambda input_var=i: switch_buttons(input_var))
            button.grid(row=i, column=0, padx=25)

        # Create the image
        self.imageBorder = load_image(f'Artwork\\imageBorder.png', (300, 300))
        img_label = tk.Label(self, image=self.imageBorder, borderwidth=0, background='#fefbdc')
        img_label.grid(row=0, column=1, rowspan=3, pady=15)
        self.image = load_image(f'Artwork\\{suspect.name}.png', (286, 286))
        img_label = tk.Label(self, image=self.image, borderwidth=0)
        img_label.grid(row=0, column=1, rowspan=3, pady=15)

        text_box = tk.Label(self, text=suspect.name, background="black", foreground="white")
        text_box.grid(row=2, column=1, columnspan=2, sticky="s")

        self.dialogue_background = load_image(f'Artwork\\bigTextBar.png', (425, 74))
        self.text_box = tk.Label(self, text=suspect.default_dialogue, image=self.dialogue_background, borderwidth=0, background='#fefbdc', compound='center',  font=('Helvetica', 16, "bold"), justify='left', wraplength=425)
        self.text_box.grid(row=3, column=0, pady=5, columnspan=2)

        # # Create three text boxes
        self.background_images = []
        for i in range(3):
            frame = tk.Frame(self, background='#fefbdc')
            frame.grid(row=4 + i, column=0, columnspan=2, pady=2.5)
            frame.columnconfigure(0, weight=1, minsize=50)
            frame.columnconfigure(1, weight=10, minsize=350)

            selected_status = "notS"
            if (i in suspect.selected):
                selected_status = "S"

            text = suspect.questions[i]

            height = 37 * (text.count("\n") + 1)
            self.background_images.append((load_image(f'Artwork\\{selected_status}electedButton.png', (height, height)), load_image(f'Artwork\\{selected_status}electedSmallTextBar.png', (75*5, height))))

            button = tk.Button(frame, text="Select", image=self.background_images[i][0], borderwidth=0, background='#fefbdc', command=lambda i = i: update_dialogue(suspect, i))
            button.grid(row=0, column=0)

            label = tk.Label(frame, text=text, image=self.background_images[i][1], borderwidth=0, background='#fefbdc', compound='center',  font=('Helvetica', 16, "bold"))
            label.grid(row=0, column=1)

class NotesPage(tk.Frame):
    def __init__(self, app, suspect):
        tk.Frame.__init__(self, app)
        tk.Frame.configure(self, bg='#fefbdc')
        contents = ""
        with open("notes.txt", "r") as f:
            contents = f.read()
        def back():
            with open("notes.txt", "w") as f:
                f.write(text.get("1.0", "end"))
            app.switch_frame(SuspectPage, suspect)
        tk.Button(self, text="Back", command=back).pack()
        text = tk.Text(self, width=100, height=10)
        text.insert("1.0", contents)
        text.pack()

class AccusePage(tk.Frame):
    def __init__(self, app):
        tk.Frame.__init__(self, app)
        tk.Frame.configure(self, bg='#fefbdc')
        app.columnconfigure(0, weight=1)
        app.columnconfigure(1, weight=10)

        self.images = []

        self.backbutton = load_image(f'Artwork\\BackButton.png', (35, 35))
        button = tk.Button(self, command=lambda : app.switch_frame(MapPage), image=self.backbutton, borderwidth=0, background='#fefbdc')
        button.grid(row=0, column=0, padx=25)


        # Create the buttons
        size = int(550/(len(suspects) + 2))
        for i in range(len(suspects)):
            self.images.append(load_image(f'Artwork\\notSelectedSmallTextBar.png', (int(size * 5), size)))
            name = tk.Button(self, text=suspects[i].name, image=self.images[i], borderwidth=0, background='#fefbdc', compound='center', command=lambda suspect = suspects[i]: app.switch_frame(EndPage, suspect), font=('Helvetica', 24))
            name.grid(row=1+i, column=1, pady=5, columnspan=2)

class EndPage(tk.Frame):
    def __init__(self, app, suspect):
        tk.Frame.__init__(self, app)
        # Create the image
        self.image = load_image('Artwork\\Title Image Pixel Art.png', (460, 550))
        img_label = tk.Label(self, image=self.image, borderwidth=0)
        img_label.grid(row=0, column=0, rowspan=3)

        if (suspect.is_villian):
            text = "You caught the right person!"
        else:
            text = "You accused the wrong person."

        l = tk.Label(self, text=text, font=('Helvetica', 16, "bold"))
        l.grid(row=1, column=0)


def load_image(image_name, image_size):
    img = Image.open(image_name)
    if (image_size):
        img = img.resize(image_size, Image.NEAREST)
    return ImageTk.PhotoImage(img)


suspects = [
    suspect(
        "Cogsworth", location=(8, 10), default_dialogue="Hello my good man.", 
        questions=["Are you the theif?", "Did you witness anything?", "Who do you think did it?"], 
        answers=["No. Absolutely not!\nHow DARE you accuse me of that!", "Well, I did see someone running across the rooftop last night at midnight.", "Ah, no idea."],
    ), 
    suspect(
        "Amy", location=(10, 8), default_dialogue="hello",
        questions=["Are you the theif?", "Did you witness anything?", "Who do you think did it?"], 
        answers=["No. Absolutely not!\nHow DARE you accuse me of that!", "Well, I did see someone running across the rooftop last night at midnight.", "Ah, no idea."],
    ), 
    suspect(
        "James", location=(11, 9), default_dialogue="Sup.", 
        questions=["Are you the thief?", "Did you witness anything?", "Who do you think did it?"], 
        answers=["No.", "No.", "Not me."],
    ), 
    suspect(
        "Mrs. Jenny", location=(7, 9), default_dialogue="hello", 
        questions=["Are you the thief?", "Did you witness anything?", "Who do you think did it?"], 
        answers=["No.", "No.", "Not me."],
    ), 
    suspect(
        "Sir Ronald", location=(8, 11), default_dialogue="hello", is_villian=True,
        questions=["Are you the theif?", "Did you witness anything?", "Who do you think did it?"], 
        answers=["No. Absolutely not!\nHow DARE you accuse me of that!", "Well, I did see someone running across the rooftop last night at midnight.", "Ah, no idea."],
    ), 
    suspect(
        "Natile", location=(10, 10), default_dialogue="hello",
        questions=["Are you the theif?", "Did you witness anything?", "Who do you think did it?"], 
        answers=["No. Absolutely not!\nHow DARE you accuse me of that!", "Well, I did see someone running across the rooftop last night at midnight.", "Ah, no idea."],
    ),
]

app = Application()
app.mainloop()
