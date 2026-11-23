import json
from fastapi import APIRouter
from pathlib import Path

router = APIRouter(prefix="/api/posts", tags=["posts"])

DATA_PATH = Path(__file__).parent.parent / "storage" / "posts.json"


def get_posts():
    with open(DATA_PATH, encoding="utf-8") as f:
        return json.load(f)


@router.get("")
def get_all_posts():
    return get_posts()


@router.get("/best")
def get_best_posts(limit: int = 5):
    return sorted(get_posts(), key=lambda p: p["likes"], reverse=True)[:limit]


@router.get("/latest")
def get_latest_posts(limit: int = 10):
    return sorted(get_posts(), key=lambda p: p["createdAt"], reverse=True)[:limit]
