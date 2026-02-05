from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import PlainTextResponse

from app.models.combatant_model import CombatantModel
from app.models.search import SearchRequest
from app.services.ai_langchain_service import get_gen_chat_chain, invoke_llm, get_make_chars_chain
from app.services.vectordb_service import similarity_search

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)
gen_char_chain = get_gen_chat_chain()
make_chars_chain = get_make_chars_chain()


class ChatInputModel(BaseModel):
    input: str

@router.post("/gen_dnd_chat", status_code=200)
async def chat_dnd_with_memory(chat_input: ChatInputModel):
    return PlainTextResponse(gen_char_chain.invoke(input=chat_input.input)['response'])

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
    return PlainTextResponse(make_chars_chain.invoke({"input": chat.input})['response'])

@router.delete("/make_chars_chat", status_code=200)
async def clear_make_chars_memory():
    make_chars_chain.memory.clear()
    return {"message": "The memory for the chat at /make_chars_chat has been cleared."}