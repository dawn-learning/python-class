from __future__ import annotations
from enum import Enum
import status_effects

# --- Characters ---

global unique_id
unique_id = 0

class CharacterStats():
    def __init__(self, max_health : int = 10, damage = 0, healing = 0) -> None:
        if type(max_health) != int: raise Exception(f"max_health must be an int, was given a {type(max_health)}")
        self.max_health = max_health
        if type(damage) != int: raise Exception(f"damage must be an int, was given a {type(damage)}")
        self.damage = damage
        if type(healing) != int: raise Exception(f"healing must be an int, was given a {type(healing)}")
        self.healing = healing
    
    def copy(self):
        return CharacterStats(self.max_health, self.damage, self.healing)

    def __str__(self) -> str:
        return f"max_health: {self.max_health}\ndamage: {self.damage}\nhealing: {self.healing}"

    def as_dict(self) -> dict:
        return {
            "max_health": self.max_health,
            "damage": self.damage,
            "healing" : self.healing,
        }

class BasicCharacter:
    def __init__(self, name, artwork, stats : CharacterStats = None, character_type = "Enemy", abilities : list[Ability] = []) -> None:
        self.name = name
        self.current_health = stats.max_health if stats != None else None
        self.stats = stats
        self.artwork = artwork
        self.current_status_effects : list[status_effects.Effect] = []
        self.outgoing_status_effects : list[status_effects.Effect] = []
        self.character_type = character_type
        self.charms = []
        global unique_id
        self.uniqueID = unique_id
        unique_id += 1
        self.abilities = abilities
        self.skip_next_turn = False

    def __eq__(self, value: object) -> bool:
        if type(value) != BasicCharacter: return False
        return self.uniqueID == value.uniqueID

    def __str__(self) -> str:
        output = f"{self.name} ({self.character_type})"
        stats = self.stats.as_dict()
        max_health = stats.pop("max_health")
        output += f"\n health: {self.current_health}/{max_health}\n "
        output += "\n ".join([f"{a}: {stats[a]}" for a in stats.keys()])
        output += "\n Status Effects:\n  " + "\n  ".join([str(a) for a in self.current_status_effects])
        return output

    def deepcopy(self):
        output = BasicCharacter(
            name=self.name,
            stats= self.stats.copy(),
            artwork=self.artwork.copy(),
            character_type=self.character_type,
        )
        output.current_status_effects = self.current_status_effects.copy()
        output.outgoing_status_effects = self.outgoing_status_effects.copy()
        output.charms = self.charms.copy()
        output.abilities = self.abilities.copy()
        return output

    def height(self):
        return len(self.artwork) + 2 + 2 + 2

    def width(self):
        max_width = -1
        for row in self.artwork:
            if len(row) > max_width:
                max_width = len(row)
        if len(self.name) > max_width:
            max_width = len(self.name)
        if self.stats.max_health > max_width:
            max_width = self.stats.max_health
        return max_width

    # def attack(self):
    #     if len(self.outgoing_status_effects) > 0:
    #         outgoing_status_effect = self.outgoing_status_effects.pop(0)
    #         self.outgoing_status_effects.append(outgoing_status_effect)
    #     else:
    #         outgoing_status_effect = None
    #     return (self.base_damage, outgoing_status_effect)

    def take_damage(self, damage):
        self.current_health -= damage
        if self.current_health < 0:
            self.current_health = 0

    def take_healing(self, healing):
        self.current_health += healing
        if self.current_health > self.stats.max_health:
            self.current_health = self.stats.max_health

    # def get_next_default_action(self):
    #     action = self.default_actions.pop(0)
    #     self.default_actions.append(action)
    #     return action

    def end_turn(self, DEBUG = False):
        # Signals to each effect that the turn is over
        for effect in self.current_status_effects:
            effect.turn_end(effected_character=self, DEBUG=DEBUG)
        for ability in self.abilities:
            ability.round_over()
        # Removes effects that have worn off
        self.current_status_effects = [effect for effect in self.current_status_effects if not effect.has_worn_off()]
        if self.skip_next_turn:
            self.skip_next_turn = False

    def full_heal(self):
        self.current_health = self.stats.max_health





# --- Abilities ---

import artwork

class TargetType(Enum):
    ALLY = "Can only target allies"
    ALLIES_RANDOM = "Targets a random ally"
    ENEMY = "Can only target enemies"
    ENEMIES_RANDOM = "Targets a random enemy"
    ALL = "Can target anyone"
    SELF = "Can only be used on self"
    NONE = "A purely cosmetic ability"

class Ability():
    def __init__(self, name, description : str, target_type : TargetType = TargetType.NONE, image_name : str | None = None, effect : status_effects.Effect | None = None) -> None:
        self.name = name
        self.description = description
        self.target_type = target_type
        self.on_cooldown = 0
        self.effect : status_effects.Effect | None = effect # The effect if any the ability applies to the target
        self.artwork = artwork.load_art(image_name) if image_name else None

    def activate(self, using_characters_stats : CharacterStats, using_characters_effects : list[status_effects.Effect], effected_character : BasicCharacter, DEBUG : bool = False) -> str:
        '''Does whatever the ability does to the target. All subclasses must override this.'''
        raise Exception(f"The function activate() was run on a generic Ability ({self.name}). Should only be run on subtypes of Ability.")

    def round_over(self):
        if self.on_cooldown > 0:
            self.on_cooldown -= 1

class Whack(Ability):
    def __init__(self) -> None:
        super().__init__(name="Whack", description="Does damage to the enemy based on this character's base stats.", target_type=TargetType.ENEMY, image_name="Whack")

    def activate(self, using_characters_stats: CharacterStats, using_characters_effects: list[status_effects.Effect], effected_character : BasicCharacter, DEBUG : bool = False) -> str:
        damage = using_characters_stats.damage
        if status_effects.DamageBoost() in using_characters_effects:
            if DEBUG: print("StrengthBoost applied")
            damage = int(2.5 * damage)
        effected_character.take_damage(damage)
        if DEBUG: print(f"{effected_character.name} took {damage} damage")
        return f"- {damage}"


class Win(Ability):
    def __init__(self) -> None:
        super().__init__(name="Win", description="Does too much damage to the enemy.", target_type=TargetType.ENEMY, image_name="Whack")

    def activate(self, using_characters_stats: CharacterStats, using_characters_effects: list[status_effects.Effect], effected_character : BasicCharacter, DEBUG : bool = False) -> str:
        damage = 99999
        effected_character.take_damage(damage)
        if DEBUG: print(f"{effected_character.name} took {damage} damage")
        return f"- {damage}"


class Heal(Ability):
    def __init__(self) -> None:
        super().__init__("Heal", "Heals the target based on this character's base stats.", TargetType.ALLY, image_name="Heal")

    def activate(self, using_characters_stats: CharacterStats, using_characters_effects: list[status_effects.Effect], effected_character: BasicCharacter, DEBUG : bool = False) -> str:
        healing = using_characters_stats.healing
        if status_effects.HealBoost() in using_characters_effects:
            if DEBUG: print("HealBoost applied")
            healing = int(1.5 * healing)
        effected_character.take_healing(healing)
        if DEBUG: print(f"{effected_character.name} received {healing} healing")
        return f"+ {healing}"

class Poison(Ability):
    def __init__(self) -> None:
        super().__init__("Poison", "Poisions the target over the next 3 rounds for 5 damage each.", TargetType.ENEMY, image_name="Poison")

    def activate(self, using_characters_stats: CharacterStats, using_characters_effects: list[status_effects.Effect], effected_character: BasicCharacter, DEBUG : bool = False) -> str:
        effected_character.current_status_effects.append(status_effects.Poisoned())
        if DEBUG: print(f"{effected_character.name} was poisoned")
        self.on_cooldown = 4
        return "+ Poisoned"

class Freeze(Ability):
    def __init__(self) -> None:
        super().__init__("Freeze", "Prevent enemy from acting next round", TargetType.ENEMY, image_name="Freeze")

    def activate(self, using_characters_stats: CharacterStats, using_characters_effects: list[status_effects.Effect], effected_character: BasicCharacter, DEBUG: bool = False) -> str:
        effected_character.skip_next_turn = True
        self.on_cooldown = 3
        return "+ Frozen"


class DamageBoost(Ability):
    def __init__(self) -> None:
        super().__init__("Damage Boost", "Boosts the ally's damage by 150% for two rounds", TargetType.ALLY, image_name="Power_charm")

    def activate(self, using_characters_stats: CharacterStats, using_characters_effects: list[status_effects.Effect], effected_character: BasicCharacter, DEBUG : bool = False) -> str:
        effected_character.current_status_effects.append(status_effects.DamageBoost())
        return "⚔ x2.5"
