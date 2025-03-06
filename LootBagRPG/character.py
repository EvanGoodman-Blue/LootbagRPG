from items import Item, Weapon, Potion
from loot_bag import LootBag
from inventory import Inventory
from health_bar import HealthBar, ManaBar
from random import randint, choice, uniform
#from shop import Shop

class Character:   
    def __init__(self, name: str, health: int, mana: int, attack_rating: int, defense: int) -> None:
        self.name = name
        self._health = health
        self.health_max = health
        self._mana = mana
        self.mana_max = mana
        self.attack_rating = attack_rating
        self.defense = defense
        self.health_bar = HealthBar(self)
        self.mana_bar = ManaBar(self)

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
                 gold: int=0
                 ) -> None:
        super().__init__(name=name, health=health, mana=mana, attack_rating=attack_rating, defense=defense)

        self.level = level
        self.xp = xp
        self.gold = gold
        self.loot_bag = loot_bag
        self.inventory = inventory
        self.weapon = self.loot_bag
        self.health_bar = HealthBar(self, color= "red")
        self.mana_bar = ManaBar(self, color= "blue")

    def level_up(self) -> None:
        self.level += 1
        #implement level bonuses (max health, defense, attack rating, lootbag weight)
        print(f"{self.name} Advanced to Level {self.level}!")

    def gain_xp(self, drops:list=None, xp:int=None) -> None:
        if drops is None and xp is not None:
            xp_gained = xp
            self.xp += xp
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
        #eventually implement intermediate inventory system
        self.inventory.add_item(drops[2])

    def inspect(self, target) -> None:
        if target:
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
            print("No enemies present...")

    def draw_stats(self) -> None:
        print(f"{self.name}'s Stats")
        print(f"Level: {self.level}")
        print(f"XP: {self.xp}/{self.level * 100}")
        print(f"Max Health: {self.health_max}")
        print(f"Max Mana: {self.mana_max}")
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
                Item.all_items_list.append(item_to_add)

            elif item["item_type"] == "Potion":
                item_to_add = Potion.get_potion_by_name(item["name"])
                data["loot_bag"][i] = item_to_add

        for i, item in enumerate(data["inventory"]):
            if item["item_type"] == "Weapon":
                item_to_add = Weapon.from_dict(item)
                data["inventory"][i] = item_to_add
                Item.all_items_list.append(item)

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

    enemy_weapons_list = ["Wooden Stick", "Iron Dagger"]
    all_enemies_list = [
        {"name": "Goblin", 
         "health": 50,
         "mana": 1,
         "attack_rating": 50,
         "defense": 10,
         "weapon": "Wooden Stick"},

         {"name": "Bandit", 
         "health": 75,
         "mana": 2,
         "attack_rating": 66,
         "defense": 20,
         "weapon": "Iron Dagger"}
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

