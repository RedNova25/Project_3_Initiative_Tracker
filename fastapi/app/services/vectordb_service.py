import asyncio
import json
from typing import Any

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings

from app.models.combatant_model import CombatantModel

PERSIST_DIRECTORY = "app/chroma_store" # Where the DB will be stored on disk
EMBEDDING = OllamaEmbeddings(model="all-minilm:l6-v2") # The embedding model to use
vector_store: dict[str, Chroma] = {}

def combatant_to_document(combatant: CombatantModel) -> Document:
    # TODO: do some string replacement to change dex_score to DEX (Dexterity), may help with tasks
    return Document(page_content=json.dumps(combatant.to_dict(), separators=(',', ':')).replace('"', ''))

def get_vector_store(collection:str) -> Chroma:
    # Get (or create) the vector store instance
    # If creating, define the collection name, persist directory, and embedding function
    if collection not in vector_store:
        vector_store[collection] = Chroma(
            collection_name=collection,
            # collection_metadata={"hnsw:space":"cosine"},
            persist_directory=PERSIST_DIRECTORY,
            embedding_function=EMBEDDING
        )
    return vector_store[collection]

def ingest_combatants_vector(combatants: list[CombatantModel]):
    combatant_store = get_vector_store("combatants")
    # make LangChain documents and ids to ingest
    docs = [
        combatant_to_document(combatant)
        for combatant in combatants
    ]
    ids = [combatant.name for combatant in combatants]
    # add documents
    combatant_store.add_documents(docs, ids=ids)

def update_combatant_vector(combatant: CombatantModel):
    combatant_store = get_vector_store("combatants")
    combatant_store.update_document(document_id=combatant.name, document=combatant_to_document(combatant))

def delete_combatants_vector(combatants: list[CombatantModel]):
    combatant_store = get_vector_store("combatants")
    combatant_store.delete(ids=[combatant.name for combatant in combatants])

# Search the vector store for similar or relevant documents based on a query
def similarity_search(query: str, collection:str, k: int = 10) -> list[dict[str,Any]]:

    # Get an instance of the vector store
    db_instance = get_vector_store(collection)

    # Save the results of the similarity search
    results = db_instance.similarity_search_with_score(query, k=k)

    # Return the results as a list of dicts with the expected fields
    return [
        {
            "text": result[0].page_content,
            "metadata": result[0].metadata,
            "score": result[1]
        }
        for result in results
    ]