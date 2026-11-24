const API = "http://localhost:8000/api/posts"; // 실제 서버 주소
const postForm = document.getElementById("postForm");
// postForm 아이디를 가진 태그의 참조를 변수 postForm에 저장

// postForm에 이벤트 리스너 등록, 이벤트 종류는 제출
// 이벤트 리스너는 이벤트 발생 시 자동으로 이벤트 객체를 만들어서 함수의 첫번째 인자값(여기서는 e)으로 넘겨줌
// 각각의 이벤트마다 이벤트 객체는 다름(click -> MouseEvent, submit -> SubmitEvent 등등)
// submit 이벤트 객체 자체를 변수 e에 저장
// 이 함수 안에서 await를 쓰기 위해 async 표시
postForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  // 폼 제출에 따른 브라우저의 기본동작, 즉 데이터 전송 + 페이지 이동을 막기 위해 메서드 preventDefault() 사용

  const body = {
    // body 변수에 객체를 저장. 해당 객체는 총 3개의 key로 구성되어 있음.
    // 각각의 키는 클라이언트가 "작성자, 제목, 내용" 입력칸에 입력한 내용을 앞뒤 공백 제거한 형태의 값을 가짐
    author: document.getElementById("author").value.trim(),
    title: document.getElementById("title").value.trim(),
    content: document.getElementById("content").value.trim(),
  };

  const res = await fetch(API, {
    // fetch는 결과를 바로 돌려주지 않고 Promise객체를 반환하기 때문에 await 필요
    // Promise가 완료될 때까지 이 줄에서 기다렸다가 결과를 받음
    // fetch가 서버에 요청을 보내는데, 이 때, 두번째 인자값은 요청 설정 객체.
    // 이 요청 설정 객체는 요청의 방식, 부가 정보, 본문을 담고 있음
    // 이 요청에 대해서 서버가 응답한 결과물을 변수 res에 저장
    method: "POST", //  보내는 데이터의 요청의 종류를 나타냄, 서버에 새 데이터를 추가해달라는 요청
    headers: { "Content-Type": "application/json" }, // FastAPI 서버에게 body가 JSON 형태임을 알려줌
    body: JSON.stringify(body), // 객체를 저장한 위의 변수 body를 문자열로 바꿈.
    // 자바스크립트 객체는 메모리 안의 구조라서 그대로 보낼 수 없기 때문에 텍스트 형식으로의 변환(직렬화) 필요
  });

  if (res.ok) {
    // 만약 변수 res를 통한 요청에 대해서 서버가 성공 상태 코드로 응답한다면,
    // 즉, 응답 상태 코드가 200~299(성공 범위)에 있다면
    location.href = "allPosts.html"; // 웹페이지의 주소를 ""안에 있는 주소로 변경하고 페이지 이동
  } else {
    // 만약 서버가 요청에 대해서 응답 실패 코드를 준다면 아래의 메세지 출력
    alert("등록에 실패했습니다. 입력값을 다시 확인해주세요");
  }
});
