import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "storage" / "white_desert_monsters.json"


# json 파일 읽기
def load_monsters():
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


# json 파일 쓰기
def save_monsters(monsters_list):
    with open(DATA_PATH, "w", encoding="utf-8") as file:
        json.dump(monsters_list, file, ensure_ascii=False, indent=4)


# 시작과 동시에 json파일을 로드하여 monsters 리스트에 저장
monsters = load_monsters()

next_id = max((obj.get("id", 0) for obj in monsters), default=0) + 1


def get_all():
    return monsters


# 검색기능
def search_Word(word):
    result = []
    q = str(word).strip()
    for m in monsters:
        name = str(m.get("name", ""))
        level = str(m.get("level", ""))
        habitat = str(m.get("habitat", ""))
        if q in name or q in level or q in habitat:
            result.append(m)
    return result


def add_monster(payload: dict):
    global next_id
    next_id = max([m.get("id", 0) for m in monsters], default=0) + 1

    new_monster = {
        "id": next_id,
        "name": payload.get("name", ""),
        "level": payload.get("level", 1),
        "habitat": payload.get("habitat", ""),
        "hp": payload.get("hp", 0),
        "exp": payload.get("exp", 0),
        "attack": payload.get("attack", 0),
        "drops": payload.get("drops", []),
        "description": payload.get("description", ""),
        "image": payload.get("image", "./image/monster01.jpg"),
    }

    monsters.append(new_monster)
    save_monsters(monsters)
    next_id += 1
    return new_monster

# id 로 데이터 삭제하는 함수
def delete_mob(mob_id):                       #enumerate 이 함수를 사용하면 인덱스와 값을 가져올 수 있다.
    for index, mob in enumerate(monsters):  # 삭제할 데이터를 찾을 때는 id로 찾고
                                          # 리스트에서 지울 때는 인덱스 번호로 지운다.. 
                                          # 그래서 리스트이 번호와 메뉴의 정보인 값이 모두 필요함
        if mob["id"]== mob_id:  #  삭제할 메뉴..
            monsters.pop(index)
            save_monsters(monsters)  #menus의 내용이 변경되었으니 json파일도 변경되어야 함
            return mob_id       #삭제가 되었다면  삭제한 아이디를 리턴
    return None   #삭제한 데이터가 없다면   None 리턴됨

# id로 데이터를 검색하는 함수
def get_one(id):
    for obj in monsters:
        if(obj["id"] == id):
            return obj
    return None

# 클라이언트가 보낸 수정할 데이트로 실제 데이터를 수정하는 코드
def update_one(idData):  #객체를 받는다.
    for obj in monsters:
        #menu변수는 딕셔너리이고,  menudata는 클래스 객체라서 변수 접근 방식이 다름.
        if(obj["id"]==idData.id):
            obj["name"]=idData.name
            obj["level"]=idData.level
            obj["habitat"]=idData.habitat
            obj["hp"]=idData.hp
            obj["exp"]=idData.exp
            obj["drops"]=idData.drops
            obj["attack"]=idData.attack
            obj["description"]=idData.description
            if getattr(idData, "image", None):
                obj["image"] = idData.image
            save_monsters(monsters)
            return obj  # 수정이 되면 끝난 것이니 리턴해서 마무리 해
    return None