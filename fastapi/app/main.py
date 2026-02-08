from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.routers import combatants, encounter, vectordb, ai_chat
from app.services.sqldb_service import init_db, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    engine.dispose()


app = FastAPI(lifespan=lifespan, swagger_ui_parameters={"syntaxHighlight": False})
app.include_router(combatants.router)
app.include_router(vectordb.router)
app.include_router(ai_chat.router)
app.include_router(encounter.router)

# Global custom Exception Handler
# All Exceptions raised in the routers get handled here
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exception: HTTPException):
    return JSONResponse(
        status_code=exception.status_code,
        content={"message": exception.detail}
    )


# explicit validation error handler (required for the PATCH endpoints to return 422 on invalid input)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exception: ValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exception.errors()}
    )


# generic sample endpoint
@app.get("/")
async def sample_endpoint():
    return {"message": "Hello! Go to /docs to start using the Initative Tracker API!"}
