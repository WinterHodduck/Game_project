# Live Server 반복 새로고침: `get_notice`

## 증상

공지 상세 페이지를 열면 `requestNotice()`가 반복 호출되고 페이지가 계속 다시 로드됐다.

## 실행 환경

- 프론트엔드: VS Code Live Server
- 백엔드: `uvicorn --reload`

## 원인

`backend/routers/notices.py`의 `get_notice()`는 기본적으로 `increase_view=True`로 실행된다. 조회수가 증가하면 `save_notices()`가 `backend/storage/notices.json`을 수정한다.

Live Server가 이 JSON 파일의 변경을 감지해 페이지를 새로고침하면, 상세 페이지가 다시 공지를 요청하고 조회수가 또 증가하는 반복이 생겼다. `if increase_view:` 블록을 주석 처리했을 때 반복이 멈춘 것으로 확인했다.

## 해결

조회수 증가 동작은 유지하고, Live Server가 해당 파일 변경을 감시하지 않도록 `.vscode/settings.json`에 제외 설정을 추가했다.

```json
{
    "liveServer.settings.ignoreFiles": [
        ".vscode/**",
        "**/*.scss",
        "**/*.sass",
        "**/*.ts",
        "**/backend/storage/notices.json"
    ]
}
```

설정을 저장한 뒤 Live Server를 재시작했다. 그 결과 반복 새로고침이 멈췄다.

## 참고

- `uvicorn --reload`는 별도로 JSON 감시를 설정하지 않았다면 보통 Python 파일 변경을 기준으로 재시작한다.
- 배포 환경에서는 로컬 Live Server의 파일 감시가 실행되지 않으므로 같은 새로고침 루프가 발생하지 않는다.
