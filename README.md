# 하얀 사막 프로젝트

![HTML](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)

하얀 사막을 주제로 한 몬스터 도감, 주인공 소개, 커뮤니티, 공지사항을 제공하는 풀스택 웹 프로젝트입니다. 프런트엔드는 HTML/CSS/Vanilla JavaScript로 구성하고, 백엔드는 FastAPI와 JSON 파일 기반 저장소로 구현했습니다.

현재 저장소에는 몬스터 102종, 게시글 51건, 공지사항 25건, 주인공 캐릭터 4명을 위한 데이터와 관련 이미지가 포함되어 있습니다.

## 목차

- [배포 주소](#배포-주소)
- [주요 화면](#주요-화면)
- [핵심 기능](#핵심-기능)
- [기술 스택](#기술-스택)
- [아키텍처 개요](#아키텍처-개요)
- [프로젝트 구조](#프로젝트-구조)
- [설치 방법](#설치-방법)
- [환경변수 및 전체 가이드](#환경변수-및-전체-가이드)
- [주요 API](#주요-api)
- [모델 권장(CPU 환경)](#모델-권장cpu-환경)
- [트러블슈팅](#트러블슈팅)
- [향후 로드맵](#향후-로드맵)

## 배포 주소

현재 프로젝트는 로컬 환경에서 실행되며 별도의 클라우드 배포 주소는 없습니다.

- 프런트엔드: VS Code Live Server 또는 로컬 정적 서버로 실행
- 백엔드 Swagger 문서: <http://127.0.0.1:8000/docs>
- 백엔드 루트: <http://127.0.0.1:8000/>

## 주요 화면

### 메인 화면

- 하얀 사막 소개 화면과 일일 퀘스트용 몬스터 추천 카드를 표시합니다.
- 몬스터 도감, 커뮤니티, 공지사항, 주인공 캐릭터, 관리자 페이지로 이동할 수 있습니다.
- 좌측 상단 로그인은 현재 화면 UI이며 실제 인증 기능은 연결되어 있지 않습니다.

### 몬스터 도감

- 몬스터 전체 목록을 표 형태로 제공합니다.
- 이름, 레벨, 서식지로 검색할 수 있습니다.
- 몬스터 이미지 클릭 시 원본 이미지를 모달로 확인할 수 있습니다.
- 레벨, 체력, 경험치, 공격력, 드랍 아이템, 설명 정보를 확인할 수 있습니다.

### 커뮤니티

- 추천 게시글과 최신 게시글을 카드형 목록으로 보여줍니다.
- 게시글 작성, 전체 목록 조회, 상세 조회, 수정, 삭제를 지원합니다.
- 게시글은 카테고리, 제목, 작성자, 내용으로 구성됩니다.
- 페이지네이션과 조회수, 추천수, 댓글 수 표시를 제공합니다.

### 공지사항

- 카테고리 필터와 제목/내용 검색을 지원합니다.
- 상단 고정 공지와 일반 공지를 구분합니다.
- 공지 작성, 상세 조회, 수정, 삭제와 조회수 증가를 지원합니다.
- 페이지당 항목 수와 페이지네이션을 제공합니다.

### 주인공 캐릭터

- 전사, 마법사, 은술사, 격투가 등 주인공 캐릭터를 카드로 보여줍니다.
- 캐릭터 이미지, 이름, 직업, 종족, 설명을 제공합니다.

### 관리자 페이지

- 몬스터 등록 및 드래그 앤 드롭 이미지 업로드를 지원합니다.
- 몬스터 전체 목록 모달에서 정보 수정과 삭제를 수행할 수 있습니다.

## 핵심 기능

- 몬스터 목록 조회와 이름/레벨/서식지 검색
- 몬스터 이미지 업로드 및 정적 이미지 제공
- 몬스터 등록, 조회, 수정, 삭제
- 게시글 추천 목록, 최신 목록, 전체 목록 조회
- 게시글 작성, 상세 조회, 수정, 삭제
- 공지사항 카테고리 필터, 검색, 상단 고정
- 공지사항 작성, 상세 조회, 수정, 삭제
- 주인공 캐릭터 목록 조회
- FastAPI Swagger UI를 통한 API 테스트

## 기술 스택

| 구분 | 사용 기술 |
| --- | --- |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Backend | Python, FastAPI |
| API 문서화 | Swagger UI / OpenAPI |
| 데이터 저장 | JSON 파일 |
| 이미지 제공 | FastAPI StaticFiles |
| 개발 도구 | VS Code, Live Server |

## 아키텍처 개요

```text
Browser / Live Server
        │
        │ HTTP Fetch
        ▼
FastAPI 서버 (127.0.0.1:8000)
        │
        ├─ /monsters
        ├─ /api/posts
        ├─ /api/notices
        └─ /api/pro
        │
        ▼
backend/storage/*.json
```

- 프런트엔드는 JavaScript `fetch`로 백엔드 REST API를 호출합니다.
- 몬스터 데이터는 메모리와 `white_desert_monsters.json`에 반영됩니다.
- 게시글과 공지사항은 대응하는 JSON 파일에 직접 읽기/쓰기를 수행합니다.
- 업로드된 몬스터 이미지는 `backend/storage/image/`에 저장되고 `/image` 경로로 제공됩니다.

## 프로젝트 구조

```text
Game_project/
├─ backend/
│  ├─ main.py                 # FastAPI 앱 생성 및 라우터 등록
│  ├─ routers/
│  │  ├─ monsters.py          # 몬스터 CRUD 및 이미지 업로드
│  │  ├─ posts.py             # 게시글 CRUD
│  │  ├─ notices.py           # 공지사항 CRUD 및 검색
│  │  └─ pro.py               # 주인공 캐릭터 조회
│  ├─ service/
│  │  └─ data.py              # 몬스터 데이터 로드 및 변경 로직
│  └─ storage/
│     ├─ *.json               # 서비스 데이터
│     └─ image/               # 몬스터 및 캐릭터 이미지
├─ frontend/withJS/
│  ├─ index.html              # 메인 화면과 몬스터 도감
│  ├─ admin/                  # 관리자 페이지
│  ├─ FromHome/
│  │  ├─ board/               # 커뮤니티 화면
│  │  ├─ notice/              # 공지사항 화면
│  │  └─ propage/             # 주인공 캐릭터 화면
│  ├─ css/
│  └─ js/
├─ testcode/
└─ README.md
```

## 설치 방법

### 1. 저장소 복제

```bash
git clone https://github.com/WinterHodduck/Game_project.git
cd Game_project
```

### 2. Python 가상환경 및 패키지 설치

```bash
python -m venv .venv
.venv\Scripts\activate
pip install fastapi uvicorn pydantic python-multipart
```

### 3. 백엔드 실행

프로젝트 루트가 아닌 `backend` 폴더를 기준으로 실행합니다.

```bash
cd backend
uvicorn main:app --reload
```

실행 확인:

- <http://127.0.0.1:8000/>
- <http://127.0.0.1:8000/docs>

### 4. 프런트엔드 실행

VS Code에서 `frontend/withJS/index.html`을 열고 Live Server로 실행하거나, 정적 서버를 사용합니다.

```bash
cd frontend/withJS
python -m http.server 5500
```

브라우저에서 <http://localhost:5500/> 또는 Live Server 주소로 접속합니다.

## 환경변수 및 전체 가이드

현재 프로젝트는 별도의 `.env` 파일이나 환경변수를 사용하지 않습니다. 프런트엔드의 API 주소는 각 JavaScript 파일에 `http://127.0.0.1:8000` 또는 `http://localhost:8000`으로 고정되어 있습니다.

포트나 서버 주소를 변경할 경우 다음 위치도 함께 수정해야 합니다.

- `frontend/withJS/js/data_api.js`
- `frontend/withJS/FromHome/board/*.js`
- `frontend/withJS/FromHome/notice/notice.js`
- `frontend/withJS/FromHome/propage/pro.js`
- `frontend/withJS/admin/admin_create.html`

백엔드를 프로젝트 루트가 아닌 `backend` 폴더에서 실행하지 않으면 JSON 경로나 이미지 경로를 찾지 못할 수 있으므로 위 실행 명령을 기준으로 실행하는 것을 권장합니다.

## 주요 API

| 기능 | Method | Endpoint |
| --- | --- | --- |
| 몬스터 전체 조회 | `GET` | `/monsters/` |
| 몬스터 검색 | `GET` | `/monsters/search?word=검색어` |
| 몬스터 단건 조회 | `GET` | `/monsters/{id}` |
| 몬스터 등록 | `POST` | `/monsters/` |
| 몬스터 수정 | `PUT` | `/monsters/` |
| 몬스터 삭제 | `DELETE` | `/monsters/{id}` |
| 몬스터 이미지 업로드 | `POST` | `/monsters/upload-image` |
| 게시글 목록 | `GET` | `/api/posts?page=1&size=10` |
| 추천 게시글 | `GET` | `/api/posts/best?limit=5` |
| 최신 게시글 | `GET` | `/api/posts/latest?limit=10` |
| 게시글 등록 | `POST` | `/api/posts` |
| 게시글 상세 조회 | `GET` | `/api/posts/{id}` |
| 게시글 수정 | `PUT` | `/api/posts/{id}` |
| 게시글 삭제 | `DELETE` | `/api/posts/{id}` |
| 공지사항 목록 | `GET` | `/api/notices?page=1&size=10` |
| 공지사항 상세 조회 | `GET` | `/api/notices/{id}` |
| 공지사항 등록 | `POST` | `/api/notices` |
| 공지사항 수정 | `PATCH` | `/api/notices/{id}` |
| 공지사항 삭제 | `DELETE` | `/api/notices/{id}` |
| 주인공 캐릭터 조회 | `GET` | `/api/pro/` |

API 요청 본문과 응답 예시는 실행 중인 서버의 `/docs`에서 확인할 수 있습니다.

## 모델 권장(CPU 환경)

이 프로젝트는 이미지 생성 AI 또는 대형 언어 모델을 서버에서 실행하지 않으며, 별도의 GPU가 필요하지 않습니다.

- 권장 CPU: 일반 2코어 이상
- 권장 메모리: 4GB 이상
- 권장 Python: 3.10 이상
- 권장 브라우저: 최신 Chrome 또는 Edge
- GPU: 필수 아님

백엔드와 정적 프런트엔드 서버를 동시에 실행할 수 있는 일반 개인용 컴퓨터에서 충분히 동작하도록 설계된 소규모 로컬 프로젝트입니다.

## 트러블슈팅

### `ModuleNotFoundError: No module named 'fastapi'`

가상환경을 활성화한 뒤 FastAPI와 관련 패키지를 설치합니다.

```bash
pip install fastapi uvicorn pydantic python-multipart
```

### 프런트엔드에서 데이터가 조회되지 않음

백엔드가 `127.0.0.1:8000` 또는 `localhost:8000`에서 실행 중인지 확인합니다.

```bash
cd backend
uvicorn main:app --reload
```

브라우저 개발자 도구의 Network 탭에서 API 요청 실패 여부와 상태 코드를 확인합니다.

### CORS 오류 발생

현재 백엔드의 CORS 설정은 모든 오리진을 허용합니다. 프런트엔드에서는 유효한 서버 주소로 요청하고 있는지 확인합니다.

### JSON 데이터가 저장되지 않음

프로젝트의 `backend/storage/*.json` 파일에 쓰기 권한이 있는지 확인합니다. 게시글이나 공지사항 작성 후 실제 JSON 파일이 갱신되는지 확인할 수 있습니다.

### 이미지 업로드 후 이미지를 찾을 수 없음

이미지는 `backend/storage/image/`에 저장됩니다. 백엔드가 `backend` 폴더를 기준으로 실행 중인지 확인하고 `/image/{파일명}` 경로로 접근되는지 확인합니다.

## 향후 로드맵

- 환경변수를 통한 API 주소 및 포트 구성
- 로그인과 관리자 권한 인증 기능 구현
- 데이터베이스 연동 및 게시글 좋아요/댓글 저장 구조 개선
- 이미지 파일명과 공개 URL 관리 체계 개선
- 공지사항 및 게시글 검색 기능 고도화
- 반응형 UI와 공통 컴포넌트 정리
- 프런트엔드 빌드 도구 도입
- 테스트 코드 및 자동화된 API 테스트 추가
- Docker 또는 클라우드 환경 배포
