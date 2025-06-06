#LootBagRPG
#Text-Based MVP
from character import Hero, Enemy
from loot_bag import LootBag
from inventory import Inventory
import os
import time
import msvcrt
from items import Item, Weapon, Potion
from shop import Shop
from saveload import *
from help_messages import *
import re

UI_WIDTH = 50

def strip_ansi(text: str) -> str:
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

def format_stat_line(label: str, bar_str: str, value_str: str) -> str:
    """
    Returns a formatted line with ANSI-safe padding.
    """
    full_text = f"   {label} {bar_str} {value_str}"
    visible_length = len(strip_ansi(full_text))
    padding = UI_WIDTH - visible_length
    return full_text + ' ' * max(padding, 0)

def draw_boxed_ui(lines: list[str], title: str = None):
    """
    Draws a box with an optional centered title and aligned lines.
    """
    print("╔" + "═" * UI_WIDTH + "╗")
    if title:
        print(f"║ {title:^{UI_WIDTH - 2}} ║")
    for line in lines:
        print(f"║{line}║")
    print("╚" + "═" * UI_WIDTH + "╝")

def pause_without_buffering(duration_ms):
    end_time = time.time() + duration_ms / 1000
    while time.time() < end_time:
        while msvcrt.kbhit():
            _ = msvcrt.getch()
            time.sleep(.001)
        time.sleep(.001)

    while msvcrt.kbhit():
        _ = msvcrt.getch()

def main_settings_menu() -> None:
    global options_list
    if options_list is None:
        options_list = [True, True]
    os.system("cls")
    print("Settings:")
    print(f"[1] AutoEncounter")
    print(f"[2] AutoPickup")
    print(f"[3] Main Menu")
    print(f"...or press <ENTER> to go back")
    menu_option = input("Please Select An Option... ")
    if menu_option in ["1"]:
        os.system("cls")
        print("AutoEncounter Settings:")
        print(f"[1] AutoEncounter On: The next enemy is automatically generated by pressing <ENTER> after an enemy is killed.")
        print(f"[2] AutoEncounter Off: The next enemy must be manually encountered after an enemy is killed.")
        menu_option = input("Please Select An Option... ")
        auto_encounter = True if menu_option in ["1"] else False
        print(f"AutoEncounter: {auto_encounter}")
        options_list[0] = auto_encounter
        main_settings_menu()
    elif menu_option in ["2"]:
        os.system("cls")
        print("AutoPickup Settings:")
        print(f"[1] AutoPickup On: Items will automatically be picked up by pressing <ENTER> after an enemy is killed.")
        print(f"[2] AutoPickup Off: Items must be manually picked up after an enemy is killed.")
        menu_option = input("Please Select An Option... ")
        auto_pickup = True if menu_option in ["1"] else False
        print(f"AutoPickup: {auto_pickup}")
        options_list[1] = auto_pickup
        main_settings_menu()
    elif menu_option in ["3"]:
        main_menu()
    elif menu_option in [""]:
        main_menu()

def main_menu() -> None:
    global options_list
    if options_list is None:
        options_list = [True, True]
    os.system("cls")
    #print(f"Welcome To Lootbag RPG!")
    print("""
     _                _   _                   ____  ____   ____ 
    | |    ___   ___ | |_| |__   __ _  __ _  |  _ \|  _ \ / ___|
    | |   / _ \ / _ \| __| '_ \ / _` |/ _` | | |_) | |_) | |  _ 
    | |__| (_) | (_) | |_| |_) | (_| | (_| | |  _ <|  __/| |_| |
    |_____\___/ \___/ \__|_.__/ \__,_|\__, | |_| \_\_|    \____|
                                      |___/                     
    """)
    print(f"____________________________")
    print(f"Main Menu")
    options = ["Play", "Load Saved Game", "Settings", "Quit"]
    auto_option = ["Play"]
    action_input = option_menu(options, auto_option)
    if action_input == "":
        return
    if action_input == 0:
        return
    elif action_input == 1:
        load_menu()
    elif action_input == 2:
        main_settings_menu()
    elif action_input == 3:
        exit()

def option_menu(options: list, auto_option: str = None) -> str:
    print(f"___________________________")
    print(f"OPTIONS: ")
    for i, option in enumerate(options):
        print(f"[{i+1}] {option}")
    if auto_option:
        print(f"...or press <ENTER> to {auto_option}")
    print(f"___________________________")
    #Pause to prevent danger when holding keys
    pause_without_buffering(200)
    action_input = input("Please Select An Option... ").strip().lower()
    if action_input == "" and auto_option:
        return action_input
    elif action_input in ["help", "h", "?"]:
        return "help"
    else:
        try:
            action_input = int(action_input)
        except Exception as e:
            print(f"Command not Recognized. Please Choose a Valid Option.")
            option_menu(options, auto_option)
        action_input -= 1
        return action_input

def inventory_menu() -> None:
    game_state["menu"] = "inventory"
    os.system("cls")
    hero.inventory.draw(hero)
    #Provide options for:
    #Move
    #drop
    #inspect
    #lootbag
    #character
    #exit(attack)
    options = ["Move", "Drop", "Inspect", "Lootbag", "Character", "Use"]
    auto_option = ["Attack"]
    action_input = option_menu(options, auto_option)
    if action_input == 0:
        move_menu()
    elif action_input == 1:
        drop_menu()
    elif action_input == 2:
        inspect_menu()
    elif action_input == 3:
        lootbag_menu()
    elif action_input == 4:
        character_menu()
    elif action_input == 5:
        use_menu()
    elif action_input == "":
        os.system("cls")
        return

def lootbag_menu() -> None:
    game_state["menu"] = "lootbag"
    os.system("cls")
    hero.loot_bag.draw_bag()
    #Provide options for:
    #Move
    #drop
    #inspect
    #inventory
    #character
    #exit(attack)
    options = ["Move", "Drop", "Inspect", "Inventory", "Character"]
    auto_option = ["Attack"]
    action_input = option_menu(options, auto_option)
    if action_input == 0:
        move_menu()
    elif action_input == 1:
        drop_menu()
    elif action_input == 2:
        inspect_menu()
    elif action_input == 3:
        inventory_menu()
    elif action_input == 4:
        character_menu()
    elif action_input == "":
        os.system("cls")
        return

def inspect_menu() -> None:
    #Options:
    #Enemy
    #Item in Inventory
    #Item in Lootbag
    #exit(attack)
    os.system("cls")
    options = ["Enemy", "Item in Inventory", "Item in Lootbag"]
    auto_option = ["Attack"]
    action_input = option_menu(options, auto_option)

    if action_input == 0:
        os.system("cls")
        game_state["menu"] = "inspect_enemy"
        hero.inspect(Enemy.active_enemy)
    elif action_input == 1:
        #Inspect item in inventory, list all items
        os.system("cls")
        options = hero.inventory.get_items()
        auto_option = ["Go Back"]
        action_input = option_menu(options, auto_option)
        if action_input == "":
            os.system("cls")
            return
        item_to_inspect = options[action_input]
        os.system("cls")
        hero.inspect(item_to_inspect)
    elif action_input == 2:
        #Inspect item in lootbag, list all items
        os.system("cls")
        options = hero.loot_bag.get_items()
        auto_option = ["Go Back"]
        action_input = option_menu(options, auto_option)
        if action_input == "":
            os.system("cls")
            return
        item_to_inspect = options[action_input]
        os.system("cls")
        hero.inspect(item_to_inspect)
    elif action_input == "":
        os.system("cls")
        return

def character_menu() -> None:
    #Options:
    #Inventory
    #Lootbag
    #Heal
    #Use
    #exit(attack)
    os.system("cls")
    game_state["menu"] = "character"
    health_bar_str = hero.health_bar.draw()
    mana_bar_str = hero.mana_bar.draw()
    xp_bar_str = hero.xp_bar.draw()
    print("╔" + "═" * 50 + "╗")
    print(f"║" + " " * 50 + "║")
    print(f"║ {"{}'s Stats".format(hero.name):^48} ║")
    print(f"║ {"Level - {}".format(hero.level):^48} ║")
    print(f"║" + " " * 50 + "║")
    print("╠" + "═" * 50 + "╣")
    print(f"║" + " " * 50 + "║")
    print(f"║   Health: {health_bar_str} {hero.health}/{hero.health_max:<8}║") 
    print(f"║   Mana:   {mana_bar_str} {hero.mana}/{hero.mana_max:<9}║")
    print(f"║" + " " * 50 + "║")
    print(f"║   XP:     {xp_bar_str} {hero.xp}/{(hero.level * 100):<7}║")
    print(f"║" + " " * 50 + "║")
    print("╠" + "═" * 50 + "╣")
    print(f"║   Attack Rating: {hero.attack_rating}   Defense: {hero.defense}   Gold: {hero.gold:<7}║")
    print("╠" + "═" * 50 + "╣")
    print(f"║{"{}'s Lootbag".format(hero.name):^50}║")
    print(f"║" + " " * 50 + "║")
    print(f"║   Damage: {hero.weapon.damage}   Hit Rating: {hero.weapon.hit_rating}   Capacity: {hero.loot_bag.weight}/{hero.loot_bag.weight_max:<5}║")
    print("╚" + "═" * 50 + "╝")
    if hero.stat_points > 0:
        options = ["Inventory", "Lootbag", "Heal", "Use", "Assign Stat Points"]
    else:
        options = ["Inventory", "Lootbag", "Heal", "Use"]
    auto_option = ["Attack"]
    action_input = option_menu(options, auto_option)
    if action_input == 0:
        inventory_menu()
    elif action_input == 1:
        lootbag_menu()
    elif action_input == 2:
        heal_menu()
    elif action_input == 3:
        use_menu()
    elif action_input == 4 and hero.stat_points > 0:
        level_up_menu(hero)
    elif action_input == "":
        os.system("cls")
    return

def level_up_menu(hero) -> None:
    os.system("cls")
    print(f"Which Stat Would You Like To Increase?")
    options = ["Health", "Defense", "Attack Rating", "Lootbag Capacity"]
    auto_option = ["Go Back"]
    action_input = option_menu(options, auto_option)
    if action_input == "":
        os.system("cls")
        return
    elif action_input == 0:
        hero.apply_stats("health")
    elif action_input == 1:
        hero.apply_stats("defense")
    elif action_input == 2:
        hero.apply_stats("attack_rating")
    elif action_input == 3:
        hero.apply_stats("lootbag_weight")
    return

def shop_menu() -> None:
    #Options:
    #Buy
    #Sell
    #Move
    #exit(attack)
    os.system("cls")
    game_state["menu"] = "shop"
    shop = Shop()
    shop.generate_shop()
    shop.draw()
    options = ["Buy", "Sell", "Move"]
    auto_option = ["Attack"]
    action_input = option_menu(options, auto_option)
    
    if action_input == 0:
        os.system("cls")
        shop.draw()
        print(f"________________________________")
        hero.inventory.draw(hero)
        options = []
        for item_name, item_obj in shop.stock.items():
            options.append(item_name)
        auto_option = ["Go Back"]
        action_input = option_menu(options, auto_option)
        if action_input == "":
            os.system("cls")
            return
        item_to_buy = options[action_input]
        os.system("cls")
        shop.buy(hero, item_to_buy)

    elif action_input == 1:
        os.system("cls")
        hero.inventory.draw(hero, shop_flag=True)
        options = hero.inventory.get_items()
        auto_option = ["Go Back"]
        action_input = option_menu(options, auto_option)
        if action_input == "":
            os.system("cls")
            return
        item_to_sell = options[action_input]
        os.system("cls")
        shop.sell(hero, item_to_sell)

    elif action_input == 2:
        move_menu()

    elif action_input == "":
        os.system("cls")
        return

def heal_menu() -> None:
    os.system("cls")
    hero.heal(10)
    hero.health_bar.draw()
    hero.mana_bar.draw()

def move_menu() -> None:
    #Options:
    #From Inventory -> Lootbag
    #From Lootbag -> Inventory
    #exit(attack)
    os.system("cls")
    options = ["Inventory -> Lootbag", "Lootbag -> Inventory"]
    auto_option = ["Attack"]
    action_input = option_menu(options, auto_option)
    os.system("cls")
    if action_input == 0:
        #move from inventory to lootbag
        options = hero.inventory.get_items()
        hero.inventory.draw(hero)
        if len(options) > 0:
            auto_option = ["Go Back"]
            action_input = option_menu(options, auto_option)
            os.system("cls")
            if action_input == "":
                return
            item_to_move = options[action_input]
            #BAD BAD BAD, FIX.
            if (hero.loot_bag.weight < hero.loot_bag.weight_max) and item_to_move not in ["Mana Potion", "Fortification Potion"] and hero.inventory.remove_item(item_to_move) :
                hero.loot_bag.add_item(item_to_move)
            elif hero.loot_bag.weight >= hero.loot_bag.weight_max:
                print(f"{item_to_move} won't fit in your lootbag.")
            elif item_to_move in ["Mana Potion", "Fortification Potion"]:
                print(f"{item_to_move} is not a weapon. ")
        else:
            print("Inventory Empty.")

    elif action_input == 1:
        #move from lootbag to inventory
        hero.loot_bag.draw_bag()
        options = hero.loot_bag.get_items()
        if len(options) > 0:
            auto_option = ["Go Back"]
            action_input = option_menu(options, auto_option)
            os.system("cls")
            if action_input == "":
                return
            item_to_move = options[action_input]
            if (hero.inventory.weight < hero.inventory.weight_max) and hero.loot_bag.remove_item(item_to_move):
                hero.inventory.add_item(item_to_move)
            elif hero.inventory.weight >= hero.inventory.weight_max:
                print(f"{item_to_move} won't fit in your inventory.")
        else:
            print("Lootbag Empty.")
    elif action_input == "":
        return
    
def drop_menu() -> None:
    os.system("cls")
    options = ["From Inventory", "From Lootbag"]
    auto_option = ["Attack"]
    action_input = option_menu(options, auto_option)

    if action_input == 0:
        os.system("cls")
        hero.inventory.draw(hero)
        options = hero.inventory.get_items()
        if len(options) > 0:
            auto_option = ["Go Back"]
            action_input = option_menu(options, auto_option)
            if action_input == "":
                os.system("cls")
                return
            item_to_drop = options[action_input]
            os.system("cls")
            hero.inventory.remove_item(item_to_drop)
            hero.inventory.draw(hero)
        else:
            print("Inventory Empty.")


    elif action_input == 1:
        os.system("cls")
        hero.loot_bag.draw_bag()
        options = hero.loot_bag.get_items()
        if len(options) > 0:
            auto_option = ["Go Back"]
            action_input = option_menu(options, auto_option)
            if action_input == "":
                os.system("cls")
                return
            item_to_drop = options[action_input]
            os.system("cls")
            hero.loot_bag.remove_item(item_to_drop)
            hero.loot_bag.draw_bag()
        else:
            os.system("cls")
            print("Lootbag Empty.")

    elif action_input == "":
        os.system("cls")
        return

def use_menu() -> None:
    #Options
    #Inventory Items
    os.system("cls")
    hero.inventory.draw(hero)
    options = hero.inventory.get_items()
    auto_option = ["Go Back"]
    action_input = option_menu(options, auto_option)
    if action_input == "":
        os.system("cls")
        return
    os.system("cls")
    item_to_use = options[action_input]
    hero.use(item_to_use)
    hero.inventory.draw(hero)
    options = ["Inventory", "Lootbag", "Heal", "Character"]
    auto_option = ["Go Back"]
    action_input = option_menu(options, auto_option)
    if action_input == "":
        os.system("cls")
        return
    if action_input == 0:
        inventory_menu()
    elif action_input == 1:
        lootbag_menu()
    elif action_input == 2:
        heal_menu()
    elif action_input == 3:
        character_menu()

def load_menu() -> None:
    global hero
    global options_list
    os.system("cls")

    save_files = list_saves()

    if not save_files:
        print("No saves found.")
        input("Press Enter to Return")
        return
    
    gold_column_width = max(4, max(len(str(get_save_preview(path)["gold"])) for path in save_files) + 1)
    
    print(f"{'    Name':<14} | {'Level':<8} | {'Gold':<{gold_column_width}} | {'Modified':<20}")

    options = []
    for path in save_files:
        info = get_save_preview(path)
        time_raw = info["modified"].strftime("%a %m/%d %I:%M %p") if isinstance(info["modified"], datetime) else "N/A"
        modified_str = time_raw.replace(" 0", " ")

        display_str = (
            f"{info['name']:<10} | "
            f"Level {str(info['level']):<2} | "
            f"{str(info['gold']) + "g":<{gold_column_width}} | "
            f"{modified_str}")
        
        options.append(display_str)
    auto_option = ["Go Back"]
    action_input = option_menu(options, auto_option)
    
    if action_input == "":
        os.system("cls")
        return
    
    selected_path = save_files[action_input]
    filename = selected_path.name

    hero_save, enemy_save, game_state, shop_save = load_game(filename)
    if hero_save is None:
        input("Failed to load save, press Enter to return...")
        return

    hero = None
    Enemy.active_enemy = None
    hero = Hero.from_dict(hero_save)
    Enemy.active_enemy = Enemy.from_dict(enemy_save)
    #run function to change to correct game state, refactor all actions to take place in functions
    #load_game_state(game_state)
    options_list = game_state["options_list"]

    os.system("cls")

    print(f"Game loaded: {hero.name} (Level {hero.level}, {hero.gold}g)")
    input("Press Enter to continue...")
    
    return

def save_menu() -> None:
    os.system("cls")
    hero_save = hero.to_dict()
    enemy_save = Enemy.active_enemy.to_dict()
    save_game(hero=hero_save, enemy=enemy_save, game_state=game_state)

def game_menu() -> None:
    #Options:
    #Settings
    #Save
    #Load
    #Help
    #Quit
    os.system("cls")
    options = ["Settings", "Save", "Load", "Help", "Quit"]
    auto_option = ["Go Back"]
    action_input = option_menu(options, auto_option)
    if action_input == "":
        os.system("cls")
        return
    elif action_input == 0:
        game_settings_menu()
    elif action_input == 1:
        save_menu()
    elif action_input == 2:
        load_menu()
    elif action_input == 3:
        help_menu()
    elif action_input == 4:
        os.system("cls")
        print("Are you sure? Don't forget to save!")
        options = ["Yes, Quit", "Don't Quit"]
        auto_option = ["Go Back"]
        action_input = option_menu(options, auto_option)
        if action_input == "":
            os.system("cls")
            return
        elif action_input == 0:
            exit()
        elif action_input == 1:
            os.system("cls")
            return
        
def game_settings_menu() -> None:
    global options_list
    if options_list is None:
        options_list = [True, True]
    os.system("cls")
    print("Settings:")
    #Options:
    #AutoEncounter
    #AutoPickup
    options = ["AutoEncounter", "AutoPickup"]
    auto_option = ["Go Back"]
    action_input = option_menu(options, auto_option)
    if action_input == "":
        os.system("cls")
        return
    elif action_input == 0:
        os.system("cls")
        print("AutoPickup Settings:")
        options = ["AutoEncounter On: The next enemy is automatically generated by pressing <ENTER> after an enemy is killed.",
                    "AutoEncounter Off: The next enemy must be manually encountered after an enemy is killed."]
        auto_option = ["Go Back"]
        action_input = option_menu(options, auto_option)
        if action_input == "":
            game_settings_menu()
        auto_encounter = True if action_input == 0 else False
        print(f"AutoEncounter: {auto_encounter}")
        options_list[0] = auto_encounter
        game_settings_menu()
    elif action_input == 1:
        os.system("cls")
        print("AutoPickup Settings:")
        options = ["AutoPickup On: Items will automatically be picked up by pressing <ENTER> after an enemy is killed.",
                    "AutoPickup Off: Items must be manually picked up after an enemy is killed."]
        auto_option = ["Go Back"]
        action_input = option_menu(options, auto_option)
        if action_input == "":
            game_settings_menu()
        auto_pickup = True if action_input == 0 else False
        print(f"AutoPickup: {auto_pickup}")
        options_list[1] = auto_pickup
        game_settings_menu()

def help_menu() -> None:
    os.system("cls")
    options = ["General", "Attack", "Saving/Loading", "Inventory", "Lootbag", "Stats", "Inspect", "Shop", "Use", "Heal", "Move", "Drop"]
    auto_option = ["Go Back"]
    action_input = option_menu(options=options, auto_option=auto_option)
    os.system("cls")

    if action_input == 0:
        help_general()
    elif action_input == 1:
        help_attack()
    elif action_input == 2:
        help_save_load()
    elif action_input == 3:
        help_inventory()
    elif action_input == 4:
        help_lootbag()
    elif action_input == 5:
        help_stats()
    elif action_input == 6:
        help_inspect()
    elif action_input == 7:
        help_shop()
    elif action_input == 8:
        help_use()
    elif action_input == 9:
        help_heal()
    elif action_input == 10:
        help_move()
    elif action_input == 11:
        help_drop()
    elif action_input == "":
        return
    help_menu()

def pickup_menu(drops) -> None:
    global options_list
    if options_list[1] == False:
        options = [f"Pick up {drops[2]}"]
        auto_option = ["Go Back"]
        action_input = option_menu(options, auto_option)
    else:
        action_input = 0
    if action_input == 0:
        hero.pick_up(drops)
        drops = None

def add_menu() -> None:
    #Options:
    #Gold
    #XP
    #Item
    #exit(attack)
    os.system("cls")
    options = ["Gold", "XP", "Item"]
    auto_option = ["Go Back"]
    action_input = option_menu(options, auto_option)

    if action_input == "":
        return
    if action_input == 0:
        hero.gold += 10
        print("Added 10 gold.")
    elif action_input == 1:
        hero.gain_xp(drops=None,xp=50)
    elif action_input == 2:
        options = ["Mana Potion", "Wooden Stick", "Iron Dagger", "Fortification Potion"]
        action_input = option_menu(options, auto_option)
        item_to_add = options[action_input]
        if action_input == "":
            return
        if action_input == 0:
            hero.inventory.add_item(item_to_add)
        elif action_input == 1:
            weapon_to_add = Weapon.generate_weapon("Wooden Stick")
            hero.inventory.add_item(weapon_to_add.name)
        elif action_input == 2:
            weapon_to_add = Weapon.generate_weapon("Iron Dagger")
            hero.inventory.add_item(weapon_to_add.name)
        elif action_input == 3:
            hero.inventory.add_item(item_to_add)
        hero.inventory.draw(hero)
    add_menu()
    
def encounter_menu() -> None:
    #if autoencounter off, present options here
    global options_list
    if options_list[0] == False:
        options = ["Encounter Enemy"]
        auto_option = ["Go Back"]
        action_input = option_menu(options, auto_option)
    else:
        action_input = ""
    #Set up autocall if autoencounter on
    if action_input == 0 or options_list[0] == True:
        Enemy.active_enemy = Enemy.spawn_enemy(hero)
    #remove if drops should be permanent (also refactor attack function returns)
    drops = None

def attack_menu() -> None:
    game_state["menu"] = "enemy"
    if Enemy.active_enemy is None:
        encounter_menu()
    else:
        drops = hero.attack(Enemy.active_enemy)
        if drops is not None:
            hero.gain_xp(drops)
            hero.gain_gold(drops)
            if len(drops) > 2:
                pickup_menu(drops)
            drops = None

        if Enemy.active_enemy is not None and Enemy.active_enemy.health > 0 :
            Enemy.active_enemy.attack(hero)

        if Enemy.active_enemy is not None:

            line = format_stat_line("Health:", Enemy.active_enemy.health_bar.draw(), f"{Enemy.active_enemy.health}/{Enemy.active_enemy.health_max}")
            draw_boxed_ui([line], title=Enemy.active_enemy.name)

            """
            enemy_health_label = "Health: "
            enemy_health_bar_str = Enemy.active_enemy.health_bar.draw()
            enemy_health_value = f"{Enemy.active_enemy.health}/{Enemy.active_enemy.health_max}"

            enemy_line_text = strip_ansi(f"   {enemy_health_label} {enemy_health_bar_str} {enemy_health_value}")

            print("╔" + "═" * 50 + "╗")
            print(f"║ {"{}".format(Enemy.active_enemy.name):^48} ║")
            print(f"║{enemy_line_text:<50}║")
            print("╚" + "═" * 50 + "╝")
            """

        health_line = format_stat_line("Health:", hero.health_bar.draw(), f"{hero.health}/{hero.health_max}")
        mana_line = format_stat_line("Mana:  ", hero.mana_bar.draw(), f"{hero.mana}/{hero.mana_max}")
        xp_line = format_stat_line("XP:    ", hero.xp_bar.draw(), f"{hero.xp}/{hero.level * 100}")

        draw_boxed_ui([health_line, mana_line, " " * UI_WIDTH, xp_line])
        """
        hero_health_label = "Health: "
        hero_health_bar_str = hero.health_bar.draw()
        hero_health_value = f"{hero.health}/{hero.health_max}"

        hero_health_line_text = strip_ansi(f"   {hero_health_label} {hero_health_bar_str} {hero_health_value}")

        hero_mana_label = "Mana:   "
        hero_mana_bar_str = hero.mana_bar.draw()
        hero_mana_value = f"{hero.mana}/{hero.mana_max}"

        hero_mana_line_text = strip_ansi(f"   {hero_mana_label} {hero_mana_bar_str} {hero_mana_value}")

        hero_xp_label = "XP:     "
        hero_xp_bar_str = hero.xp_bar.draw()
        hero_xp_value = f"{hero.xp}/{hero.level * 100}"

        hero_xp_line_text = strip_ansi(f"   {hero_xp_label} {hero_xp_bar_str} {hero_xp_value}")

        
        print("╔" + "═" * 50 + "╗")
        print(f"║{hero_health_line_text:<50}║") 
        print(f"║{hero_mana_line_text:<50}║")
        print(f"║" + " " * 50 + "║")
        print(f"║{hero_xp_line_text:<50}║")
        print("╚" + "═" * 50 + "╝")
        """

        

        if Enemy.active_enemy is None:
            encounter_menu()

#Startup, Main Menu
#Settings
hero = None
options_list = None
main_menu()
os.system("cls")
if hero == None:
    print(f"Welcome To Lootbag RPG!")
    print(f"____________________________")
    username = input("Please enter your username: ")
    os.system("cls")
    print(f"Welcome To Lootbag RPG!")
    print(f"____________________________")
    print(f"The Game About Hitting Things With Your Lootbag.")
    print(f"This is a text-adventure, turn-based ARPG.")
    print(f"Type 'help' for help.")
    print(f"If you encounter issues or a crash, feel free to file an issue on the public github.")
    input("Press Enter To Begin...")
    os.system("cls")
    #define player and enemy objects
    loot_bag = LootBag()
    shop = Shop()
    hero = Hero(name=username, 
                level=1, 
                xp=0, 
                health=100, 
                mana=10, 
                attack_rating=50, 
                defense=10, 
                loot_bag=loot_bag, 
                inventory=Inventory())
    Enemy.active_enemy = Enemy.spawn_enemy(hero, enemy_name="Goblin Grunt")
else:
    print(f"Welcome Back To Lootbag RPG, {hero.name}!")
    print(f"____________________________")

game_state = {
    "options_list": options_list,
    "menu": "enemy"
}

#Game loop
while True:

    #Modify options menu to include [!] action reminders
    if hero.stat_points > 0:
        options = ["Inventory", "Lootbag", "Inspect", "Character [!]", "Shop", "Heal", "Menu"]
    else:
        options = ["Inventory", "Lootbag", "Inspect", "Character", "Shop", "Heal", "Menu"]
    auto_option = ["Attack"]
    action_input = option_menu(options=options, auto_option=auto_option)
    os.system("cls")

    #Input choice parsing
    #"Help" and other special keywords check here
    if action_input == "help":
        help_menu()
        continue

    #Prototype execution test
    if action_input == 0:
        #Inventory menu
        inventory_menu()
    elif action_input == 1:
        #lootbag menu
        lootbag_menu()
    elif action_input == 2:
        #Inspect menu
        inspect_menu()
    elif action_input == 3:
        #Character menu
        character_menu()
    elif action_input == 4:
        #Shop menu
        shop_menu()
    elif action_input == 5:
        #Heal character
        heal_menu()
    elif action_input == 6:
        #Game menu (settings, save, load)
        game_menu()
    elif action_input == "":
        #Attack
        attack_menu()
    elif action_input == -1:
        add_menu()

    
        
#Shop Save debug
"""
if argument in ["debug"]:
                shop_dict_before = shop.to_dict()
                shop = None
                shop = Shop.from_dict(shop_dict_before)
                shop_dict_after = shop.to_dict()
                print("BEFORE")
                for item in shop_dict_before:
                    print(f"{item}: {shop_dict_before.get(item)}")
                print("----------------")
                print("AFTER")
                for item in shop_dict_after:
                    print(f"{item}: {shop_dict_after.get(item)}")
                if shop_dict_before == shop_dict_after:
                        print("YES")
                print(shop_dict_after)
"""

#General Save Debug
"""
elif action in ["debug"]:
        enemydictbefore = Enemy.active_enemy.to_dict()
        Enemy.active_enemy = None
        Enemy.active_enemy = Enemy.from_dict(enemydictbefore)
        enemydictafter = Enemy.active_enemy.to_dict()
        print("BEFORE")
        for item in enemydictbefore:
            print(f"{item}: {enemydictbefore.get(item)}")
        print("----------------")
        print("AFTER")
        for item in enemydictafter:
            print(f"{item}: {enemydictafter.get(item)}")
        if enemydictbefore == enemydictafter:
            print("YES")
"""

#Deprecated Input parsing
"""
    if action_input == "":
        action = ""
        argument = None
    else:
        action_parts = action_input.split(maxsplit=1)
        action = action_parts[0]
        argument = action_parts[1] if len(action_parts) > 1 else None
"""