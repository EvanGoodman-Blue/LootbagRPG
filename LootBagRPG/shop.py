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
            price = self.stock[matching_item]
            if hero.gold >= price:
                hero.gold -= price
                print(f"{matching_item} Purchased for {price} Gold.")
                hero.inventory.add_item(matching_item)
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
        for item, price in self.stock.items():
            print(f"{item}: {price} gold")

    def to_dict(self):
        return self.stock

    @classmethod
    def from_dict(cls, data):

        shop = Shop(data)
        stocked_weapon_name = list(data.keys())[1]
        stocked_weapon = Weapon.generate_weapon()
        shop.stock[stocked_weapon.name] = stocked_weapon.value 
        
        return shop