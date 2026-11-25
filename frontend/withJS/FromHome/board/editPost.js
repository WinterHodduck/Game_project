const API = "http://localhost:8000/api/posts"; // 실제 서버 주소

const postId = new URLSearchParams(location.search).get("id");
// 수정 페이지의 쿼리 스트링에서의 id값을 postId에 저장

const editForm = document.getElementById("editForm"); // 네 개의 태그의 참조를 각각 변수에 저장
const category = document.getElementById("category");
const title = document.getElementById("title");
const content = document.getElementById("content");

// 기존 글을 불러와서 입력칸을 채우는 함수
async function loadPost() {
  try {
    const response = await fetch(`${API}/${postId}`); //  fetch에 method가 생략되면 기본값은 GET
    // FastAPI에 postId를 붙인 주소를 요청, 그 요청에 대한 응답 객체를 response에 저장
    if (!response.ok) {
      // 만약 response의 상태 코드가 200~299 사이에 있지 않다면
      const error = await response.json(); // error 변수에 response에 저장된 응답 객체의 본문을 JS객체로 변환 후 저장
      // 즉 이 경우에는, error에 {"detail": "..."} 평범한 객체 저장
      alert(error.detail); // detail키의 값을 사용자에게 보여줌
      location.href = "allPosts.html"; // 웹 브라우저의 주소를 "allPosts.html"로 이동
      return; // 함수를 종료
    } // 만약 response의 상태 코드가 200~299 사이에 있다면
    const post = await response.json(); // post 라는 변수에 response가 저장한 응답 객체의 본문을 JS객체로 변환 후 저장
    category.value = post.category; // 위에서 참조를 저장해둔 태그들의 입력칸의 값을
    title.value = post.title; // 각각  js 객체의 세 개의 키 (category, title, content)의 값으로 저장
    content.value = post.content;
  } catch (e) {
    // try문 코드를 실행하는 중 에러가 발생하면 catch문 실행
    console.error(e); // 에러 발생 객체의 정보를 담은 변수 e를 Console창에 보여줌 (에러 확인용)
    alert("서버와 통신 중 오류가 발생했습니다"); // 해당 문구를 사용자에게 보여줌
  }
}

// 수정 내용을 서버에 보내는 함수
async function updatePost() {
  try {
    const response = await fetch(`${API}/${postId}`, {
      // response라는 변수에 해당 주소로 요청한 응답 객체를 저장
      method: "PUT", // HTTP 메서드
      headers: { "Content-Type": "application/json" }, // 요청에 붙는 부가 정보, 본문이 JSON이라는 것을 FastAPI에게 알려주기 위함
      body: JSON.stringify({
        // FastAPI에게 보낼 JS 객체를 JSON 문자열로 전환
        category: category.value, // 보낼 데이터는 입력칸에 입력된 값
        title: title.value, // 총 3개의 키를 가지고 있다 : category, title, content
        content: content.value, // 각각의 키의 값은 category, title, content 각 입력칸에 입력된 값으로 설정
      }),
    });

    if (!response.ok) {
      // 만약 response에 저장된 응답 객체의 상태 코드가 200~299의 범위를 벗어나면
      const error = await response.json(); // 변수 error에 response에 저장된 응답 객체의 본문을 js 객체로 변환 후 저장
      alert(
        // 즉 이 경우에는, error에 {"detail": "..."} 평범한 객체 저장
        typeof error.detail === "string" ? error.detail : "입력값을 확인하세요",
      ); // 삼항연산자로, error의 본문 객체의 detail 키가 문자열이라는 조건. 참일 경우 detail 값 출력.
      // 거짓일 경우, 즉, error의 상태코드가 422면 detail이 문자열이 아닌 배열이기 때문에 해당 문구 출력
      return; // 함수 종료
    }
    alert("수정되었습니다"); // 만약 위의 response에 저장된 응답 객체의 상태 코드가 200~299 안에 있으면 아래의 코드 실행
    location.href = `postDetail.html?id=${postId}`; // 현재 웹 브라우저의 주소를 postId값에 맞춰서 postDetail.html로 이동
  } catch (e) {
    // try문 실행 시 에러 발생시 catch문 실행
    console.error(e); // 에러 발생 정보를 담은 객체를 변수 e에 저장하고 콘솔창에 띄움
    alert("서버와 통신하는 중 오류가 발생했습니다"); // 사용자에게 해당 문구를 보여줌
  }
}

editForm.addEventListener("submit", (e) => {
  // editForm 이라는 id를 가진 태그에 이벤트 발생 함수 설정, e는 이벤트 객체
  e.preventDefault(); // submit 이라는 이벤트 발생 시, 이벤트 발생 대상인 폼 제출의 기본동작을 막음
  updatePost(); // updatePost 함수 실행
});

loadPost(); // loadPost 함수 실행
