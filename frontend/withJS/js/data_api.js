API_SERVER = "http://127.0.0.1:8000";

async function getAllMobs() {
  try {
    const url = `${API_SERVER}/monsters`;
    //const re = await fetch(url)
    const re = await fetch(url, { method: "get" });
    //method :  get방식
    console.log("불러오기 성공");

    if (!re.ok) throw new Error("전체메뉴불러오지못함");
    return re.json(); // 서버로 부터 받은 데이터..
  } catch (error) {
    console.error(error);
    return [];
  }
}

async function searchMobs(keyword) {
  try {
    const url = `${API_SERVER}/monsters/search?word=${encodeURIComponent(keyword)}`;
    const re = await fetch(url, {
      method: "get",
    });
    if (!re.ok) throw new Error("검색어 불러오지못함");
    return re.json();
  } catch (error) {
    console.error(error);
    return [];
  }
}

// 서버에게 메뉴를 삭제해 달라고 요청
// 요청명: /menus/id값    메서드:  DELETE     넘길값 : id 값 필요 (path  파라미터 방식.. 쿼리로 보내도 됩니다.)
async function deleteMonster(mobId) {
  try {
    // 클라이언트가 서버에게 데이터를 보내는 방식
    // 1. 쿼리파라미터 방식  : url 뒤에 붙여서 보낸다.
    // ..  const url = "http://127.0.0.1:8000/menus?menuId="+menuId;  # ? 뒤에가 변수를 붙힌것이고

    // 2. path 파라미터방식 : url 경로에 포함해서 보냅니다.
    const url = `${API_SERVER}/monsters/${mobId}`; // 변수명 없이 그냥 값만 붙힌다..  path 파리미터방식

    // 3. request body : html문서의  body 숨겨서 보낸다. addMenu() 함수에서  post  보내는 방식

    //위와 같은 방법으로 상관없지만..
    const re = await fetch(url, {
      method: "DELETE",
    });
    if (!re.ok) throw new Error("항목 삭제에 실패함");
    //return re.json()    메뉴 추가 서비스는 호출위치로 리턴이 필수가 아니다.
    return re.json(); //필수는 아니지만 일반적으로 리턴을 하기도 합니다.
  } catch (error) {
    console.log(error);
    alert("항목 삭제 중 오류가 발생함");
  }
}

async function fetchMobById(id) {
  try {
    const url = `${API_SERVER}/monsters/${id}`;
    const re = await fetch(url, {
      method: "get",
    });
    if (!re.ok) throw new Error("글을 가져오지 못했어요");
    return re.json(); //필수는 아니지만 일반적으로 리턴을 하기도 합니다.
  } catch (error) {
    console.log(error);
    alert("글을 가져오는 중에 에러가 발샘 함.");
  }
}

async function updateMonster(mobObject) {
  try {
    const url = `${API_SERVER}/monsters`;
    const re = await fetch(url, {
      method: "PUT",
      headers: { "Content-Type": "application/json" }, //html  헤더의 문서의 종류가   json 이다
      body: JSON.stringify(mobObject), //html의 body영역에 넣은 값
    });
    if (!re.ok) throw new Error("수정에 실패함");
    //return re.json()    메뉴 추가 서비스는 호출위치로 리턴이 필수가 아니다.
    return re.json(); //필수는 아니지만 일반적으로 리턴을 하기도 합니다.
  } catch (error) {
    console.log(error);
    alert("수정 중 오류가 발생함");
    return null;
  }
}
