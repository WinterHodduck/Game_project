// 게시글 삭제 함수
async function deletePost(postID) {
  // 실수로 삭제 버튼이 눌리는 것을 방지하기 위한 확인창
  if (!confirm("정말 이 게시글을 삭제할까요?")) return;
  // 확인을 누르면 True, 취소를 누르면 False
  // 근데 !가 붙어있으므로 그 반대가 된다
  // 즉, 확인 버튼을 누르면 false 이므로 try문 실행
  // 만약 True라면,즉 취소를 눌렀다면 아래의 return 실행
  try {
    const response = await fetch(`${API}/${postID}`, {
      // response 변수에 서버가 돌려준 응답 객체를 저장
      method: "DELETE", // HTTP 메서드를 의미
    });

    if (!response.ok) {
      // 만약 서버가 성공 상태 코드를 응답하지 못한다면
      const error = await response.json(); // error 변수에 JSON을 자바스크립트 객체로 변환한 데이터 저장
      alert(error.detail); // detail 출력
      return; // 함수 종료
    }

    alert("삭제되었습니다"); // 만약 서버가 성공 상태 코드를 응답한다면 "삭제되었습니다" 출력
    loadPosts(); // 커뮤니티 첫 페이지로 돌아가기
  } catch (e) {
    // 서버에 아예 닿지 못한 경우 아래 코드 실행
    console.error(e); // F12 -> Console탭에서 에러 확인 가능
    alert("서버와 통신하는 중 오류가 발생했습니다"); // 해당 문구 출력
  }
}
