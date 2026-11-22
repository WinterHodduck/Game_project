const API = "http://localhost:8000/api/posts";
const PAGE_SIZE = 10;

const postList = document.getElementById("postList");
const pageNumber = document.getElementById("pageNumber");

async function loadPosts(page = 1) {
  const res = await fetch(`${API}?page=${page}&size=${PAGE_SIZE}`);
  const data = await res.json();
}
