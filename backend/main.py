import json
import random
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pathlib import Path
from notices import router as notices_router  # 추가

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

DATA_PATH = Path(__file__).parent / "storage" / "white_desert_monsters.json"

def load_monsters():
    with open(DATA_PATH,encoding="utf-8") as f:
        return json.load(f)
    
    
@app.get("/api/monsters/random")
def random_monsters():
    monsters=load_monsters()
    return random.sample(monsters,k=3)

app.include_router(notices_router)