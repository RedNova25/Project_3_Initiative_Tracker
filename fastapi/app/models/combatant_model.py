import random
from collections import OrderedDict
from enum import Enum

from sqlmodel import Field, SQLModel


def get_init_roll() -> int:
    return random.randint(1, 20)

def get_dex_init_mod(dex_score) -> int:
    return (dex_score // 2) - 5

class CharacterClass(str, Enum):
    UNCLASSED = "Unclassed"
    BARBARIAN = "Barbarian"
    BARD = "Bard"
    CLERIC = "Cleric"
    DRUID = "Druid"
    FIGHTER = "Fighter"
    MONK = "Monk"
    PALADIN = "Paladin"
    RANGER = "Ranger"
    ROGUE = "Rogue"
    SORCERER = "Sorcerer"
    WARLOCK = "Warlock"
    WIZARD = "Wizard"

class CombatantModel(SQLModel, table=True):
    name: str = Field(primary_key=True, min_length=1)
    char_class: CharacterClass
    dex_score: int = Field(ge=0, le=30)
    other_init_mod: int = 0 # default to 0, can really technically be any integer

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "char_class": self.char_class,
            "dex_score": self.dex_score,
            "other_init_mod": self.other_init_mod,
        }

def get_init_roll_details(combatants: list[CombatantModel]) -> list[dict]:
    combatants_with_rolls = []
    for combatant in combatants:
        combatant_dict = OrderedDict(combatant.model_dump())
        del combatant_dict["dex_score"], combatant_dict["char_class"]
        dex_init_mod = get_dex_init_mod(combatant.dex_score)
        combatant_dict["dex_init_mod"] = dex_init_mod
        combatant_dict.move_to_end("other_init_mod")
        combatant_dict["init_roll"] = get_init_roll()
        combatant_dict["initiative"] = combatant_dict["init_roll"] + dex_init_mod + combatant.other_init_mod
        combatant_dict.move_to_end("initiative", last=False) # move initiative roll to the front
        combatants_with_rolls.append(combatant_dict)
    # sort by init_roll, highest to lowest
    combatants_with_rolls.sort(key=lambda x: x["initiative"], reverse=True)
    return combatants_with_rolls