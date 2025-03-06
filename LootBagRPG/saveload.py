import json
import os

SAVE_FILE = "savegame.json"

def save_game(hero, enemy, game_state, shop: dict = None):

    #create filename by using hero.name
    SAVE_FILE = f"{hero['name']}"

    data = {
        "hero": hero,
        "enemy": enemy,
        "game_state": game_state,
        "shop": shop
    }

    #try:
    with open(SAVE_FILE, "w") as file:
        #for item in data:
            #print(f"{item}: {data.get(item)}")
            #for subitem in value:
                #print(f"{subitem}: {subitem.get(subitem)}")
        json.dump(data, file, indent=4)
    print(f"Game saved to {SAVE_FILE}.json")

    #except Exception as e:
        #print(f"Error saving game: {e}")

def load_game(filename):
    if not os.path.exists(filename):
        print("Save file not found.")
        #change to return default savegame?
        return None, None, None
    
    try:
        with open(filename, "r") as file:
            data = json.load(file)
        print(f"{filename}.json Loaded Successfully.")
        return data.get("hero"), data.get("enemy"), data.get("game_state"), data.get("shop")
    
    except Exception as e:
        print(f"Error loading save: {e}")
        #change to return default savegame?
        return None, None, None, None
    
def delete_save(filename):
    if os.path.exists(filename):
        os.remove(filename)
        print(f"{filename} Deleted.")
    else:
        print(f"{filename} Save File Not Found.")