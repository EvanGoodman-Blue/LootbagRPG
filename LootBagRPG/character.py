from items import Item, Weapon, Potion
from loot_bag import LootBag
from inventory import Inventory
from health_bar import HealthBar, ManaBar, XPBar
from random import randint, choice, uniform
import os
#from shop import Shop

class Character:   
    def __init__(self, name: str, health: int, mana: int, attack_rating: int, defense: int, level: int = None, xp: int = None) -> None:
        self.name = name
        self.level = level
        self._health = health
        self.health_max = health
        self._mana = mana
        self.mana_max = mana
        self._xp = xp
        self.attack_rating = attack_rating
        self.defense = defense
        self.health_bar = HealthBar(self)
        self.mana_bar = ManaBar(self)
        if xp is not None:
            self.xp_bar = XPBar(self)

        #self.weapon = Weapon.get_weapon_by_name("Fists")

    @property
    def health(self):
        return self._health
    
    @health.setter
    def health(self, value: int):
        self._health = value
        self.health_bar.update()

    @property
    def mana(self):
        return self._mana
    
    @mana.setter
    def mana(self, value: int):
        self._mana = value
        self.mana_bar.update()

    @property
    def xp(self):
        return self._xp
    
    @xp.setter
    def xp(self, value: int):
        self._xp = value
        self.xp_bar.update()

    def attack(self, target) -> list:
        #hit rating check
        #higher character attack rating and weapon hit rating = higher chance of success
        #higher target defense = lower chance of success
        #character attack rating and weapon hit rating average
        attack_chance = (self.attack_rating + self.weapon.hit_rating) // 2
        #possibly add more mechanisms for block, spells, armor effects etc
        block_chance = target.defense
        #possibly implement diminishing returns on very high attack and block chances
        hit_chance = attack_chance - block_chance

        if randint(1, 100) <= hit_chance:
            target.health -= self.weapon.damage
            target.health = max(target.health, 0)
            #target.health_bar.update()
            print(f"Hit! {self.name} dealt {self.weapon.damage} damage to {target.name} with {self.weapon.name}")
        else:
            print(f"{self.name} Missed!")

        if target.health == 0:
            target.die()

            #xp and loot drop function calls
            drops = target.generate_drops()
            if len(drops) > 2:
                item = Weapon.get_weapon_by_name(drops[2])

                print(f"{target.name} Dropped {item.rarity} {item.name}")

            if isinstance(target, Enemy):
                target.death_cleanup()

            return drops
        else:
            return None

    def die(self) -> None:
        print (f"{self.name} has died!")


class Hero(Character):
    def __init__(self, 
                 name: str,
                 level: int,
                 xp: int, 
                 health: int,
                 mana: int,
                 attack_rating: int,
                 defense: int,
                 loot_bag: object,
                 inventory: object,
                 gold: int=0,
                 stat_points: int=0
                 ) -> None:
        super().__init__(name=name, level=level, health=health, mana=mana, xp=xp, attack_rating=attack_rating, defense=defense)

        self.gold = gold
        self.loot_bag = loot_bag
        self.inventory = inventory
        self.weapon = self.loot_bag
        self.health_bar = HealthBar(self, color= "red")
        self.mana_bar = ManaBar(self, color= "blue")
        self.xp_bar = XPBar(self)
        self.stat_points = stat_points

    def level_up(self) -> None:
        self.level += 1
        self.stat_points += 5
        #implement level bonuses (max health, defense, attack rating, lootbag weight)
        print(f"{self.name} Advanced to Level {self.level}!")
        print(f"Open the Character Screen to Assign Stat Points.")

    def apply_stats(self, stat:str) -> None:
        #stat- stat to increase (max health, defense, attack rating, lootbag weight)
        os.system("cls")
        if stat in ["health"]:
            self.health_max += 5
            self.health += 5
            self.health_bar.update()
            print(f"{self.name}'s Max Health increased by 5!")
            self.health_bar.draw()
            self.mana_bar.draw()
        elif stat in ["defense"]:
            self.defense += 5
            print(f"{self.name}'s Defense increased by 5!")
        elif stat in ["attack_rating"]:
            self.attack_rating += 5
            print(f"{self.name}'s Attack Rating increased by 5!")
        elif stat in ["lootbag_weight"]:
            self.loot_bag.weight_max += 5
            print(f"{self.name}'s Lootbag Capacity increased by 5!")
        self.stat_points -= 5

    def gain_xp(self, drops:list=None, xp_gained:int=None) -> None:
        if drops is None and xp_gained is not None:
            self.xp += xp_gained
        else:
            xp_gained = drops[0]
            self.xp += drops[0]
        print(f"{self.name} Gained {xp_gained} XP! Current XP: {self.xp}/{self.level * 100}")
        if self.xp >= self.level*100:
            self.xp -= self.level * 100
            self.level_up()
    
    def gain_gold(self, drops) -> None:
        self.gold += drops[1]
        print(f"{self.name} Picked up {drops[1]} Gold! Current Gold: {self.gold}")

    def pick_up(self, drops) -> None:
        #IMPLEMENT ERROR CHECKS HERE, IF NO DROPS, INVENTORY FULL ETC
        self.inventory.add_item(drops[2])

    def inspect(self, target) -> None:
        if target is None:
            print("No enemies present...")
        if isinstance(target, Enemy):
            print(f"Inspecting Enemy...")
            print(f"Name: {target.name}")
            print(f"Max Health: {target.health_max}")
            print(f"Max Mana: {target.mana_max}")
            print(f"Attack Rating: {target.attack_rating}")
            print(f"Defense: {target.defense}")
            print(f"Weapon: {target.weapon.name}")
            print(f"    Weapon Damage: {target.weapon.damage}")
            print(f"    Weapon Hit Rating: {target.weapon.hit_rating}")
        else:
            target = Item.get_item_by_name(target)
            if isinstance(target, Weapon):
                print(f"Inspecting {target.name}...")
                print(f"Name: {target.name}")
                print(f"Rarity: {target.rarity}")
                print(f"Prefix: {target.prefix}")
                print(f"Suffix: {target.suffix}")
                print(f"Damage: {target.damage}")
                print(f"Hit Rating: {target.hit_rating}")
                print(f"Value: {target.value}")
                print(f"Weight: {target.weight}")
                
            elif isinstance(target, Potion):
                print(f"Inspecting {target.name}...")
                print(f"Name: {target.name}")
                print(f"Description: {target.description}")
                print(f"Duration: {target.duration}")
                print(f"Value: {target.value}")
                print(f"Weight: {target.weight}")

    def draw_stats(self) -> None:
        print(f"Attack Rating: {self.attack_rating}")
        print(f"Defense: {self.defense}")
        print(f"Gold: {self.gold}")
        print(f"Lootbag:")
        print(f"    Lootbag Damage: {self.weapon.damage}")
        print(f"    Lootbag Hit Rating: {self.weapon.hit_rating}")
        print(f"    Lootbag Capacity: {self.loot_bag.weight}/{self.loot_bag.weight_max}")

    def die(self) -> None:
        print(f"{self.name} has fallen in combat! Your glorious deeds will be remembered.")
        exit()

    def use(self, item_to_use: str) -> None:
        item_to_use = Item.get_item_by_name(item_to_use)
        if item_to_use:
            if item_to_use in self.inventory.items:
                if item_to_use.item_type == "Potion":
                    if item_to_use.potion_type == "mana":
                        self.mana += item_to_use.effect_value
                        self.health_bar.draw()
                        self.mana_bar.draw()
                        print(f"{self.name} Restored {item_to_use.effect_value} Mana!")
                        self.inventory.remove_item(item_to_use.name)
                    elif item_to_use.potion_type == "health":
                        self.health_max += item_to_use.effect_value
                        self.health_bar.update()
                        self.health_bar.draw()
                        self.mana_bar.draw()
                        print(f"{self.name} Increased their maximum health by {item_to_use.effect_value}!")
                        self.inventory.remove_item(item_to_use.name)
                else:
                    print("Invalid Item Type.")
            else:
                print("Item not in inventory.")
        else:
            print("Invalid Item.")


    def heal(self, heal_amount) -> None:
        mana_cost = 1 # BALANCE LATER
        #spend X Mana to heal self
        if self._mana >= mana_cost:
            #implement range check, cant overheal
            if (self.health_max - self.health) > heal_amount:
                self.health += heal_amount
            else:
                #allow "wasted" healing
                self.health = self.health_max
            #possibly add condition to restrict wasting mana on useless heals
            self.mana -= mana_cost
            #self.mana_bar.update()
            print(f"{self.name} used {mana_cost} Mana to restore {heal_amount} health.")

        else:
            print(f"Not enough Mana!")

    #def equip(self, LootBag) -> None:
        #self.weapon = LootBag
        #print(f"{self.name} equipped their Loot Bag.")

    #def drop(self) -> None:
        #self.weapon = self.default_weapon
        #print(f"{self.name} dropped their {self.weapon.name}.")

    def to_dict(self) -> dict:
        #Convert object to dict for saving
        
        inventory_list = self.inventory.items
        lootbag_list = self.loot_bag.items
        for i, item in enumerate(inventory_list):
            if isinstance(item, Potion):
                inventory_list[i] = item.to_dict()
            elif isinstance(item, Weapon):
                inventory_list[i] = item.to_dict()
        
        for i, item in enumerate(lootbag_list):
            if isinstance(item, Weapon):
                lootbag_list[i] = item.to_dict()

        return {
            "name": self.name,
            "level": self.level,
            "xp": self.xp,
            "health": self.health,
            "health_max": self.health_max,
            "mana": self.mana,
            "mana_max": self.mana_max,
            "attack_rating": self.attack_rating,
            "defense": self.defense,
            "gold": self.gold,
            "loot_bag": lootbag_list,
            "inventory": inventory_list
        }
    @classmethod
    def from_dict(cls, data):

        #add weapons to weapons list so they can be accessed later
        for i, item in enumerate(data["loot_bag"]):
            if item["item_type"] == "Weapon":
                item_to_add = Weapon.from_dict(item)
                data["loot_bag"][i] = item_to_add
                if item_to_add not in Item.all_items_list:
                    Item.all_items_list.append(item_to_add)

            elif item["item_type"] == "Potion":
                item_to_add = Potion.get_potion_by_name(item["name"])
                data["loot_bag"][i] = item_to_add

        for i, item in enumerate(data["inventory"]):
            if item["item_type"] == "Weapon":
                item_to_add = Weapon.from_dict(item)
                data["inventory"][i] = item_to_add
                if item_to_add not in Item.all_items_list:
                    Item.all_items_list.append(item_to_add)

            elif item["item_type"] == "Potion":
                item_to_add = Potion.get_potion_by_name(item["name"])
                data["inventory"][i] = item_to_add

        hero = cls(
            name=data["name"],
            level=data["level"],
            xp=data["xp"],
            health=data["health"],
            mana=data["mana"],
            attack_rating=data["attack_rating"],
            defense=data["defense"],
            loot_bag=LootBag(items=data["loot_bag"]),
            inventory=Inventory(items=data["inventory"]),
            gold=data["gold"]
        )

        hero.health_max = data["health_max"]
        hero.mana_max = data["mana_max"]
        hero.health_bar = HealthBar(hero, color= "red")
        hero.mana_bar = ManaBar(hero, color= "blue")
        return hero

class Enemy(Character):
    active_enemy = None

    enemy_weapons_list = ["Wooden Stick", "Iron Dagger", "Wooden Club", "Iron Shortsword"]
    all_enemies_list = [
        {"name": "Goblin Grunt", 
         "health": 50,
         "mana": 1,
         "attack_rating": 50,
         "defense": 10,
         "weapon": "Wooden Stick"},

         {"name": "Goblin Thug", 
         "health": 80,
         "mana": 1,
         "attack_rating": 50,
         "defense": 15,
         "weapon": "Wooden Club"},

         {"name": "Bandit Rookie", 
         "health": 75,
         "mana": 2,
         "attack_rating": 66,
         "defense": 20,
         "weapon": "Iron Dagger"},

         {"name": "Bandit Scout", 
         "health": 100,
         "mana": 3,
         "attack_rating": 70,
         "defense": 25,
         "weapon": "Iron Shortsword"},
    ]

    def __init__(self, 
                 name: str, 
                 health: int,
                 mana: int,
                 attack_rating: int,
                 defense: int,
                 weapon: Weapon,
                 health_max: int=None,
                 mana_max: int=None
                 ) -> None:
        #Possibly need to optionally declare health and mana max here 
        #to allow for loading enemies with less than max health.
        super().__init__(name=name, health=health, mana=mana, attack_rating=attack_rating, defense=defense)
        self.weapon = weapon
        if health_max:
            self.health_max = health_max
        if mana_max:
            self.mana_max = mana_max
        self.health_bar = HealthBar(self, color= "grey")
        self.mana_bar = ManaBar(self, color= "blue")

        Enemy.active_enemy = self

    @classmethod
    def spawn_enemy(cls, hero: object, enemy_name: str = None) -> object:

        if enemy_name:
            enemy_data = next((enemy for enemy in cls.all_enemies_list if enemy["name"].lower() == enemy_name.lower()), None)
        elif hero.level < 2:
            enemy_data = cls.all_enemies_list[0]
        else:
            enemy_data = choice(cls.all_enemies_list)
        
        #randomize health value +/- 10%, round to nearest 5
        name = enemy_data["name"]
        health = round((enemy_data["health"] * uniform(0.9, 1.1)) / 5) * 5
        mana = enemy_data["mana"]
        attack_rating = enemy_data["attack_rating"]
        defense = enemy_data["defense"]
        weapon_name = enemy_data["weapon"]
        #always spawn enemy with basic stick if level 1
        if hero.level < 2:
            enemy_weapon = Weapon.get_weapon_by_name(weapon_name=weapon_name)
        else:
            enemy_weapon = Weapon.generate_weapon(weapon_base=weapon_name)

        print(f"A {name} appears!")
        return cls(
            name=name, 
            health=health, 
            mana=mana, 
            attack_rating = attack_rating, 
            defense = defense, 
            weapon=enemy_weapon
            )

    def generate_drops(self) -> list:
        drops = []
        #drop xp
        xp = self.health_max // 10
        drops.append(xp)
        #drop gold
        gold = (self.health_max // 20) * randint(1,3)
        drops.append(gold)
        #drop items
        item = self.weapon.name
        if (randint(1,100) < 50):
            drops.append(item)
        return drops

    def die(self) -> None:
        print(f"{self.name} has been killed!")
        #spawn new enemy
        #return Enemy.spawn_enemy()

    def death_cleanup(self) -> None:
        #garbage collection
        Enemy.active_enemy = None

    def to_dict(self) -> dict:
        #Convert object to dict for saving
        weapon_dict = self.weapon.to_dict()
        return {
            "name": self.name,
            "health": self.health,
            "health_max": self.health_max,
            "mana": self.mana,
            "mana_max": self.mana_max,
            "attack_rating": self.attack_rating,
            "defense": self.defense,
            "weapon": weapon_dict
        }
    @classmethod
    def from_dict(cls, data):

        #Possibly need to configure weapon object, maybe not. Test.
        weapon = Weapon.from_dict(data["weapon"])

        enemy = cls(
            name=data["name"],
            health=data["health"],
            mana=data["mana"],
            attack_rating=data["attack_rating"],
            defense=data["defense"],
            weapon=weapon,
            health_max=data["health_max"],
            mana_max=data["mana_max"]
        )

        #enemy.health_max = data["health_max"]
        #enemy.mana_max = data["mana_max"]
        return enemy

