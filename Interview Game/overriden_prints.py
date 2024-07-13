
def flatten_text(*text):
    content : str = ""
    for i in range(len(text)):
        if i != 0:
            content += " "
        content += str(text[i])
    return content

def print_character_dialogue(*text, actions, mood : str = None, character_name : str = None):
    DEBUG = False
    parts = list(text)
    if len(parts) < 1:
        parts.append("")
    dictionary = {"character_speaks" : flatten_text(*text)}
    if mood:
        dictionary["character_portrait_changes"] = mood
        if DEBUG: print("mood changed")
    if character_name:
        dictionary["character_name_changes"] = character_name
        if DEBUG: print("name changed")
    actions.append(dictionary)
    if DEBUG: print("action added")

def print_player_options(*text, actions):
    DEBUG = False
    if len(actions) == 0: actions.append({})
    if "user_options" in actions[len(actions)-1].keys():
        actions[len(actions)-1]["user_options"] += [flatten_text(*text)]
    else:
        # actions[len(actions)-1]["user_options"] = [flatten_text(*text)]
        actions.append({"user_options" : [flatten_text(*text)]})
    if DEBUG: print("option added")
