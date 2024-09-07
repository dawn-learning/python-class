# from charms import Charms

# class StatusEffect:
#     def __init__(self, action, name = "Unamed Status Effect", duration = 3, level = 1) -> None:
#         self.name = name
#         self.action = action
#         self.duration = duration
#         self.level = level

# def burn(basic_character, count : int, level : int = 1):
#     if not count: return None
#     if count > 0:
#         # Burn resistance prevents burn damage
#         if Charms.BURNRESISTANCE in basic_character.charms:
#             return count - 1
#         # Without this charm, damage is taken
#         basic_character.take_damage(level)
#         print(f"{basic_character.name} was burned for {level} damage")
#         return count - 1
#     return None

# def regen(basic_character, count : int, level : int = 1):
#     if not count: return None
#     if count > 0:
#         basic_character.take_healing(level)
#         print(f"{basic_character.name} was healed for {level} health")
#         return count - 1
#     return None

# def damage_boost(basic_character, already_applied : bool | None, level : int = 1):
#     if already_applied == False:
#         basic_character.base_damage += 2 * level
#         return True
#     if already_applied:
#         basic_character.base_damage -= 2 * level
#         return None


# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
from characters import BasicCharacter



class Effect():
    def __init__(self, effect_name, effect_description : str, duration, effect_strength = 1) -> None:
        self.name = effect_name
        self.description = effect_description
        self.duration = duration
        self.effect_strength = effect_strength

    def turn_end(self, effected_character : BasicCharacter, DEBUG = False):
        '''Decrements the remaining duration of the effect by 1 and if the effect applies itself on turn end, applies effect.'''
        self.duration -= 1

    def has_worn_off(self):
        return self.duration <= 0

    def __str__(self) -> str:
        return f"{self.name} at level {self.effect_strength} for {self.duration} more rounds"

    def __eq__(self, value: object) -> bool:
        try:
            return self.name == value.name
        except:
            return False

class DamageBoost(Effect):
    def __init__(self) -> None:
        super().__init__("Strength Boost", "Increases physical damage by 1.5", 3)

class HealBoost(Effect):
    def __init__(self) -> None:
        super().__init__("Strength Boost", "Increases healing done by 1.5", 2)

class Poisoned(Effect):
    def __init__(self) -> None:
        super().__init__("Poisoned", "Does 5 damage every round.", 3, 3)
    
    def turn_end(self, effected_character : BasicCharacter, DEBUG = False):
        super().turn_end(effected_character)
        effected_character.take_damage(5)
        if DEBUG: print(f"{effected_character.name} took 5 damage from poison")
