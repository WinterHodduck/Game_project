API_SERVER = "http://127.0.0.1:8000";

async function getAllMob() {
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
