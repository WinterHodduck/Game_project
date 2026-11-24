fetch("header.html")
  .then((res) => res.text()) // fetch가 데이터를 가져오는 것을 기다렸다고 성공하면 매개변수에 데이터 삽입
  // 위에서 가져온 데이터를 문자열 형태로 변환
  .then((html) => {
    // 첫번째 then에서 얻은 결과를 매개변수 html에 저장
    document.getElementById("header").innerHTML = html;
    // header라는 id의 태그 참조에 html 통째로 삽입
  });
