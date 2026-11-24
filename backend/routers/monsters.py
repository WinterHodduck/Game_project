import json
import random
from pathlib import Path

from fastapi import APIRouter
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from service import data

router = APIRouter(prefix="/monsters", tags=["monsters"])

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "storage" / "white_desert_monsters.json"
IMAGE_DIR = BASE_DIR / "storage" / "image"


class Monster(BaseModel):
    id: int
    name: str
    level: int
    habitat: str
    image: str


@router.get("/")
def get_all_monsters():
    return data.get_all()



def mount_monster_images(app):
    if IMAGE_DIR.exists():
        app.mount("/image", StaticFiles(directory=str(IMAGE_DIR)), name="image")

 #Read / Update / Delete 구현예정
