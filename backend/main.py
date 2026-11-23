from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from routers.notices import router as notices_router #추가

app = FastAPI()

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

app.include_router(notices_router)