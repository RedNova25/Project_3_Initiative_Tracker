import random
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

# Prompt: I want to create a character Karlach with a DEX of 16 and a bonus init mod of +3
# Output: Here is the properly formatted JSON to ingest that char

# there are several methods, such as the dir method, which show you all of the builtins for an object
