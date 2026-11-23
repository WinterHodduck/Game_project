from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from routers import monsters, posts

app = FastAPI()

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

app.include_router(monsters.router)
app.include_router(posts.router)
