from collections import OrderedDict

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlmodel import select, Session

from app.models.combatant_model import CombatantModel, get_init_roll_details
from app.services.sqldb_service import get_session

router = APIRouter(
    prefix="/encounter",
    tags=["encounter"]
)

encounter_chars: dict[str, CombatantModel] = dict()

@router.put("/{name}", status_code=200)
async def add_combatant_to_encounter(name: str, session: Session = Depends(get_session)):
    combatant_for_name = session.exec(
        select(CombatantModel).where(CombatantModel.name == name)
    ).first()
    # If the combatant exists, add it, if not, throw exception
    if combatant_for_name:
        encounter_chars[name] = combatant_for_name
        return {"encounter":[char.to_dict() for char in encounter_chars.values()]}
    else:
        raise HTTPException(status_code=404, detail=f"A combatant with the name {name} was not found; it cannot be added to the encounter.")

@router.delete("/{name}", status_code=200)
async def remove_combatant_from_encounter(name: str):
    if name in encounter_chars:
        del encounter_chars[name]
        return {"encounter":[char.to_dict() for char in encounter_chars.values()]}
    else:
        raise HTTPException(status_code=400, detail=f"A combatant with the name {name} is not in the encounter; it cannot be removed from the encounter.")

@router.get("/", status_code=200)
async def get_encounter_combatants():
    # return {name : char.to_dict() for name, char in encounter_chars.items()} 
    # JOEY :changed to return list of combatants instead of dict, 
    return [char.to_dict() for char in encounter_chars.values()]

@router.delete("/", status_code=200)
async def clear_encounter_chars():
    encounter_chars.clear()
    return {"message" : "All combatants have been removed from the encounter."}

@router.get("/rolls", status_code=200)
async def get_encounter_init_rolls():
    if len(encounter_chars) == 0:
        raise HTTPException(status_code=404, detail="No combatants have been added to the encounter.")
    return get_init_roll_details(encounter_chars.values())
