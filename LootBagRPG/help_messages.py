def help_template() -> None:
    #Template function to display help messages
    print(f"")

def help_general() -> None:
    #General help message
    print("Welcome to LootbagRPG!")
    print("This is a Diablo-inspired text based RPG")
    print("Your only weapon is your lootbag. Kill monsters, put their loot in your bag, kill more monsters.")
    print("Type a number from options lists and press Enter to select it")
    input("Press Enter to Go Back")

def help_move() -> None:
    #Help messages for the "move" command
    print(f"Moving an Item")
    print(f"_________________________")
    print(f"Selecting 'Move' will allow you to transfer items between your lootbag and inventory")
    print(f"Choose which direction to move items, then choose the item to move")
    input("Press Enter to Go Back")

def help_shop() -> None:
    #Help messages for the "shop" menu
    print(f"The Shop")
    print(f"_________________________")
    print(f"The shop allows you to purchase potions and random weapons")
    print(f"Items can be sold for equal value to the shop")
    print(f"Once an item is sold to the shop it is permanently gone")
    print(f"Every time the shop is opened, the stocked weapon is randomly chosen")
    print(f"Items bought in the shop are moved into your inventory")
    print(f"Items sold to the shop must come from your inventory")
    input("Press Enter to Go Back")

def help_drop() -> None:
    #Help messages for the "drop" command
    print(f"Dropping an item")
    print(f"_________________________")
    print(f"Items can be dropped from the inventory or lootbag")
    print(f"Once an item is selected, it will be permanently removed.")
    input("Press Enter to Go Back")

def help_attack() -> None:
    #Help messages for the "attack" command
    print(f"Attacking an Enemy")
    print(f"_________________________")
    print(f"Pressing <ENTER> will cause you to autoattack.")
    print(f"Holding <ENTER> will cause you to autoattack rapidly, watch your HP carefully!")
    print(f"The enemy will respond after your attack if able")
    print(f"When attacking, the chance to hit is determined by the average of your attack rating and your lootbag hit rating.")
    print(f"The lootbag hit rating is an average of all weapon hit ratings in the lootbag")
    print(f"This chance is then reduced by the enemy defense")
    print(f"%Hit chance = (attackrating + lootbaghitrating)/2 - enemydefense")
    print(f"Example: If your attack rating is 80 and your lootbag hit rating is 60, your hit chance will be 70%")
    print(f"    If the enemy defense is 10, the actual hit chance is 60%")
    input("Press Enter to Go Back")

def help_save_load() -> None:
    #Help messages for the "save/load" commands
    print(f"Saving and Loading")
    print(f"_________________________")
    print(f"When saving, the file will be saved in the same directory as the game files, under 'saves'")
    print(f"The save file is [hero_name].json")
    print(f"When loading a save file, ensure you enter the entire filename")
    print(f"Example: 'heroname.json'")
    input("Press Enter to Go Back")

def help_inventory() -> None:
    #Help messages for the "inventory" command
    print(f"Using your Inventory")
    print(f"_________________________")
    print(f"The inventory is a typical RPG inventory, it can hold any item")
    print(f"All items sold to or bought from the shop go through the inventory")
    print(f"Items may only be used from the inventory")
    print(f"Weapons in the inventory do not contribute to your attack power")
    print(f"Weapons may be moved between the inventory and lootbag using the 'move' menu")
    input("Press Enter to Go Back")

def help_lootbag() -> None:
    #Help messages for the "lootbag" command
    print(f"The Lootbag")
    print(f"_________________________")
    print(f"The lootbag is your primary weapon. It is your Implement.")
    print(f"All weapons in the lootbag add their damage together")
    print(f"All weapons in the lootbag average their hit rating together")
    print(f"Only weapons can be stored in the lootbag")
    input("Press Enter to Go Back")

def help_stats() -> None:
    #Help messages for the "stats" command
    print(f"The Stats Screen")
    print(f"_________________________")
    print(f"The stats screen will show your current health and mana,")
    print(f"Your level and XP,")
    print(f"Your max health and mana,")
    print(f"Your attack rating and defense,")
    print(f"Your current gold,")
    print(f"And a summary of your lootbag, its damage, hit rating, and capacity.")
    print(f"%Hit chance = (attackrating + lootbaghitrating)/2 - enemydefense")
    input("Press Enter to Go Back")

def help_inspect() -> None:
    #Help messages for the "inspect" command
    print(f"Inspecting Enemies/Items")
    print(f"_________________________")
    print(f"Choose 'enemy' to inspect the current enemy, and see their stats")
    print(f"Choose 'item in inventory/lootbag' to inspect an item in your inventory or lootbag, and see its stats")
    input("Press Enter to Go Back")

def help_use() -> None:
    #Help messages for the "use" command
    print(f"Using Items")
    print(f"_________________________")
    print(f"items can only be used from your inventory")
    print(f"Currently, only potions can be used.")
    print(f"The mana potion, for example, replenishes 5 mana")
    input("Press Enter to Go Back")

def help_heal() -> None:
    #Help messages for the "heal" command
    print(f"Healing Mechanics")
    print(f"_________________________")
    print(f"Choose 'heal' to heal your character.")
    print(f"Healing costs 1 mana and replenishes 10 hp.")
    input("Press Enter to Go Back")