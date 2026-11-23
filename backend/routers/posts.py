import json
from fastapi import APIRouter,Query
from pathlib import Path
from datetime import datetime
from pydantic import BaseModel, Field

# 공통 URL 접두사가 붙은 router 객체 생성
router = APIRouter(prefix="/api/posts", tags=["posts"])

# 게시글 데이터베이스가 저장된 경로
DATA_PATH = Path(__file__).parent.parent / "storage" / "posts.json"

# JSON 파일을 읽어서 파이썬 객체로 변환해 반환하는 함수, 여기선 리스트로 바뀜
def get_posts():
    with open(DATA_PATH, encoding="utf-8") as f:
        return json.load(f)

# get/api/posts 요청이 오면 실행되는 api 핸들러
@router.get("")
# 아래의 함수는 쿼리 파라미터를 통해서 기본값과 검증 규칙을 설정했다. 
# 매개변수로 page와 size를 갖고 각각의 기본값은 1과 10으로 설정. 
# page는 1이상, size는 1이상 50이하의 검증 규칙 추가
def get_all_posts(page: int = Query(1,ge=1),size:int = Query(10,ge=1,le=50)):
    posts = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    # 위의 get_posts() 함수를 사용한 posts = get_posts()와 결과는 같다
    # DATA_PATH의 데이터를 문자열로 읽겠다. 한글 깨짐을 방지하기 위해 인코딩 방식은 "utf-8"로 설정
    # 이렇게 받아온 데이터를 json 형식으로 받으므로, 결국 리스트로 읽겠다는 의미. 이를 posts 라는 변수에 저장
    posts.sort(key=lambda p:p["createdAt"], reverse = True)
    # posts에 저장된 배열을 정렬
    # 분류 기준은 람다식으로 설정한 키 값을 통해 분류
    # 리스트의 요소 하나 전체를  p에 저장, 그 객체의 createdAt 키의 값이 정렬의 기준값
    # 이 값들은 역순, 즉 내림차순으로 정렬

    #아래의 식은 게시판 페이지에서 프론트엔드가 번호 및 페이지 버튼을 그리는데 필요한 코드
    total = len(posts)  # 리스트의 길이, 즉 총 게시글 수
    start = (page -1)*size  # 페이지의 첫 게시글 인덱스
    return{
        "total" : total,  
        "page" : page,
        "size" : size,
        "totalPages":(total+size -1) //size,    # 필요한 전체 페이지 수
        "items":posts[start:start+size]     # 슬라이싱: start번째부터 start+size번째 직전까지 자르기
    }


# 추천 글을 보여주는 함수
@router.get("/best")
def get_best_posts(limit: int = Query(5,ge=1, le=50)): 
    # limit라는 매개변수를 가지고 자료형은 정수, 기본값을 5로 설정, 1이상 50이하로 쿼리 검증
    return sorted(get_posts(), key=lambda p: p["likes"], reverse=True)[:limit]
# sorted는 sort와는 다르게 원본을 수정하지 않은채 새로운 리스트를 반환하기 때문에 limit로 바로 슬라이싱 가능

# 최신글을 보여주는 함수
@router.get("/latest")
def get_latest_posts(limit: int = Query(10,ge=1,le=50)):  
    # 위 함수와 동일한 매개변수, 단 기본값을 10으로 설정
    return sorted(get_posts(), key=lambda p: p["createdAt"], reverse=True)[:limit]
# 위의 sorted를 사용한 이유와 동일


# 클라이언트가 보내야 하는 데이터의 형태와 검증 규칙
class PostCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    author: str = Field(min_length=1, max_length=20)
    content: str = Field(min_length=1)

# 리스트를 JSON 파일로 저장하는 도우미 함수
def save_posts(posts):
    DATA_PATH.write_text(
        json.dumps(posts, ensure_ascii=False, indent=2), encoding="utf-8"
    )

# POST / api/posts 요청을 처리하는 핸들러
@router.post("",status_code=201)
def create_post(body: PostCreate):
    posts = get_posts()
    new_post = {
        "id" : max((p["id"] for p in posts),default=0) +1,
        "title": body.title
    }