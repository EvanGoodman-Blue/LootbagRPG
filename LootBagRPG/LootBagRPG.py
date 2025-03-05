#LootBagRPG
#Text-Based MVP
from character import Hero, Enemy
from loot_bag import LootBag
from inventory import Inventory
import os
from items import Weapon
from shop import Shop
from saveload import *


#Startup, player input
username = input("Please enter your username: ")
#Settings
settings_flag = input("Settings? (y/n)")
auto_pickup = False
if settings_flag in ["y", "yes"]:
    print("Settings:")
    auto_pickup = True if input("Auto Pickup? (y/n)") in ["y", "yes"] else False
    print(f"AutoPickup: {auto_pickup}")

#define player and enemy objects
loot_bag = LootBag()
shop = Shop()
hero = Hero(name=username, level=1, xp=0, health=100, mana=10, attack_rating=50, defense=10, loot_bag=loot_bag, inventory=Inventory())
#hero.inventory.add_item("Mana Potion")
#hero.inventory.add_item(Weapon.generate_weapon("Wooden Stick").name)
#hero.loot_bag.add_item(Weapon.generate_weapon("Iron Dagger").name)
#herodictbefore = hero.to_dict()
#hero = None
#hero = Hero.from_dict(herodictbefore)
Enemy.active_enemy = Enemy.spawn_enemy(hero, enemy_name="Goblin")



game_state = {
    "Autopickup": auto_pickup,
    "menu": "enemy"
}

#Possible menu states:
#game_state["menu"] = "enemy"
#game_state["menu"] = "inspect_enemy"
#game_state["menu"] = "character"
#game_state["menu"] = "inventory"
#game_state["menu"] = "lootbag"
#game_state["menu"] = "shop"

#Game loop
while True:
    action_input = input("Action? ").strip().lower()
    os.system("cls")

    #Input parsing
    if action_input == "":
        action = ""
        argument = None
    else:
        action_parts = action_input.split(maxsplit=1)
        action = action_parts[0]
        argument = action_parts[1] if len(action_parts) > 1 else None

    if action in ["debug"]:
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

    elif action in ["help", "tutorial", "action", "?"]:
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
        print("Type 'help' to open this menu again")
    
    elif action in ["attack", "atk", "a", ""] and Enemy.active_enemy is not None:

        drops = hero.attack(Enemy.active_enemy)
        if drops is not None:
            hero.gain_xp(drops)
            hero.gain_gold(drops)

        if Enemy.active_enemy is not None and Enemy.active_enemy.health > 0 :
            Enemy.active_enemy.attack(hero)

        hero.health_bar.draw()
        hero.mana_bar.draw()
        if Enemy.active_enemy is not None:
            Enemy.active_enemy.health_bar.draw()

    elif (action in ["pickup"] and drops is not None and len(drops) > 2) or (action in [""] and drops is not None and len(drops) > 2 and auto_pickup == True):
        hero.pick_up(drops)
        drops = None

    elif action in ["inspect", "ins", "enemy"]:
        game_state["menu"] = "inspect_enemy"
        hero.inspect(Enemy.active_enemy)

    elif action in ["c", "stats", "char", "character"]:
        game_state["menu"] = "character"
        hero.health_bar.draw()
        hero.mana_bar.draw()
        hero.draw_stats()

    elif (action in ["new", "n", "next"] and Enemy.active_enemy is None) or (Enemy.active_enemy is None and action in [""]):
        Enemy.active_enemy = Enemy.spawn_enemy(hero)
        #remove if drops should be permanent (also refactor attack function returns)
        drops = None

    elif action in ["new", "n", "next"] and Enemy.active_enemy is not None:
        print("Already fighting an enemy!")

    elif action in ["b", "bag"]:
        game_state["menu"] = "lootbag"
        hero.loot_bag.draw_bag()

    elif action in ["e", "i", "inventory", "inv"]:
        game_state["menu"] = "inventory"
        hero.inventory.draw(hero)

    elif action in ["m", "move"]:
        if argument is None:
            item_to_move = input("Which Item? ").strip().lower()
        else:
            item_to_move = argument
        destination = input("To Where? ").strip().lower()
        if destination in ["bag", "b", "lootbag"]:
            #move from inventory to lootbag
            if (hero.loot_bag.weight < hero.loot_bag.weight_max) and hero.inventory.remove_item(item_to_move):
                hero.loot_bag.add_item(item_to_move)
            elif hero.loot_bag.weight >= hero.loot_bag.weight_max:
                print(f"{item_to_move} won't fit in your lootbag.")

        elif destination in ["e", "i", "inventory", "inv"]:
            #move from lootbag to inventory
            if (hero.inventory.weight < hero.inventory.weight_max) and hero.loot_bag.remove_item(item_to_move):
                hero.inventory.add_item(item_to_move)
            elif hero.inventory.weight >= hero.inventory.weight_max:
                print(f"{item_to_move} won't fit in your inventory.")
        else:
            print("Invalid Destination")

    elif action in ["shop", "s"]:
        game_state["menu"] = "shop"
        shop.generate_shop()
        shop.draw()
        if argument is None or argument in ["debug"]:
            buy_sell = input(f"Buying or Selling, {hero.name}? ").strip().lower()
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
        else:
            buy_sell = argument
        if buy_sell in ["b", "buy", "buying", "purchase"]:
            hero.inventory.draw(hero)
            item_to_buy = input(f"Whaddaya Buyin, {hero.name}? ").strip().lower()
            shop.buy(hero, item_to_buy)

        elif buy_sell in ["s", "sell", "selling"]:
            hero.inventory.draw(hero)
            item_to_sell = input(f"Whatcha got for me, {hero.name}? ").strip().lower()
            shop.sell(hero, item_to_sell)

        else:
            print("Command not Recognized.")


    elif action in ["add"]:
        if argument in ["g", "gold"]:
            hero.gold += 10
            print("Added 10 gold.")
        elif argument in ["xp"]:
            hero.gain_xp(drops=None,xp=50)
        elif argument is None:
            weapon_name = input("Which Weapon? ").strip().lower()
        else:
            weapon_name = argument
            hero.loot_bag.add_item(weapon_name)
            hero.loot_bag.draw_bag()

    elif action in ["drop", "d"]:
        if argument is None:
            item_name = input("Which Weapon? ").strip().lower()
        else:
            item_name = argument
            source = input("From Where? ").strip().lower()
            if source in ["b", "bag", "lootbag"]:
                hero.loot_bag.remove_item(item_name)
                hero.loot_bag.draw_bag()
            elif source in ["e", "i", "inv", "inventory"]:
                hero.inventory.remove_item(item_name)
                hero.inventory.draw()

    elif action in ["heal", "h", "restore"]:
        hero.heal(10)
        hero.health_bar.draw()
        hero.mana_bar.draw()

    elif action in ["use", "u"]:
        
        if argument is None:
            item_to_use = input(f"What would you like to use, {hero.name}? ").strip().lower()
        else:
            item_to_use = argument
            hero.use(item_to_use)
            hero.inventory.draw(hero)

    else:
        print("Action Not Recognized")

    #if enemy.health == 0:
        #enemy = enemy.die()


    #if hero.health == 0:
        #hero.die()
        

#
