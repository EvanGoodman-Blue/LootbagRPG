def help_template() -> None:
    #Template function to display help messages
    print(f"")

def help_general() -> None:
    #General help message
    print("Welcome to LootbagRPG!")
    print("Press Enter to Autoattack")
    print("Type 'e' or 'i' to open inventory")
    print("Type 'b' or 'bag' to open lootbag")
    print("Type 'c' or 'stats' to examine your stats")
    print("Type 'inspect' to inspect the current enemy")
    print("Type 's' to open the shop")
    print("Type 'use' to use an item in your inventory")
    print("Type 'h' or 'heal' to heal your character")
    print("Type 'move' to move an item between your inventory and lootbag")
    print("Type 'pickup' when an enemy is killed to pick up dropped items, or let autopickup handle it automatically")
    print("Type 'drop' to drop an item from your inventory or lootbag")
    print("Type 'save' to save the game")
    print("Type 'load [filename]' to load a saved game")
    print("Type 'help [action]' at any time to show datailed help")

def help_move() -> None:
    #Help messages for the "move" command
    print(f"Moving an Item")
    print(f"_________________________")
    print(f"Type 'move' or 'm' to move an item, followed by the name of the item you wish to move")
    print(f"Example: 'move wooden stick of pain'")
    print(f"When moving an item, the game will ask where the item should be moved to,")
    print(f"The inventory, or the lootbag.")
    print(f"Select an option by typing 'inventory' or 'lootbag', ")
    print(f"The first item which matches the name given will be moved from the chosen place to the other.")
    print(f"Example: 'move wooden stick' <ENTER> 'inventory' <ENTER> ")
    print(f"The item will be moved from your lootbag to your inventory, if there is space.")

def help_shop() -> None:
    #Help messages for the "shop" menu
    print(f"The Shop")
    print(f"_________________________")
    print(f"Typing 's' or 'shop' will bring you to the shop, ")
    print(f"Optionally you can add an 's' or 'b' to this command to bring you straight to the selling or buying menu.")
    print(f"Example: 'shop s' will bring you straight to the selling menu, as will 's s'")
    print(f"Once in the shop menu to buy or sell, type the name of the item you wish to buy or sell")
    print(f"Items bought in the shop are moved into your inventory")
    print(f"Items sold to the shop must come from your inventory")
    print(f"Example: 's b' <ENTER> 'mana potion' <ENTER> will purchase a mana potion and add it to your inventory.")

def help_drop() -> None:
    #Help messages for the "drop" command
    print(f"Dropping an item")
    print(f"_________________________")
    print(f"Typing 'drop' or 'd' followed by the item's name will prompt a request for the location of the item.")
    print(f"Once provided (inventory or lootbag), the first instance of the item found will be permanently removed.")
    print(f"Example: 'drop wooden stick' <ENTER> 'lootbag' <ENTER> will drop a wooden stick from your lootbag")

def help_attack() -> None:
    #Help messages for the "attack" command
    print(f"Attacking an Enemy")
    print(f"_________________________")
    print(f"Typing 'attack' or 'a' will attack the current enemy")
    print(f"However, it is easier to simply press and even hold <ENTER>, and you will autoattack.")
    print(f"The enemy will respond after your attack if able")
    print(f"When attacking, the chance to hit is determined by the average of your attack rating and your lootbag hit rating.")
    print(f"The lootbag hit rating is an average of all weapon hit ratings in the lootbag")
    print(f"This chance is then reduced by the enemy defense")
    print(f"%Hit chance = (attackrating + lootbaghitrating)/2 - enemydefense")
    print(f"Example: If your attack rating is 80 and your lootbag hit rating is 60, your hit chance will be 70%")
    print(f"    If the enemy defense is 10, the actual hit chance is 60%")

def help_save_load() -> None:
    #Help messages for the "save/load" commands
    print(f"Saving and Loading")
    print(f"_________________________")
    print(f"Typing 'save' will save a [name].JSON file containing the current game state, named after your username.")
    print(f"Typing 'load filename.json' will load the corresponding save file.")

def help_inventory() -> None:
    #Help messages for the "inventory" command
    print(f"Using your Inventory")
    print(f"_________________________")
    print(f"Typing 'e' or 'i' or 'inventory' will open your inventory")
    print(f"The inventory is a typical RPG inventory, it can hold items other than weapons such as mana potions")
    print(f"All items sold to or bought from the shop go through the inventory")
    print(f"Items may only be used from the inventory")
    print(f"Weapons in the inventory do not contribute to your attack power")
    print(f"Weapons may be moved between the inventory and lootbag using the 'move' command")

def help_lootbag() -> None:
    #Help messages for the "lootbag" command
    print(f"The Lootbag")
    print(f"_________________________")
    print(f"The lootbag is your primary weapon. It is your Implement.")
    print(f"All weapons in the lootbag add their damage together")
    print(f"All weapons in the lootbag average their hit rating together")
    print(f"Only weapons can be stored in the lootbag")

def help_stats() -> None:
    #Help messages for the "stats" command
    print(f"The Stats Screen")
    print(f"_________________________")
    print(f"Typing 'c' or 'stats' will open the character stats screen")
    print(f"The stats screen will show your current health and mana,")
    print(f"Your level and XP,")
    print(f"Your max health and mana,")
    print(f"Your attack rating and defense,")
    print(f"Your current gold,")
    print(f"And a summary of your lootbag, its damage, hit rating, and capacity.")
    print(f"%Hit chance = (attackrating + lootbaghitrating)/2 - enemydefense")

def help_inspect() -> None:
    #Help messages for the "inspect" command
    print(f"Inspecting Enemies/Items")
    print(f"_________________________")
    print(f"Type 'inspect enemy' to inspect the current enemy, and see their stats")
    print(f"Type 'inspect [item]' to inspect an item in your inventory or lootbag, and see its stats")

def help_use() -> None:
    #Help messages for the "use" command
    print(f"Using Items")
    print(f"_________________________")
    print(f"Type 'use [item]' to use an item from your inventory")
    print(f"Currently, only potions can be used.")
    print(f"The mana potion, for example, replenishes 5 mana")

def help_heal() -> None:
    #Help messages for the "heal" command
    print(f"Healing Mechanics")
    print(f"_________________________")
    print(f"Type 'h' or 'heal' to heal your character.")
    print(f"Healing costs 1 mana and replenishes 10 hp.")