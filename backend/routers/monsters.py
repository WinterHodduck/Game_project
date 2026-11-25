import json
import random
from pathlib import Path

from fastapi import APIRouter
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from service import data

import os
import shutil
from uuid import uuid4
from fastapi import APIRouter, File, HTTPException, UploadFile
from typing import Any, List, Optional

UPLOAD_DIR = "storage/image"
os.makedirs(UPLOAD_DIR, exist_ok=True)

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

class MonsterCreate(BaseModel):
    id: Optional[int] = 0
    name: str
    level: int
    habitat: str
    hp: int = 0
    exp: int = 0
    attack: int = 0
    drops: List[Any] = []
    description: str = ""
    image: str = "./image/monster01.jpg"

class MonsterUpdate(BaseModel):
    id: int
    name: str
    level: int
    habitat: str
    hp: int = 0
    exp: int = 0
    attack: int = 0
    drops: List[Any] = []
    description: str = ""
    image: Optional[str] = None

@router.get("/")
def get_all_monsters():
    return data.get_all()

@router.get("/search")
def monsters_search(word:str =""):
    print('monsters_search 진입함')
    return data.search_Word(word)


def mount_monster_images(app):
    if IMAGE_DIR.exists():
        app.mount("/image", StaticFiles(directory=str(IMAGE_DIR)), name="image")

 #Read / Update / Delete 구현예정


@router.post("/upload-image")  # main.py에 넣을 때는 @a.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="이미지 파일만 업로드할 수 있습니다.")

    ext = os.path.splitext(file.filename or "")[1] or ".jpg"
    saved_name = f"{uuid4().hex}{ext}"
    save_path = os.path.join(UPLOAD_DIR, saved_name)

    try:
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="이미지 파일 저장에 실패했습니다.") from exc

    # 정적 파일 마운트(/image -> storage/image) 기준 경로 반환
    return {"image_url": f"http://127.0.0.1:8000/image/{saved_name}"} 

@router.post("/")
def create_monster(monster: MonsterCreate):
    return data.add_monster(monster.model_dump())

# 클라이언트가 보낸 방식 http://127.0.0.1:8000/menus/${menuId}   #클라이언트가 보낸  data가 ${menuId}
# 클라이어트가 /요청/데이터  이런 형식으로 보내서 다음과 같이 작성해야 한다.
@router.delete("/{mob_id}")
def delete_mob(mob_id : int):
    #data.py 파일에게 삭제해 달라고 요청
    result = data.delete_mob(mob_id)
    if(result is None):
         return{
                "message":"삭제된거 없어요"
         }
    
    return{
           "message":"삭제했습니다."
    }


# 글 수정 요청이 아니라.. id로 글 정보 조회..
@router.get("/{id}")
def getOne_id(id : int):
    print(id, '기존의 데이터를 요청함')  #로그 남긴다. 디버깅이나 역추적
    result = data.get_one(id)
    if(result is None):
        return {
            "message":"no"
        }
    return result

# 데이터 글 갱신

@router.put("/")
def update_monster(monsterData:MonsterUpdate):
    updated = data.update_one(monsterData)
    if updated is None:
        raise HTTPException(status_code=404, detail="몬스터를 찾을 수 없습니다.")
    return {
        "message":"ok","monster": updated
    }