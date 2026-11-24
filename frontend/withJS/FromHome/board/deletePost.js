const API = "http://localhost:8000/api/posts"; // 실제 서버 주소

// 게시글 삭제 함수
async function deletePost(postID) {
  // 실수로 삭제 버튼이 눌리는 것을 방지하기 위한 확인창
  if (!confirm("정말 이 게시글을 삭제할까요?")) return;

  try {
    const response = await fetch(`${API}/posts/${postID}`, {
      method: "DELETE",
    });

    if (!response.ok) {
      const error = await response.json();
      alert(error.detail);
      return;
    }

    alert("삭제되었습니다");
    loadPosts();
  } catch (e) {
    alert("서버와 통신하는 중 오류가 발생했습니다");
  }
}
