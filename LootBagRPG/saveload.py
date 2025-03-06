import json
import os

SAVE_FILE = "savegame.json"
SAVE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saves")
os.makedirs(SAVE_DIR, exist_ok=True)


def get_save_path(filename):
    return os.path.join(SAVE_DIR, filename)

def save_game(hero, enemy, game_state, shop: dict = None):

    #create filename by using hero.name
    SAVE_FILE = f"{hero['name']}.json"
    SAVE_PATH = get_save_path(SAVE_FILE)

    data = {
        "hero": hero,
        "enemy": enemy,
        "game_state": game_state,
        "shop": shop
    }

    #try:
    with open(SAVE_PATH, "w") as file:
        #for item in data:
            #print(f"{item}: {data.get(item)}")
            #for subitem in value:
                #print(f"{subitem}: {subitem.get(subitem)}")
        json.dump(data, file, indent=4)
    print(f"Game saved to {SAVE_PATH}")

    #except Exception as e:
        #print(f"Error saving game: {e}")

def load_game(filename):

    SAVE_PATH = get_save_path(filename)

    if not os.path.exists(SAVE_PATH):
        print("Save file not found.")
        #change to return default savegame?
        return None, None, None, None
    
    try:
        with open(SAVE_PATH, "r") as file:
            data = json.load(file)
        print(f"{SAVE_PATH} Loaded Successfully.")
        return data.get("hero"), data.get("enemy"), data.get("game_state"), data.get("shop")
    
    except Exception as e:
        print(f"Error loading save: {e}")
        #change to return default savegame?
        return None, None, None, None
    
def delete_save(filename):

    SAVE_PATH = get_save_path(filename)

    if os.path.exists(SAVE_PATH):
        os.remove(SAVE_PATH)
        print(f"{SAVE_PATH} Deleted.")
    else:
        print(f"{SAVE_PATH} Save File Not Found.")