from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import monsters, notices, posts
from routers.monsters import mount_monster_images

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(notices.router)
app.include_router(monsters.router)
app.include_router(posts.router)

mount_monster_images(app)


@app.get("/")
def home():
    print("클라이언트가 /를 요청하였습니다.")
    return {"message": "환영합니다."}


@app.get("/ground")
def make_practice():
    print("연습 중입니다.")
    return {"message": "연습중입니다", "cnt": 2}
