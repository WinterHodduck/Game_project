const API = "http://localhost:8000/api/posts"; // 서버의 실제 주소, 밑에서 요청을 보낼 때 사용
const PAGE_SIZE = 10; // size 값을 저장하기 위한 변수, 상수라 대문자 표기, 다만 이는 관례일뿐

const postList = document.getElementById("postList");
// 게시글들이 들어가는 태그 (postList)를 찾아서 그 요소의 참조를 변수 postList에 저장
const pageNumber = document.getElementById("pageNumber");
// 위와 동일하게 해당 요소의 참조를 변수 pageNumber에 저장

// 서버에 요청을 하기 위한 함수. fetch는 Promise를 반환하고 await로 그 결과를 기다림
async function loadPosts(page = 1) {
  // 매개변수 page, 기본값을 1로 설정, 이 기본값은 인자없이 부를 때 자동 설정됨
  const res = await fetch(`${API}?page=${page}&size=${PAGE_SIZE}`);
  // 서버 주소에 요청을 보냄. 이때 쿼리 파라미터도 인자값으로 같이 보냄
  // FASTAPI가 요청받은 주소를 통해 일치하는 주소를 가진 데코레이터를 찾아 처리 및 응답.
  // 그 결과로 실행된 get_all_posts 함수의 응답 객체 전체가 변수 res에 저장.
  // 이 응답 객체는 상태 코드, header, body를 포함하고 있고 JSON 문자열은 body에 들어있음
  const data = await res.json();
  // 응답 객체의 json 문자열을 자바스크립트 객체로 변환 후 변수 data에 저장
  renderPosts(data.items, data.total, data.page);
  // 이렇게 저장된 변수 data에 .점 연산자로 접근하여 각각의 값을 인자값으로 하여 renderPosts 함수 실행
  renderPageNumber(data.page, data.totalPages);
  // 위와 동일하게 함수 실행
}

// 게시글을 랜더링하는 함수
function renderPosts(items, total, page) {
  postList.innerHTML = items // items는  posts.py에서 start번째부터 start+size번째 직전까지 슬라이싱한 배열
    // .map 매서드를 통하여 배열 내의 요소 하나하나를 매개변수 p에 전달하고 (i는 인덱스) 함수 실행
    .map(
      (p, i) => `
  <tr>
    <td>${total - (page - 1) * PAGE_SIZE - i}</td>
    <td>[${escapeHtml(p.category)}]</td> 
    <td>
    <a href="postDetail.html?id=${p.id}">${escapeHtml(p.title)}</a>
    ${p.comments ? `<span class="cmt">[${p.comments}]</span>` : ""}
    </td>  
    <td>${escapeHtml(p.author)}</td>
    <td>${p.createdAt.slice(0, 10)}</td>
    <td>${p.views}</td>
    <td><button onclick="deletePost(${p.id})">삭제</button></td>
    <td><a href="editPost.html?id=${p.id}">수정</a></td>   
  </tr>
`,
    )
    .join("");
}

// 페이지 번호를 랜더링 하는 함수
function renderPageNumber(current, totalPages) {
  let html = "";
  for (let i = 1; i <= totalPages; i++) {
    html += `<button class="${i === current ? "active" : ""}" data-page="${i}">${i}</button>`;
  }
  // 현재 페이지가 변수 current와 같다면 button 태그 안에 class "active" 생성
  // 이 클래스는 추후 css 디자인 시 활용
  pageNumber.innerHTML = html;
  // 위의 반복문을 통해 만든 버튼들을 pageNumber 라는 객체에 삽입
}

// pageNumber 객체에 이벤트 위임
pageNumber.addEventListener("click", (e) => {
  // 생성한 이벤트는 클릭, 클릭하면 람다식 함수 실행
  // e는 발생한 이벤트의 정보를 담은 객체
  const page = e.target.dataset.page; // data-로 시작하는 속성은 dataset 객체로 접근해야 함
  if (page) {
    // page 라는 변수의 값이 존재한다면 (pageNumber안 빈공간 클릭 시 이벤트 발생을 막기 위함)
    loadPosts(Number(page)); // dataset 객체로 접근하여 얻은 값은 문자열이기 때문에 정수로 바꿔주자
    history.replaceState(null, "", `?page=${page}`); // fetch를 통해 데이터만 받아 화면을
    // 랜더링 했으므로 주소창은 바뀌지 않았음. 이 상태로 새로고침을 하게 되면 fetch로 받은 데이터를
    // 처음 주소창 기준의 화면으로 돌아감. 이를 방지하기 위해 주소창을 fetch로 받아온 데이터에 맞게
    // 변경해주기 위해 작성한 코드임. 이러면 새로고침해도 원래의 페이지로 돌아가지 않음.
  }
});

// 제목에 코드가 들어와도 태그로 해석되어 실행되지 않게 하기 위한 함수
function escapeHtml(str) {
  return String(str).replace(
    // replace 매서드를 사용하기 위해 str을 String으로 감싸 문자열로 읽음
    /[&<>"']/g, // 정규식: & < > " ' 해당 다섯 개의 문자를 전부 찾아내시오.
    // g는 global 전부 찾기 라는 의미를 가짐
    (
      c, // 찾은 글자 하나하나를 c에 대입하여 아래의 객체 속 해당하는 값으로 변환
    ) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[
        c
      ],
  );
}

// 첫 진입 시의 페이지를 결정
const initialPage =
  Number(new URLSearchParams(location.search).get("page")) || 1;
// location.search는 쿼리 스트링 부분을 의미
// new URLSearchParams을 통해 해당 쿼리 스트링을 다루기 쉬운 객체로 변환
// .get("page") > page의 값을 불러옴, 근데 문자열임. 그래서 마지막에 Number로 감싸 정수로 만듬
// 여기까지 구한 값이 false면, 즉 page의 값이 없거나 잘못되었다면 1로 설정
loadPosts(initialPage);
