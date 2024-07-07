
# class Suspect():
#     def __init__(self, name, init_dialogue) -> None:
#         self.name = name
#         self.init_dialogue = init_dialogue
#         self.questions = []
#         self.answers = []

#     def addQuestionAndAnswer(self, question, answer):
#         self.questions.append(question)
#         self.answers.append(answer)
#         return self

# class Villain(Suspect):
#     def isVillian(self):
#         return True








# import tkinter as tk
# from PIL import Image, ImageTk
# import urllib.request
# import io

# character_portraits = {
#     "normal" : "https://static.wikia.nocookie.net/slimerancher/images/2/2b/MochiDefault.png/revision/latest/scale-to-width-down/1000?cb=20180317174715", 
#     "angry" : "https://static.wikia.nocookie.net/slimerancher/images/d/d6/MochiAngry.png/revision/latest/scale-to-width-down/1000?cb=20180317174315", 
#     "boastful" : "https://static.wikia.nocookie.net/slimerancher/images/9/9e/MochiBoastful.png/revision/latest/scale-to-width-down/1000?cb=20180317174331", 
#     "charming" : "https://static.wikia.nocookie.net/slimerancher/images/1/15/MochiCharming.png/revision/latest/scale-to-width-down/1000?cb=20180317174352", 
#     "confident" : "https://static.wikia.nocookie.net/slimerancher/images/8/8a/MochiConfident.png/revision/latest/scale-to-width-down/1000?cb=20180317174404", 
#     "discouraged" : "https://static.wikia.nocookie.net/slimerancher/images/7/74/MochiDiscouraged.png/revision/latest/scale-to-width-down/1000?cb=20180317174418", 
#     "very discouraged" : "https://static.wikia.nocookie.net/slimerancher/images/5/5e/MochiDiscouraged2.png/revision/latest/scale-to-width-down/1000?cb=20180317174429", 
#     "mocking" : "https://static.wikia.nocookie.net/slimerancher/images/2/21/MochiMocking.png/revision/latest/scale-to-width-down/1000?cb=20180317174440", 
#     "sad" : "https://static.wikia.nocookie.net/slimerancher/images/1/13/MochiSad1.png/revision/latest/scale-to-width-down/1000?cb=20180317174500", 
#     "sad mad" : "https://static.wikia.nocookie.net/slimerancher/images/0/0b/MochiSad2.png/revision/latest/scale-to-width-down/1000?cb=20180317174518", 
#     "shy" : "https://static.wikia.nocookie.net/slimerancher/images/4/4c/MochiShy.png/revision/latest/scale-to-width-down/1000?cb=20180317174545", 
# }

# class Photo():
#     def __init__(self, file : str | None = None) -> None:
#         if file:
#             self.load_image(file)

#     def load_portrait(self, mood : str):
#         url = character_portraits[mood]
#         with urllib.request.urlopen(url) as u:
#             raw_data = u.read()
#         # image = ImageTk.PhotoImage(Image.open().resize((350, 350)))
#         # return image
#         self.load_image(io.BytesIO(raw_data))

#     def load_image(self, file : any):
#         self._just_loaded_image = Image.open(file)
#         self._unchanged_image = self._just_loaded_image.copy()
#         self.image = ImageTk.PhotoImage(self._just_loaded_image)
#         self.height = self.image.height()
#         self.width = self.image.width()

#     def update(self, given_width : int, given_height : int):
#         given_space_width = given_width * 1.0
#         given_space_height = given_height * 1.0
#         if self.width > self.height:
#             new_height = given_space_width/self.width * self.height
#             new_width = given_space_width * 1.0
#         else:
#             new_width = given_space_height/self.height * self.width
#             new_height = given_space_height * 1.0
#         if new_width > given_width:
#             new_height = given_width/self.width * self.height
#             new_width = given_width
#         elif new_height > given_height:
#             new_width = given_width/self.width * self.height
#             new_height = given_height
#         new_width = int(new_width)
#         new_height = int(new_height)
#         self.image = ImageTk.PhotoImage(self._unchanged_image.resize((new_width, new_height)))


# class InterviewApp(tk.Tk):
#     def __init__(self):
#         tk.Tk.__init__(self)
#         # self.title("Resizable Image Example")
#         self.geometry("400x400")  # Set your desired window size

#         self.photo = Photo()
#         self.photo.load_portrait("charming")
#         # "C:\\Users\\jgill\\Desktop\\ORGANIZE ME\\Saved (on phone) (4.22.2024)\\Screenshot_20231006-124545_One UI Home.jpg"
        
#         # Create a label for the image
#         self.background_label = tk.Label(self, image=self.photo.image)
#         self.background_label.grid(row=0, column=0, sticky="nsew")

#         # Bind the resize function to window configuration
#         self.bind("<Configure>", self._resize_widgets)

#         # Configure grid weights
#         self.columnconfigure(0, weight=1)
#         self.rowconfigure(0, weight=1)

#         # tk.Button(self, text="Nice").grid(row=1, column=0)
#         tk.Button(self, text="Nice").grid(row=0, column=1)
#         # tk.Button(self, text="Nice").grid(row=1, column=1)

#     def _resize_widgets(self, event):
#         self.photo.update(event.width, event.height)
#         self.background_label.configure(image=self.photo.image)

# if __name__ == "__main__":
#     app = InterviewApp()
#     app.mainloop()



# import tkinter as tk
# root = tk.Tk()
# canv = tk.Canvas(root, width=300, height=200, bg="blue")
# canv.pack()
# lab = tk.Label(canv, text="HELLO", fg="red", bg=canv['bg'])
# lab.place(x=50, y=50, anchor='nw')
# # lab['bg'] = canv['bg'] # could have done it this way instead
# root.mainloop()


from ah import split_text


for a in split_text("HILKJALKEJHILKJALKEJHILKJALKEJHHILKJALKEJ"):
    print(a)




