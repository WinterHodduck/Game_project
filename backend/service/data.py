import json    #json 개념 정리하고 이거 사용하겠다..
# import os      #os (operation systme - 운영체제) 윈도우 자원을 사용하려고 한다.

# json 파일 위치
JSON_PATH = "./storage/white_desert_monsters.json"

# json 파일 읽기
def load_monsters():
    with open(JSON_PATH, "r", encoding="utf-8") as file:
        return json.load(file)

# json 파일 쓰기
def save_monsters():
    with open(JSON_PATH, "w", encoding="utf-8") as file:
        json.dump(monsters, file, ensure_ascii=False, indent=4)

# 시작과 동시에 json파일을 로드하여 menus배열에 저장
monsters = load_monsters()

#load_menus()에서 읽어온 id중 최고값을 찾아서 하나 증가 시킴. 
# 다음에 메뉴가 추가될때의  id 값
next_id = max((obj["id"] for obj in monsters),default=0)+1

def get_all():
    return monsters