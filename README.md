# Project 3 Initiative Tracker

Initiative Tracker is a web application designed to assist Dungeon Masters (DMs) in managing combat encounters during tabletop role-playing games (TTRPGs). 

## Initial Run instructions

1. Clone Repository
    ```bash
    git clone https://github.com/RedNova25/Project_3_Initiative_Tracker
    ```

2. Run backend (you need ollama installed and running for this step)
    ```bash
    cd fastapi
    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    ollama pull all-minilm:l6-v2
    ollama pull llama3.1:8b
    ollama pull gemma3:4b
    uvicorn app.main:app --reload
    ```

3. Run frontend
   * Open a new terminal in the root of the repository
    ```bash
    cd react_app
    npm install
    npm run dev
    ```

## Run Instructions (after initial setup)

1. Run backend (you need ollama installed and running for this step)
    ```bash
    cd fastapi
    .venv\Scripts\activate
    uvicorn app.main:app --reload
    ```

2. Run frontend
   * Open a new terminal in the root of the repository
    ```bash
    cd react_app
    npm run dev
    ```

## Ollama Required Models

```bash
ollama pull all-minilm:l6-v2
ollama pull llama3.1:8b
ollama pull gemma3:4b
```

## SQLite Database

The `fastapi/app.db` SQLite database, as of iniital commit, came with 39 combatants. If you want to play around with the API for testing, **please make sure to discard changes in Git for this file before pushing.**

