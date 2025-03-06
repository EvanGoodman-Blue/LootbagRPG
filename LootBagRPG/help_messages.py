def help_template() -> None:
    #Template function to display help messages
    print(f"")

def help_move() -> None:
    #Help messages for the "move" command
    print(f"Moving an Item")
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
    print(f"Typing 'drop' or 'd' followed by the item's name will prompt a request for the location of the item.")
    print(f"Once provided (inventory or lootbag), the first instance of the item found will be permanently removed.")
    print(f"Example: 'drop wooden stick' <ENTER> 'lootbag' <ENTER> will drop a wooden stick from your lootbag")