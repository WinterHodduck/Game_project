import json
from fastapi import APIRouter,Query
from pathlib import Path
from datetime import datetime
from pydantic import BaseModel, Field

# 공통 URL 접두사가 붙은 router 객체 생성
router = APIRouter(prefix="/api/posts", tags=["posts"])

# 게시글 데이터베이스가 저장된 경로
DATA_PATH = Path(__file__).parent.parent / "storage" / "posts.json"

# JSON 문자열을 파이썬 리스트로 변환하는 함수
def get_posts():
    with open(DATA_PATH, encoding="utf-8") as f:
        return json.load(f)
    # json.load()는 파일 객체를, json.loads()는 문자열을 바로 읽음

# get/api/posts 요청이 오면 실행되는 api 핸들러
@router.get("")
# 아래의 함수는 쿼리 파라미터를 통해서 기본값과 검증 규칙을 설정했다. 
# 매개변수로 page와 size를 갖고 각각의 기본값은 1과 10으로 설정. 
# page는 1이상, size는 1이상 50이하의 검증 규칙 추가
def get_all_posts(page: int = Query(1,ge=1),size:int = Query(10,ge=1,le=50)):
    posts = get_posts()
    posts.sort(key=lambda p:p["createdAt"], reverse = True)
    # posts에 저장된 리스트를 정렬
    # 분류 기준은 람다식으로 설정한 키 값을 통해 분류
    # 리스트의 요소 하나 전체를  p에 저장, 그 딕셔너리의 createdAt 키의 값이 정렬의 기준값
    # 이 값들은 역순, 즉 내림차순으로 정렬

    #아래의 코드는 게시판 페이지에서 프론트엔드가 번호 및 페이지 버튼을 그리는데 필요한 코드
    total = len(posts)  # 리스트의 길이, 즉 총 게시글 수
    start = (page -1)*size  # 페이지의 첫 게시글 인덱스
    return{
        "total" : total,  
        "page" : page,
        "size" : size,
        "totalPages":(total+size -1) //size,    # 누락되는 페이지를 막기 위한 올림 나눗셈 사용
        "items":posts[start:start+size]     # 슬라이싱: start번째부터 start+size번째 직전까지 자르기
    }


# 추천 글을 보여주는 함수
@router.get("/best")
def get_best_posts(limit: int = Query(5,ge=1, le=50)): 
    # limit라는 매개변수를 가지고 자료형은 정수, 기본값을 5로 설정, 1이상 50이하로 쿼리 검증
    return sorted(get_posts(), key=lambda p: p["likes"], reverse=True)[:limit]
# sorted는 sort와는 다르게 정렬된 리스트를 반환하기 때문에 limit로 바로 슬라이싱 가능

# 최신글을 보여주는 함수
@router.get("/latest")
def get_latest_posts(limit: int = Query(10,ge=1,le=50)):  
    # 위 함수와 동일한 매개변수, 단 기본값을 10으로 설정
    return sorted(get_posts(), key=lambda p: p["createdAt"], reverse=True)[:limit]
# 위의 sorted를 사용한 이유와 동일
# .sort()는 None을 반환하기 때문에 .sort()[:limit]처럼 슬라이싱 불가



# 클라이언트가 보내야 하는 데이터의 형태와 검증 규칙
class PostCreate(BaseModel): # PostCreate 라는 새로운 클래스 생성, BaseModel이라는 클래스 상속
    # BaseModel의 역할은 클라이언트가 보낸 요청 본문을 검증. 다만, FastAPI가 먼저 역직렬화 하고 검증 
    # 검증을 통과한 요청 데이터를 PostCreate 인스턴스로 변환 
    category: str 
    title: str = Field(min_length=1, max_length=100)    # 네 개의 변수 모두 공통적인 검증 조건은
    author: str = Field(min_length=1, max_length=20)    # str을 통해 각 필드의 자료형은 문자열로 제한하고
    content: str = Field(min_length=1)      # Field를 통해 세 개의 필드(클래스 속성)값에 대한 추가 제약 조건

# 리스트를 JSON 파일로 저장하는 도우미 함수
def save_posts(posts):  # 서버 내부 함수이므로 서버 코드(create_post)가 넘긴 인자값을 매개변수 posts로 받음
    DATA_PATH.write_text(   #DATA_PATH에 덮어쓰기
        json.dumps(posts, ensure_ascii=False, indent=2), encoding="utf-8"
    )   # posts로 받은 인자값을 한글이 깨지지 않게 
        # 보기좋게 두 칸씩 들여쓰기 해서, 파이썬 리스트를 JSON 문자열로 변환

# POST /api/posts 요청을 처리하는 핸들러
@router.post("",status_code=201)    # POST /api/posts의 주소로 오는 요청에 대해서, 
                                    # 성공하면 상태 코드 201로 응답 
def create_post(body: PostCreate):  # FastAPI가 요청 본문을 PostCreate 규칙으로 검증하고
    # PostCreate 인스턴스로 변환해서, body에 넣어줌. body.title 처럼 . 점표기법을 통해 접근한다. 
    # 만약 검증에 실패할 경우, 이 함수는 실행되지 않고 422로 응답 
    posts = get_posts() # get_posts() 함수를 통해 불러온 파이썬 리스트를 posts에 저장
    new_post = {    # new_post 변수에 딕셔너리 저장
        "id" : max((p["id"] for p in posts),default=0) +1,  # posts의 리스트의 요소 하나씩 꺼내어
        # p에 놓고 id 키에 해당하는 값을 뽑는다, 그 중에서 가장 큰 값을 선택. 거기에 1을 더해 새 id 생성 
        # 리스트가 비어 있는 경우, max값이 존재할 수 없으므로 에러 방지 기본값을 0으로 설정 
        "category" : body.category,
        "title": body.title,
        "author" : body.author,
        "content" : body.content,
        "views":0,
        "likes" : 0,
        "comments":0,
        "createdAt" : datetime.now().isoformat(timespec="seconds"), # datetime은 표준 라이브러리
                # .isoformat 메서드를 통해  국제 표준 방식의 문자열로 바꿈. 단위는 초, 따라서 뒤의 마이크로초 제거
    }
    posts.append(new_post)      # 기존 메모리 속 리스트에 새로 만든 딕셔너리를 추가함
    save_posts(posts)       # 새로 만든 딕셔너리가 추가된 리스트를 저장함
    return new_post     # 위의 딕셔너리를 호출한 곳으로 반환함 
