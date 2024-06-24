# # import os
# # game_not_over = True

# # rooms_list = ["living room", "kitchen", "bathroom", "bedroom"]
# # print("You enter the house. You know who the killer is, you just have to prove if by finding the murder weapon.")

# # # Rooms selection
# # while (game_not_over):
# #     os.system("cls||clear")
# #     print("The house has four rooms:")
# #     for room in rooms_list:
# #         print(room)
# #     print("Which room do you want to look in?")
# #     selected_room = input()

# #     if (selected_room == "living room"):
# #         objects_in_room = ["dresser", "couch", "cat", "lamp", "newspaper"]
# #     elif (selected_room == "kitchen"):
# #         objects_in_room = ["dresser", "couch", "cat", "lamp", "newspaper"]
# #     elif (selected_room == "bathroom"):
# #         objects_in_room = ["dresser", "couch", "cat", "lamp", "newspaper"]
# #     elif (selected_room == "bedroom"):
# #         objects_in_room = ["dresser", "couch", "cat", "lamp", "newspaper"]
# #     elif (selected_room == "e" or selected_room == "exit"):
# #             break
# #     else:
# #         print("Select a room")
# #         continue

# #     print("You enter the " + selected_room + ".")
# #     # Checking room
# #     while (True):
# #         os.system("cls||clear")
# #         print("You find several objects. \nWhich one do you look under for the murder weapon?")
# #         for object in objects_in_room:
# #             print(object)
# #         selected_object = input()

# #         if (selected_object == "couch" and selected_room == "living room"):
# #             print("You check under the couch. You find the knife.\nYou have the evidence to convict the killer.")
# #             game_not_over = False
# #             break
# #         elif (selected_object == "e" or selected_object == "exit"):
# #             break
# #         elif (selected_object in objects_in_room):
# #             print("You find nothing of note under the " + selected_object + ".\nYou need to keep searching.")
# #         else:
# #             print("Select an object")














# # import tkinter as tk

# # class Application(tk.Tk):
# #     def __init__(self):
# #         tk.Tk.__init__(self)
# #         self._frame = StartPage(self)
# #         self._frame.pack()

# # class StartPage(tk.Frame):
# #     def __init__(self, app):
# #         tk.Frame.__init__(self, app)
# #         # Create the image

# #         l = tk.Label(self, text="DETECTIVE GAME", font=('Helvetica', 32, "bold"))
# #         l.grid(row=0, column=0)

# #         b = tk.Button(self, text="Start", font=('Helvetica', 12))
# #         b.grid(row=2, column=0)



# # Application().mainloop()






# # import tkinter as tk
# # from PIL import ImageTk, Image


# class Suspect():
#     def __init__(self, name, map_location, default_dialogue) -> None:
#         self.name : str = name
#         self.map_location : tuple[int, int] = map_location
#         self.default_dialogue = default_dialogue
#         self.questions = []
#         self.answers = []

#     def addQandA(self, question, answer):
#         self.questions.append(question)
#         self.answers.append(answer)
#         return self

#     def isVillian():
#         return False

# class Villian(Suspect):
#     def isVillian():
#         return True

# suspects = [
#     Suspect("Cogsworth", map_location=(8, 10), default_dialogue="Hello my good man.")
#         .addQandA("Are you the theif?", "No. Absolutely not!\nHow DARE you accuse me of that!")
#         .addQandA("Did you witness anything?", "Well, I did see someone running across the rooftop last night at midnight.")
#         .addQandA("Who do you think did it?", "Ah, no idea."), 
#     Suspect("Amy", map_location=(10, 8), default_dialogue="hello")
#         .addQandA("Are you the theif?", "No. Absolutely not!\nHow DARE you accuse me of that!")
#         .addQandA("Did you witness anything?", "Well, I did see someone running across the rooftop last night at midnight.")
#         .addQandA("Who do you think did it?", "Ah, no idea."), 
#     Suspect("James", map_location=(11, 9), default_dialogue="Sup.")
#         .addQandA("Are you the theif?", "No. Absolutely not!\nHow DARE you accuse me of that!")
#         .addQandA("Did you witness anything?", "Well, I did see someone running across the rooftop last night at midnight.")
#         .addQandA("Who do you think did it?", "Ah, no idea."), 
#     Suspect("Mrs. Jenny", map_location=(7, 9), default_dialogue="hello")
#         .addQandA("Are you the theif?", "No. Absolutely not!\nHow DARE you accuse me of that!")
#         .addQandA("Did you witness anything?", "Well, I did see someone running across the rooftop last night at midnight.")
#         .addQandA("Who do you think did it?", "Ah, no idea."), 
#     Villian("Sir Ronald", map_location=(8, 11), default_dialogue="hello")
#         .addQandA("Are you the theif?", "No. Absolutely not!\nHow DARE you accuse me of that!")
#         .addQandA("Did you witness anything?", "Well, I did see someone running across the rooftop last night at midnight.")
#         .addQandA("Who do you think did it?", "Ah, no idea."), 
#     Suspect("Natile", map_location=(10, 10), default_dialogue="hello")
#         .addQandA("Are you the theif?", "No. Absolutely not!\nHow DARE you accuse me of that!")
#         .addQandA("Did you witness anything?", "Well, I did see someone running across the rooftop last night at midnight.")
#         .addQandA("Who do you think did it?", "Ah, no idea."),
# ]


# # class Window(tk.Tk):
# #     def __init__(self):
# #         tk.Tk.__init__(self)
# #         self.frame = None
# #         self.switch_frames(TitlePage)

# #     def switch_frames(self, new_frame, new_info=None):
# #         if (not self.frame == None):
# #             self.frame.destroy()
# #         if (new_info == None):
# #             self.frame = new_frame(self)
# #         else:
# #             self.frame = new_frame(self, new_info)
# #         self.frame.pack()

# # class TitlePage(tk.Frame):
# #     def __init__(self, window):
# #         tk.Frame.__init__(self)
# #         self.window = window
# #         self.a : tk.Label = tk.Label(self, text="DETECTIVE GAME", font=('Helvetica', 32, "bold"))
# #         self.a.pack()
# #         button = tk.Button(self, text="Press me", command=self.switch_buttons)
# #         button.pack()

# #     def switch_buttons(self):
# #         if (not self.a["text"] == "HI"):
# #             self.a["text"] = "HI"
# #         else:
# #             self.window.switch_frames(InterviewPage, suspects[0])

# # def load_image(image_name, image_size):
# #     img = Image.open(image_name)
# #     if (image_size):
# #         img = img.resize(image_size, Image.NEAREST)
# #     return ImageTk.PhotoImage(img)

# # class InterviewPage(tk.Frame):
# #     def __init__(self, window, new_info):
# #         tk.Frame.__init__(self)
# #         self.window = window
# #         self.interviewie = new_info
# #         self.a : tk.Label = tk.Label(self, text=new_info.name, font=('Helvetica', 32, "bold"))
# #         self.a.grid(row=0, column=1)
# #         button = tk.Button(self, text="Press me")
# #         button.grid(row=1, column=0)
# #         self.image = load_image('Target Program\\Artwork\\Title Image Pixel Art.png', (460, 550))
# #         img_label = tk.Button(self, image=self.image, borderwidth=0)
# #         img_label.grid(row=1, column=1)

# #     def switch_buttons(self):
# #         if (not self.a["text"] == "HI"):
# #             self.a["text"] = "HI"
# #         else:
# #             self.window.switch_frames(TitlePage)

# # Window()

# # suit_case = tk.Tk()
# # suit_case.geometry("400x400")
# # # suit_case.resizable(False, False)
# # suit_case.configure(bg='#5b05a1')
# # suit_case.overrideredirect(True)
# # # suit_case.attributes("-alpha", '0.5')
# # suit_case.geometry("+200+400")

# # def tkquit():
# #     suit_case.destroy()

# # button = tk.Button(suit_case, text="Quit", command=tkquit)
# # button.pack()

# # global drag_me
# # drag_me = False

# # def yikes(x):
# #     global drag_me
# #     print("hi" + str(x))
# #     drag_me = not drag_me
# #     while(drag_me):
# #         suit_case.geometry("+300+500")

# # suit_case.bind('<Button-1>', lambda _ : yikes(drag_me))

# # suit_case.mainloop()






























# import tkinter as tk
# from PIL import ImageTk, Image



# class Window(tk.Tk):
#     def __init__(self):
#         tk.Tk.__init__(self)
#         self.geometry("400x400")
#         # self.resizable(False, False)
#         self.configure(bg="#ceeb2f")

#         self.frame = TitlePage(self)
#         self.frame.pack()

#     def switch_pages(self, page_to_switch_to):
#         if (self.frame != None):
#             self.frame.destroy()
#         self.frame = page_to_switch_to(self)
#         self.frame.pack()


# class InterviewPage(tk.Frame):
#     def __init__(self, window):
#         tk.Frame.__init__(self)
#         self.configure(bg="#ceeb2f")
#         self.window = window

#         self.image = get_image('Target Program\\Artwork\\' + suspects[0].name + '.png', (200, 200))
#         img_button = tk.Label(self, image=self.image, borderwidth=0)
#         img_button.grid(row=0, column=1)

#         text = tk.Label(self, text=suspects[0].default_dialogue, font=('Helvetica', 16, "bold"))
#         text.grid(row=1, column=1)

#         def print_this(i):
#             text["text"] = suspects[0].answers[i]


#         qs = suspects[0].questions
#         for i in range(len(qs)):
#             button = tk.Button(self, text=qs[i], command = lambda i = i: print_this(i))
#             button.grid(row=2, column=i)

# def get_image(image_location, size):
#     img = Image.open(image_location)
#     img = img.resize(size, Image.NEAREST)
#     return ImageTk.PhotoImage(img)

# class TitlePage(tk.Frame):
#     def __init__(self, window):
#         tk.Frame.__init__(self)
#         self.window = window
#         self.configure(bg="#ceeb2f")

#         self.image = get_image('Target Program\\Artwork\\Title Image Pixel Art.png', (400, 400))
#         img_button = tk.Label(self, image=self.image, borderwidth=0)
#         img_button.grid(row=0, column=0, rowspan=2)

#         text = tk.Label(self, text="Dective Game", font=('Helvetica', 30, "bold"))
#         text.grid(row=0, column=0)
#         button = tk.Button(self, text="Continue", command = lambda : self.window.switch_pages(InterviewPage))
#         button.grid(row=1, column=0)

# window = Window()
# window.mainloop()

























