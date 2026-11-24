from fastapi import APIRouter, HTTPException
from service import data

router = APIRouter(prefix="/monsters", tags=["monsters"])


@router.get("")
def get_monsters():
    return data.get_all()


@router.get("/search")
def search_monsters(word: str = ""):
    if not word.strip():
        return data.get_all()
    return data.search_Word(word)


@router.get("/{mob_id}")
def get_monster(mob_id: int):
    for m in data.get_all():
        if m.get("id") == mob_id:
            return m
    raise HTTPException(status_code=404, detail="몬스터를 찾을 수 없습니다.")