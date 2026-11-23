const API = "http://localhost:8000/api/posts";
const postForm = document.getElementById("postForm");

postForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const body = {
    author: document.getElementById("author").value.trim(),
    title: document.getElementById("title").value.trim(),
    content: document.getElementById("content").value.trim(),
  };

  const res = fetch(API, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (res.ok) {
    location.href = "allPosts.html";
  } else {
    alert("등록에 실패했습니다. 입력값을 다시 확인해주세요");
  }
});
