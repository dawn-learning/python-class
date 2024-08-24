from charms import Charms

class StatusEffect:
    def __init__(self, action, name = "Unamed Status Effect", duration = 3, level = 1) -> None:
        self.name = name
        self.action = action
        self.duration = duration
        self.level = level

def burn(basic_character, count : int, level : int = 1):
    if not count: return None
    if count > 0:
        # Burn resistance prevents burn damage
        if Charms.BURNRESISTANCE in basic_character.charms:
            return count - 1
        # Without this charm, damage is taken
        basic_character.take_damage(level)
        print(f"{basic_character.name} was burned for {level} damage")
        return count - 1
    return None

def regen(basic_character, count : int, level : int = 1):
    if not count: return None
    if count > 0:
        basic_character.take_healing(level)
        print(f"{basic_character.name} was healed for {level} health")
        return count - 1
    return None

def damage_boost(basic_character, already_applied : bool | None, level : int = 1):
    if already_applied == False:
        basic_character.base_damage += 2 * level
        return True
    if already_applied:
        basic_character.base_damage -= 2 * level
        return None
