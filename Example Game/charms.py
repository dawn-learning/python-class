from enum import Enum
from artwork import load_art

class Charms(Enum):
    BURNRESISTANCE = 0
    FREEZE = 1
    EXTRAHEALTH = 2
    STRENGTH = 3
    EXTRAHEALING = 4
    POWERSPELL = 5
    DIRT = 6
    WATER = 7
    LAVA = 8

    def get_description(charm):
        match charm:
            case Charms.BURNRESISTANCE:
                return "Prevents on fire characters from being burned"
            case Charms.FREEZE:
                return "Freezes the enemy for one round, skips their turn and if fire or water enemy, takes double damage"
            case Charms.EXTRAHEALING:
                return "Gives equiped character more health"
            case Charms.STRENGTH:
                return "Increases the base attack of the character"
            case Charms.EXTRAHEALING:
                return "Increases base healing of the character"
            case Charms.POWERSPELL:
                return "A magical stone that must have been enchanted by a powerful wizard. Allows you to give yourself a temporary strength boost."
            case Charms.DIRT:
                return "A clump of dirt. Doesn't seem to do anything."
            case Charms.WATER:
                return "Some water. Not even magical."
            case Charms.LAVA:
                return "Cooled, but still a bit warm."

    def get_artwork_name(charm):
        match charm:
            case Charms.POWERSPELL:
                return "Power_charm"
            case Charms.DIRT:
                return "Dirt"
            case Charms.WATER:
                return "Water"
            case Charms.LAVA:
                return "Lava_drop"

class FunctionalCharms():
    def __init__(self, charm : Charms) -> None:
        artwork_name = charm.get_artwork_name()
        self.name = " ".join([a[:1].upper() + a[1:].lower() for a in artwork_name.split("_")])
        self.description = Charms.get_description(charm)
        self.artwork = load_art(artwork_name)
