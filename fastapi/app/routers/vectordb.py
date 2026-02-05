from fastapi import APIRouter
from pydantic import BaseModel

from app.models.search import SearchRequest
from app.services.vectordb_service import similarity_search, get_vector_store

router = APIRouter(
    prefix="/vectordb",
    tags=["vectordb"]
)

# Endpoint for similarity search
@router.post("/sim_search")
async def combatants_similarity_search(request:SearchRequest):
    return similarity_search(request.query, collection="combatants", k=request.k)

@router.get("/dump")
async def dump_vectordb():
    vector_store = get_vector_store("combatants")
    return vector_store.get()