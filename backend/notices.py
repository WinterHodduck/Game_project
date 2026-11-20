from datetime import datetime, timezone
import json
import os
from pathlib import Path
import threading
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/notices", tags=["notices"])

NOTICES_PATH = Path(__file__).parent / "storage" / "notices.json"
file_lock = threading.Lock()


class NoticeCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    category: str = "일반"
    author: str = "관리자"
    isPinned: bool = False
    isPublished: bool = True


class NoticeUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    content: str | None = Field(default=None, min_length=1)
    category: str | None = None
    author: str | None = None
    isPinned: bool | None = None
    isPublished: bool | None = None


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat()


def load_notices() -> list[dict]:
    if not NOTICES_PATH.exists():
        NOTICES_PATH.parent.mkdir(parents=True, exist_ok=True)
        save_notices([])
        return []
    with open(NOTICES_PATH, encoding="utf-8") as f:
        data = json.load(f)
        return data if isinstance(data, list) else []


def save_notices(notices: list[dict]) -> None:
    NOTICES_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = NOTICES_PATH.with_suffix(f"{NOTICES_PATH.suffix}.tmp")
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(notices, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, NOTICES_PATH)


def sort_notices(notices: list[dict]) -> list[dict]:
    return sorted(
        notices,
        key=lambda x: (
            0 if x.get("isPinned") else 1,
            -(datetime.fromisoformat(x["createdAt"]).timestamp()) if x.get("createdAt") else 0,
        ),
    )


@router.get("")
def list_notices(
    include_unpublished: bool = Query(default=False),
    category: str | None = Query(default=None),
):
    with file_lock:
        notices = load_notices()

    result = []
    for n in notices:
        if not include_unpublished and not n.get("isPublished", True):
            continue
        if category and n.get("category") != category:
            continue
        result.append(n)

    return sort_notices(result)


@router.get("/{notice_id}")
def get_notice(notice_id: str, increase_view: bool = True):
    with file_lock:
        notices = load_notices()
        for item in notices:
            if item.get("id") == notice_id:
                if increase_view:
                    item["views"] = int(item.get("views", 0)) + 1
                    save_notices(notices)
                return item

    raise HTTPException(status_code=404, detail="공지사항을 찾을 수 없습니다.")


@router.post("", status_code=201)
def create_notice(payload: NoticeCreate):
    new_notice = {
        "id": str(uuid4()),
        "title": payload.title.strip(),
        "content": payload.content,
        "category": payload.category,
        "author": payload.author,
        "isPinned": payload.isPinned,
        "isPublished": payload.isPublished,
        "views": 0,
        "createdAt": now_iso(),
        "updatedAt": None,
    }

    with file_lock:
        notices = load_notices()
        notices.append(new_notice)
        save_notices(notices)

    return new_notice


@router.patch("/{notice_id}")
def update_notice(notice_id: str, payload: NoticeUpdate):
    with file_lock:
        notices = load_notices()
        for idx, item in enumerate(notices):
            if item.get("id") == notice_id:
                updates = payload.model_dump(exclude_unset=True)
                if "title" in updates and updates["title"] is not None:
                    updates["title"] = updates["title"].strip()
                updated = {
                    **item,
                    **updates,
                    "updatedAt": now_iso(),
                }
                notices[idx] = updated
                save_notices(notices)
                return updated

    raise HTTPException(status_code=404, detail="공지사항을 찾을 수 없습니다.")


@router.delete("/{notice_id}")
def delete_notice(notice_id: str):
    with file_lock:
        notices = load_notices()
        remaining = [n for n in notices if n.get("id") != notice_id]
        if len(remaining) == len(notices):
            raise HTTPException(status_code=404, detail="공지사항을 찾을 수 없습니다.")
        save_notices(remaining)

    return {"deleted": True, "id": notice_id}