import json
import random
from pathlib import Path
from fastapi import APIRouter

router = APIRouter(prefix="/api/monsters", tags=["monsters"])

DATA_PATH = Path(__file__).parent.parent / "storage" / "white_desert_monsters.json"


def load_monsters():
    with open(DATA_PATH, encoding="utf-8") as f:
        return json.load(f)


@router.get("/random")
def random_monsters():
    return random.sample(load_monsters(), k=3)
