from character import Hero
from items import Item, Weapon, Potion
from loot_bag import LootBag
import random

class Shop:
    def __init__(self, stock: dict = None):
        self.stock = stock if stock is not None else {}

    def generate_shop(self) -> None:
        #fill in with default items (mana potion, 10g)
        self.stock = {}
        mana_potion = Potion.get_potion_by_name("mana potion")
        self.stock[mana_potion.name] = mana_potion

        stocked_weapon = Weapon.generate_weapon()
        self.stock[stocked_weapon.name] = stocked_weapon


    def buy(self, hero, item_name: str) -> None:
        matching_item = next((item for item in self.stock if item.lower() == item_name.lower()), None)
        if matching_item:
            price = self.stock[matching_item].value
            #Check if can afford, or inventory full, dont waste gold
            if hero.gold >= price:
                if hero.inventory.weight < hero.inventory.weight_max:
                    hero.gold -= price
                    print(f"{matching_item} Purchased for {price} Gold.")
                    hero.inventory.add_item(matching_item)
                    print(f"Thanks for stopping by, {hero.name}!")
                else:
                    print(f"I Can't Carry Anymore. Current Weight: {hero.inventory.weight}/{hero.inventory.weight_max}")
                    print(f"Thanks for stopping by, {hero.name}!")
            else:
                print(f"Not enough Gold. Current Gold: {hero.gold}")
                print(f"Thanks for stopping by, {hero.name}!")
        else:
            print(f"Item not Found.")
            print(f"Thanks for stopping by, {hero.name}!")

    def sell(self, hero, item_name: str) -> None:
        matching_item = next((item for item in hero.inventory.items if item.name.lower() == item_name.lower()), None)
        if matching_item:
            price = matching_item.value
            hero.gold += price
            print(f"{matching_item.name} Sold for {price} Gold.")
            hero.inventory.remove_item(matching_item.name)
            print(f"Thanks for stopping by, {hero.name}!")
        else:
            print(f"Item not Found.")
            print(f"Thanks for stopping by, {hero.name}!")

    def draw(self) -> None:
        print("Welcome to my Shop!")
        for item_name, item_obj in self.stock.items():
            print(f"{item_name}: {item_obj.value} gold")

    def to_dict(self):
        stock_dict = self.stock
        for item, value in stock_dict:
            if isinstance(value, Potion):
                value = value.to_dict()
            if isinstance(value, Weapon):
                value = value.to_dict()
        return stock_dict

    @classmethod
    def from_dict(cls, data):

        shop = Shop(data)
        stocked_weapon_dict = list(data.values())[1]
        stocked_weapon = Weapon.get_weapon_by_name(weapon_name=stocked_weapon_dict["name"],prefix=stocked_weapon_dict["prefix"],suffix=stocked_weapon_dict["suffix"])
        shop.stock[stocked_weapon.name] = stocked_weapon
        
        return shop