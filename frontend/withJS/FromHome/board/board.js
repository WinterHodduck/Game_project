// 작성일 표시 함수 : 24시간 이내면 n시간전 , 이후면 날짜료 표기
function formatDate(createdAt) {
  const diff = Date.now() - new Date(createdAt).getTime();
  const minutes = Math.floor(diff / 60000);
  const hours = Math.floor(minutes / 60);

  if (minutes < 1) return "방금 전";
  if (minutes < 60) return `${minutes}분 전`;
  if (hours < 24) return `${hours}시간 전`;
  return createdAt.slice(0, 10).replaceAll("-", ".");
}

// 게시글 데이터를 서버로부터 받아서 저장할 변수
const API_URL = "http://127.0.0.1:8000";

async function loadPosts() {
  try {
    const [bestRes, latestRes] = await Promise.all([
      fetch(`${API_URL}/api/posts/best`),
      fetch(`${API_URL}/api/posts/latest`),
    ]);

    if (!bestRes.ok || !latestRes.ok) throw new Error("서버 응답 오류");

    const bestPosts = await bestRes.json();
    const latestPosts = await latestRes.json();

    renderList("bestList", bestPosts);
    renderList("latestList", latestPosts);
  } catch (err) {
    console.error("게시글 불러오기 실패", err);
  }
}

loadPosts();

// 게시글 목록에서 한 줄 보이게 만드는 함수 (추천/ 최신 둘다 사용)
function oneLine(post) {
  const li = document.createElement("li");
  li.className = "post-item";
  li.innerHTML = `
    <div class="post-likes">${post.likes}</div>
    <div class="post-body">
        <a class="post-title" href="readPostDetail.html?id=${post.id}">
            <span class="post-category">[${post.category}]</span>${post.title}
        </a>
        <div class = "post-data">
            <span>💬 ${post.comments}</span>
            <span>👁 ${post.views}</span>
            <span>${post.author}</span>
            <span>${formatDate(post.createdAt)}</span>
        </div>
    </div>`;
  return li;
}

// 위에서 만든 게시글 태그 li를 브라우저에서 랜더링하여 보이게 하는 함수
function renderList(targetID, list) {
  const target = document.getElementById(targetID);
  target.innerHTML = "";
  list.forEach((post) => target.appendChild(oneLine(post)));
}
