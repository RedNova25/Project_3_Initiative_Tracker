from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select

from app.models.combatant_model import (
    CombatantModel,
    CharacterClass,
    get_init_roll_details,
)
from app.services.vectordb_service import (
    ingest_combatants_vector,
    delete_combatants_vector,
)
from app.services.sqldb_service import get_session

from collections import OrderedDict

router = APIRouter(prefix="/combatants", tags=["combatants"])

# ============================================================================
# ENDPOINTS
# ============================================================================


# create multiple combatants
@router.post("/", status_code=201)
async def create_combatants(
    combatants: list[CombatantModel], session: Session = Depends(get_session)
):
    """Endpoint for direct combatant creation"""
    return await _create_combatants_logic(combatants, session)


# Return just the data for all combatants
@router.get("/data", status_code=200)
async def get_combatants(session: Session = Depends(get_session)):
    combatants = session.exec(select(CombatantModel)).all()
    if len(combatants) == 0:
        raise HTTPException(status_code=404, detail="No combatants have been created; no data can be retrieved.")
    return [combatant.to_dict() for combatant in combatants]


# Get every character's initiative roll, sorted from highest to lowest. Include character's name, initiative roll, then all other info.
@router.get("/", status_code=200)
async def get_combatants_and_rolls(session: Session = Depends(get_session)):
    combatants = session.exec(select(CombatantModel)).all()
    if len(combatants) == 0:
        raise HTTPException(
            status_code=404,
            detail="No combatants have been created; no data can be retrieved to make initiative rolls.",
        )
    return get_init_roll_details(combatants)


# get a specific combatant's info by name
@router.get("/{name}", status_code=200)
async def get_combatant(name: str, session: Session = Depends(get_session)):
    combatant = session.exec(
        select(CombatantModel).where(CombatantModel.name == name)
    ).first()
    if not combatant:
        raise HTTPException(
            status_code=404,
            detail=f"Combatant with name '{name}' not found; cannot be retrieved.",
        )
    return combatant


# delete all combatants
@router.delete("/", status_code=200)
async def delete_all_combatants(session: Session = Depends(get_session)):
    combatants = session.exec(select(CombatantModel)).all()
    length = len(combatants)
    if length == 0:
        return {"message": "All 0 combatants deleted successfully."}
    for combatant in combatants:
        session.delete(combatant)
    session.commit()
    delete_combatants_vector(combatants)
    return {"message": f"All {length} combatants deleted successfully."}


# delete a specific combatant by name
@router.delete("/{name}", status_code=200)
async def delete_combatant(name: str, session: Session = Depends(get_session)):
    combatant: CombatantModel = session.exec(
        select(CombatantModel).where(CombatantModel.name == name)
    ).first()
    if not combatant:
        raise HTTPException(
            status_code=404,
            detail=f"Combatant with name '{name}' not found; cannot be deleted.",
        )
    session.delete(combatant)
    session.commit()
    delete_combatants_vector([combatant])
    return {
        "message": f"Combatant '{name}' deleted successfully.",
        "deleted_combatant": combatant,
    }


# replace all of a combatant's info by name
@router.put("/{name}", status_code=200)
async def replace_all_combatant_info(
    name: str,
    updated_combatant: CombatantModel,
    session: Session = Depends(get_session),
):
    # validate that the updated combatant's name matches the path variable
    if updated_combatant.name != name:
        raise HTTPException(
            status_code=400,
            detail=f"Combatant name in the request body ('{updated_combatant.name}') does not match the name in the path ('{name}').",
        )
    CombatantModel.model_validate(
        updated_combatant.model_dump()
    )  # manually call validation, SQLModel requires it.
    combatant = session.exec(
        select(CombatantModel).where(CombatantModel.name == name)
    ).first()
    if not combatant:
        raise HTTPException(
            status_code=404,
            detail=f"Combatant with name '{name}' not found; cannot be updated.",
        )
    combatant.char_class = updated_combatant.char_class
    combatant.dex_score = updated_combatant.dex_score
    combatant.other_init_mod = updated_combatant.other_init_mod
    session.add(combatant)
    session.commit()
    ingest_combatants_vector([combatant])
    return {
        "message": f"Combatant '{name}' updated successfully.",
        "updated_combatant": combatant,
    }


# replace just the combatant's dex_score by name
@router.patch("/{name}/dex_score", status_code=200)
async def update_combatant_dex_score(
    name: str, dex_score: int, session: Session = Depends(get_session)
):
    combatant = session.exec(
        select(CombatantModel).where(CombatantModel.name == name)
    ).first()
    if not combatant:
        raise HTTPException(
            status_code=404,
            detail=f"Combatant with name '{name}' not found; cannot be updated.",
        )
    combatant.dex_score = dex_score
    CombatantModel.model_validate(
        combatant.model_dump()
    )  # manually call validation, SQLModel requires it.
    session.add(combatant)
    session.commit()
    ingest_combatants_vector([combatant])
    return {
        "message": f"Combatant '{name}'s Dexterity modifier updated successfully.",
        "updated_combatant": combatant,
    }


# replace just the combatant's other_init_mod by name
@router.patch("/{name}/other_init_mod", status_code=200)
async def update_combatant_other_init_mod(
    name: str, other_init_mod: int, session: Session = Depends(get_session)
):
    combatant = session.exec(
        select(CombatantModel).where(CombatantModel.name == name)
    ).first()
    if not combatant:
        raise HTTPException(
            status_code=404,
            detail=f"Combatant with name '{name}' not found; cannot be updated.",
        )
    combatant.other_init_mod = other_init_mod
    CombatantModel.model_validate(
        combatant.model_dump()
    )  # manually call validation, SQLModel requires it.
    session.add(combatant)
    session.commit()
    ingest_combatants_vector([combatant])
    return {
        "message": f"Combatant '{name}'s other initiative modifier updated successfully.",
        "updated_combatant": combatant,
    }


# replace just the combatant's char_class by name
@router.patch("/{name}/char_class", status_code=200)
async def update_combatant_char_class(
    name: str, char_class: CharacterClass, session: Session = Depends(get_session)
):
    combatant = session.exec(
        select(CombatantModel).where(CombatantModel.name == name)
    ).first()
    if not combatant:
        raise HTTPException(
            status_code=404,
            detail=f"Combatant with name '{name}' not found; cannot be updated.",
        )
    combatant.char_class = char_class
    CombatantModel.model_validate(
        combatant.model_dump()
    )  # manually call validation, SQLModel requires it.
    session.add(combatant)
    session.commit()
    ingest_combatants_vector([combatant])
    return {
        "message": f"Combatant '{name}'s class updated successfully.",
        "updated_combatant": combatant,
    }


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


# Separated the business logic from the endpoint
async def _create_combatants_logic(combatants: list[CombatantModel], session: Session):
    """Internal function with the combatant creation logic"""
    combatants_created: list[CombatantModel] = []
    combatants_failed: list[CombatantModel] = []

    for combatant in combatants:
        existing = session.exec(
            select(CombatantModel).where(CombatantModel.name == combatant.name)
        ).first()

        if existing:
            combatants_failed.append(combatant)
            continue

        session.add(combatant)
        combatants_created.append(combatant)

    if len(combatants_created) == 0:
        raise HTTPException(
            status_code=400,
            detail="No combatants were created. Either the request was empty or all combatants are already present.",
        )

    session.commit()
    ingest_combatants_vector(combatants_created)

    return {
        "message": f"{len(combatants_created)} combatants created successfully. {len(combatants_failed)} combatants are already present.",
        "created_combatants": combatants_created,
    }
