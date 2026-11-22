import json
from fastapi import APIRouter,Query
from pathlib import Path

router = APIRouter(prefix="/api/posts", tags=["posts"])

DATA_PATH = Path(__file__).parent.parent / "storage" / "posts.json"


def get_posts():
    with open(DATA_PATH, encoding="utf-8") as f:
        return json.load(f)


@router.get("")
def get_all_posts(page: int = Query(1,ge=1),size:int = Query(10,ge=1,le=50)):
    #게시글 최신순 배열
    posts = json.load(DATA_PATH.read_text(encoding="utf-8"))
    posts.sort(key=lambda p:p["createdAt"], reverse = True)

    total = len(posts)
    start = (page -1)*size  # 페이지의 첫 게시글 인덱스
    return{
        "total":total,
        "page" : page,
        "size" : size,
        "totalPages":(total+size -1) //size,
        "items":posts[start:start+size]
    }


@router.get("/best")
def get_best_posts(limit: int = 5):
    return sorted(get_posts(), key=lambda p: p["likes"], reverse=True)[:limit]


@router.get("/latest")
def get_latest_posts(limit: int = 10):
    return sorted(get_posts(), key=lambda p: p["createdAt"], reverse=True)[:limit]
