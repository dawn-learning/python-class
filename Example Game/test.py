# pixel_only = '▀'
# top_pixel_only = '\033[38;2;{};{};{}m▀'
# bottom_pixel_only ='\033[48;2;{};{};{}m▀'
# top_and_bottom_pixels = '\033[38;2;{};{};{}m\033[48;2;{};{};{}m▀'
# character_and_pixel = "\033[38;2;{};{};{}m\033[48;2;{};{};{}m{}"
# line_end = "\033[0m"


# def get_pixels(top, bottom):
#     return 


# # for j in range(3):
# #     string = ""
# #     for i in range(25):
# #         if i % 2 == 0:
# #             string += get_pixels((255, 255, 255), (200, 200, 200))
# #         else:
# #             string += get_pixels((200, 200, 200), (255, 255, 255))
# #     print(string + line_end, end="" if j == 2 else "\n")

# # print(f"\u001b[{2}A" + f"\u001b[{4}D" + get_pixels((255, 0, 0), (0, 0, 255)) + f"\u001b[{1}C" + get_pixels((255, 0, 0), (0, 0, 255)) + line_end, end="")
# # print(f"\u001b[{200}B")




# from ah import Screen, PixelLayer, background_layer, screen_width, screen_height, Color, clear_screen, TextPixel
# from math import ceil
# from time import sleep

# global previous
# previous = None

# def display(screen : Screen, width_override : int = None, height_override : int = None, DEBUG = False) -> None:
#     def get_text_color(background_color):
#         if Color.brightness_value(background_color) > 0.5:
#             text_color = (0, 0, 0)
#         else:
#             text_color = (255, 255, 255)
#         return text_color

#     # Move back to start
#     width = screen_width if width_override == None else width_override
#     height = screen_height if height_override == None else height_override
#     output : str = f"\u001b[{100}D" + f"\u001b[{100+8}A"
#     # Find and replace differences
#     global previous
#     pixels : list[list[tuple]] = screen.flatten()
#     if previous == None:
#         output += str(PixelLayer(pixels))
#     else:
#         last_change = (0, 0)
#         count_y = 0
#         for row_pair_index in range(ceil(len(pixels)/2)):
#             row_pair_index *= 2
#             top_row = pixels[row_pair_index]
#             bottom_row = pixels[row_pair_index+1] if row_pair_index +1 < len(pixels) else None
#             count_x = 0
#             for element_index in range(len(top_row)):
#                 if top_row[element_index] != previous[row_pair_index][element_index] or (False if not bottom_row else (bottom_row[element_index] != previous[row_pair_index+1][element_index])):
#                     if count_y > 0:
#                         output += f"\u001b[{count_y}B" + f"\u001b[{100}D"
#                         count_y = 0
#                     if count_x > 0:
#                         output += f"\u001b[{count_x}C"
#                         count_x = 0
#                     # output += "1"
#                     output += PixelLayer.get_pixel_pair(pixels, row_pair_index, row_pair_index+1, element_index)
#                 #     # A difference was found
#                 #     if DEBUG: print(f"difference detected was {previous[row_pair_index][element_index]} and {previous[row_pair_index+1][element_index]} is {top_row[element_index]} and {bottom_row[element_index]} at {element_index-last_change[0]} and {row_pair_index-last_change[1]}")
#                 #     move_y = row_pair_index-last_change[1]
#                 #     if move_y > 0:
#                 #         output += f"\u001b[{move_y-1}B\u001b[{width}D"
#                 #     move_x = element_index-last_change[0]-1
#                 #     if move_x > 0:
#                 #         output += f"\u001b[{move_x}C"
#                 else:
#                     count_x += 1
#                     # output += f"\u001b[{0}C"
#                     # output += "0"
#                     # if bottom_row:
#                     #     if type(top_row[element_index]) == TextPixel:
#                     #         pixel = top_row[element_index]
#                     #         output += character_and_pixel.format(
#                     #             *get_text_color(pixel.top_pixel_color), 
#                     #             *Color.combine(pixel.top_pixel_color, bottom_row[element_index]), 
#                     #             "H"
#                     #         )
#                     #     elif type(bottom_row[element_index]) == TextPixel:
#                     #         pixel = bottom_row[element_index]
#                     #         output += character_and_pixel.format(
#                     #             *get_text_color(pixel.top_pixel_color), 
#                     #             *Color.combine(pixel.top_pixel_color, top_row[element_index]), 
#                     #             "H"
#                     #         )
#                     #     else:
#                     #         output += top_and_bottom_pixels.format(*top_row[element_index], *bottom_row[element_index])
#                     # else:
#                     #     if type(top_row[element_index]) == TextPixel:
#                     #         pixel = top_row[element_index]
#                     #         output += character_and_pixel.format(*get_text_color(pixel.top_pixel_color), *pixel.top_pixel_color, "H")
#                     #     else:
#                     #         output += top_pixel_only.format(*top_row[element_index])
#                     # last_change = (element_index, row_pair_index)
#             count_y += 1
#     print(output + line_end)
#     previous = pixels


# # clear_screen()
# # display(Screen([PixelLayer([[Color.RED]]), background_layer]))
# # sleep(1)
# # display(Screen([
# #     PixelLayer([[Color.BROWN, None], [Color.BROWN, None], [Color.BROWN, None], [None, Color.BROWN]]),
# #     background_layer
# # ]))
# # sleep(1)
# # print(f"\u001b[{10000}C" + f"\u001b[{screen_height+10}B")


# # background_color = Color.combine((255, 255, 255), (0, 0, 0))
# # if Color.brightness_value(background_color) > 0.5:
# #     text_color = (0, 0, 0)
# # else:
# #     text_color = (255, 255, 255)
# # print(character_and_pixel.format(*text_color, *background_color, "H") + line_end)

# from ah import *





# def run_intro_dialogue(main_character : BasicCharacter):
#     characters = [
#         BasicCharacter(
#             name="King",
#             artwork=load_art("King"),
#             character_type="Neutral",
#         ),
#         main_character
#     ]

#     display(get_chat(
#         characters=characters, 
#         text="Hello adventurer!\nEvil beasts have taken over this land.\nEliminate the three strongest and the rest will leave.\nWill you help me?",
#         continue_text="Press any key"
#     ))
#     wait_for_character_input()

#     return

#     options = ["Yes", "No"]
#     display(get_options(characters=characters, options=options))

#     user_input = get_number_selection_from_options(options)

#     if user_input == 1:
#         display(get_chat(
#             characters=characters, 
#             text="Oh.\nOk.\nBye then.",
#             continue_text="Press any key"
#         ))
#         quit()

#     display(get_chat(
#         characters=characters, 
#         text="Good luck adventurer!\nDefeat the three beasts and then return here to claim your prize!",
#         continue_text="Press any key"
#     ))

#     wait_for_character_input()



# run_intro_dialogue(BasicCharacter(
#         name= "Wizard",
#         stats = CharacterStats(
#             max_health=10,
#             damage=2,
#             healing=1,
#         ),
#         artwork=load_art("Wizard"),
#         character_type="Ally",
#         abilities=[Whack(), Heal()],
#     )
# )

# display(Screen([
#     PixelLayer([[Color.BROWN, None], [Color.BROWN, None], [Color.BROWN, None], [None, Color.BROWN]]),
#     background_layer
# ]))

# wait_for_character_input()

# letters = ["A", "B", "C"]

# for i in enumerate(letters):
#     print(i)




