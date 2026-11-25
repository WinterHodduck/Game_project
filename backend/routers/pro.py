import json
from fastapi import APIRouter,Query
from typing import List
from pathlib import Path
from pydantic import BaseModel
from fastapi import UploadFile, File


# 공통 URL 접두사가 붙은 router 객체 생성
router = APIRouter(prefix="/api/pro", tags=["pro"])

# 게시글 데이터베이스가 저장된 경로
DATA_PATH = Path(__file__).resolve().parent.parent / "storage" / "pro.json"

class Pro(BaseModel):
    id:int
    name: str
    image: str
    job:str
    race:str
    description : str

def load_pro() -> List[dict]:
    if not DATA_PATH.exists():
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        return json.load(file)

# JSON 파일을 읽어서 파이썬 객체로 변환해 반환하는 함수, 여기선 리스트로 바뀜
@router.get("/", response_model=List[Pro])
def get_all_pro():
    return load_pro()

