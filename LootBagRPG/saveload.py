import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Tuple, Optional

def get_base_dir() -> Path:
    #Returns correct save directory regardless if running in .py or .exe
    if getattr(sys, 'frozen', False): #if running as .exe
        return Path(sys.executable).parent #temp pyinstaller directory
    return Path(__file__).resolve().parent #if running as .py script

BASE_DIR = get_base_dir()
SAVE_DIR = BASE_DIR / "saves"
SAVE_DIR.mkdir(exist_ok=True) #make save directory if it didnt exist

def get_save_path(filename) -> Path:
    return SAVE_DIR / filename

def list_saves() -> list[Path]:
    return sorted(SAVE_DIR.glob("*.json"), key=lambda f: f.stat().st_mtime, reverse=True)

def get_save_preview(path) -> dict:
    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
            hero = data.get("hero", {})
            return {
                "filename": path.name,
                "modified": datetime.fromtimestamp(path.stat().st_mtime),
                "name": hero.get("name", "Unknown"),
                "level": hero.get("level", "?"),
                "gold": hero.get("gold", "?")
            }
    except Exception:
            name, level, gold = "Corrupted", "-", "-"
    
    modified = datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
    return f"{path.name} | {modified} | {name} | (Level {level}, {gold}g)"

def save_game(hero, enemy, game_state, shop: Optional[dict] = None):

    #create filename by using hero.name
    SAVE_FILE = f"{hero['name']}.json"
    SAVE_PATH = get_save_path(SAVE_FILE)

    data = {
        "hero": hero,
        "enemy": enemy,
        "game_state": game_state,
        "shop": shop
    }

    with SAVE_PATH.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    print(f"Game saved to {SAVE_PATH}")

def load_game(filename) -> Tuple[Optional[dict], Optional[dict], Optional[dict], Optional[dict]]:

    SAVE_PATH = get_save_path(filename)

    if not SAVE_PATH.exists():
        print("Save file not found.")
        #change to return default savegame?
        return None, None, None, None
    
    try:
        last_modified = datetime.fromtimestamp(SAVE_PATH.stat().st_mtime)

        with SAVE_PATH.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return data.get("hero"), data.get("enemy"), data.get("game_state"), data.get("shop")
    
    except Exception as e:
        print(f"Error loading save: {e}")
        #change to return default savegame?
        return None, None, None, None
    
def delete_save(filename):

    SAVE_PATH = get_save_path(filename)

    if SAVE_PATH.exists():
        SAVE_PATH.unlink()
        print(f"{SAVE_PATH} Deleted.")
    else:
        print(f"{SAVE_PATH} Save File Not Found.")