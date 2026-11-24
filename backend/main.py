
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from routers.notices import router as notices_router #추가
from routers import monsters, posts

from fastapi import FastAPI
from service import data
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
# from pydantic import Field


a = FastAPI()


a.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

a.include_router(notices_router)
a.include_router(monsters.router)
a.include_router(posts.router)

a.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #오리진과 내 서버의 주소가 달라도 즉 출저가 달라도 허용할께
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

a.mount("/image", StaticFiles(directory="storage/image"), name="image")

# 로비로 들어오는 서비스를 하나 제공하자.
@a.get("/")     # 첫 화면
def home():
    print("클라이언트가 /를 요청하였습니다.")
    return {
        "message":"환영합니다."
    }

@a.get("/ground")
def makePractice():
    print("연습 중입니다.")
    return {
        "message" : "연습중입니다",
        "cnt" : 2
    }

@a.get("/monsters")  #서비스 이름(요청): /menus   방법 get (조회 의도가 있다.)
def monsters():
    return data.get_all()  
    # data객체의 get_all함수에게 자료를 조회해 달라고 요청
    # 그 요청에 대한 응답을 받아서 클라이언트에 응답을 함.
    # 응답 타입이 리스트이다.. 그리고 그 리스트에는 딕셔너리 타입  > json으로 응답

## 클라이언트가 보낸 객체를 파이썬은 객체 구조를 이해 못한다.
## BaseModel은  Menu 객체의 변수에 값을 저장할 때. 타입이 맞는지 검사하는 도구
## id변수에는 정수, name 문자열 ...
class Monster(BaseModel):
    id:int
    name:str
    level : int
    habitat : str
    image : str

