const API_BASE = "http://127.0.0.1:8000";

async function getAll() {
  try {
    const url = `${API_BASE}/api/pro`;
    //const re = await fetch(url)
    const re = await fetch(url, { method: "get" });

    if (!re.ok) throw new Error("불러오지못함");
    return re.json(); // 서버로 부터 받은 데이터..
  } catch (error) {
    console.error(error);
    return [];
  }
}
