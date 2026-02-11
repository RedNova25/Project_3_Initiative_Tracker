from fastapi import APIRouter, HTTPException, Request
from fastapi.params import Depends
from pydantic import BaseModel
from sqlmodel import Session
from starlette.responses import PlainTextResponse
import json
import re

from app.models.combatant_model import CombatantModel
from app.models.search import SearchRequest
from app.routers.combatants import _create_combatants_logic
from app.services.ai_langchain_service import (
    get_gen_chat_chain,
    invoke_llm,
    get_make_chars_chain,
)
from app.services.sqldb_service import get_session
from app.services.vectordb_service import similarity_search


router = APIRouter(prefix="/chat", tags=["chat"])
gen_char_chain = get_gen_chat_chain()
make_chars_chain = get_make_chars_chain()


class ChatInputModel(BaseModel):
    input: str


# ============================================================================
# ENDPOINTS
# ============================================================================


@router.post("/gen_dnd_chat", status_code=200)
async def chat_dnd_with_memory(chat_input: ChatInputModel):
    return PlainTextResponse(gen_char_chain.invoke(input=chat_input.input)["response"])


@router.delete("/gen_dnd_chat", status_code=200)
async def clear_chat_dnd_memory():
    gen_char_chain.memory.clear()
    return {"message": "The memory for the chat at /gen_dnd_chat has been cleared."}


@router.post("/find_char_chat", status_code=200)
async def find_combatant_from_db_chat(request: SearchRequest):
    result = similarity_search(request.query, "combatants", request.k)
    prompt = (
        f"Based on the following data from a character database, answer the user's query. "
        f"The characters are Dungeons and Dragons 5th Edition characters. "
        f"If there's no relevant characters for the user's query, you can say that. "
        f"Provide the full info for each character, capitalizing the first letter of each field.  "
        f"Put each field on a new line. "
        f"Dex becomes Dexterity. char_class can just be class. "
        f"Expand other_init_mod as Other Initiative Modifier. "
        f"Output your response in plaintext, without any indentation. "
        f"Extracted characters: {result}"
        f"User query: {request.query}"
    )
    result = invoke_llm(prompt)
    return PlainTextResponse(result.content)


@router.post("/make_chars_chat", status_code=200)
async def make_chars_chat(chat: ChatInputModel):
    # return make_chars_chain.invoke({"input": chat.input, "combatant_model_fields": str(CombatantModel.model_fields)})
    return PlainTextResponse(make_chars_chain.invoke({"input": chat.input})["response"])


@router.delete("/make_chars_chat", status_code=200)
async def clear_make_chars_memory():
    make_chars_chain.memory.clear()
    return {"message": "The memory for the chat at /make_chars_chat has been cleared."}


@router.post("/ingest_chars_from_chat", status_code=200)
async def ingest_chars_from_chat(
    chat: ChatInputModel, session: Session = Depends(get_session)
):
    """
    Extracts JSON from markdown code blocks and creates combatants.
    Use this endpoint for properly formatted requests (Swagger UI).
    """
    return await _process_chat_input(chat.input, session)


@router.post("/ingest_chars_from_chat/raw", status_code=200)
async def ingest_chars_from_chat_raw(
    request: Request, session: Session = Depends(get_session)
):
    """
    Accepts raw text body for clients that can't properly escape JSON.
    Use /ingest_chars_from_chat for normal requests.
    """
    body = await request.body()
    body_text = body.decode("utf-8")

    try:
        body_json = json.loads(body_text)
        chat_input = body_json.get("input", body_text)
    except json.JSONDecodeError:
        chat_input = body_text

    return await _process_chat_input(chat_input, session)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


# Helper function for the above two endpoints, to avoid code duplication.
async def _process_chat_input(chat_input: str, session: Session):
    """Shared logic for processing chat input"""
    pattern = r"```json\s*(.*?)\s*```"
    match = re.search(pattern, chat_input, re.DOTALL)

    if not match:
        raise HTTPException(
            status_code=400,
            detail="Bad Request: No valid JSON found in chat input in expected format (```json ... ```)",
        )

    json_str = match.group(1)

    try:
        json_data = json.loads(json_str)

        if not isinstance(json_data, list):
            json_data = [json_data]

        combatants = [CombatantModel(**item) for item in json_data]
        result = await _create_combatants_logic(combatants, session)

        return {
            "message": f"{len(combatants)} characters ingested successfully.",
            "ingested_characters": result,
        }

    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=400, detail=f"Bad Request: Invalid JSON format: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Bad Request: Invalid combatant data structure: {str(e)}",
        )
