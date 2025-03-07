from items import Weapon

class LootBag:
    def __init__(self,
                 value: int = 0, 
                 weight: int = 0,
                 weight_max: int = 10,
                 hit_rating: int = 100,
                 damage: int = 1,
                 items: list = None
                 ) -> None:
        self.items = items if items is not None else []
        self.damage = damage
        self.value = value
        self.weight = weight
        self.weight_max = weight_max
        self.hit_rating = hit_rating
        self.name = "Loot Bag"

        if items is None:
            default_weapon = Weapon.generate_weapon("Wooden Stick")
            self.add_item(default_weapon.name)
        self.update_bag()

    def update_weight(self) -> None:
        self.weight = 0
        if len(self.items) > 0:
            for item in self.items:
                self.weight += item.weight
            
    def update_damage(self) -> None:
        self.damage = 1
        if len(self.items) > 0:
            for item in self.items:
                self.damage += item.damage

    def update_value(self) -> None:
        self.value = 0
        if len(self.items) > 0:
            for item in self.items:
                self.value += item.value

    def update_hit_rating(self) -> None:
        #bag hit rating is average of all items inside
        #optionally include hit rating penalty for heavy bags
        self.hit_rating = 0
        if len(self.items) > 0:
            for item in self.items:
                self.hit_rating += item.hit_rating
            self.hit_rating = self.hit_rating // len(self.items)

    def update_bag(self) -> None:
        self.update_weight()
        self.update_damage()
        self.update_value()
        self.update_hit_rating()

    def add_item(self, weapon_name: str) -> None:
        weapon_to_add = Weapon.get_weapon_by_name(weapon_name)

        if weapon_to_add is None:
            print(f"Invalid Weapon: '{weapon_name}' does not exist.")

        elif weapon_to_add.weight > self.weight_max - self.weight:
            print(f"{weapon_name} won't fit.")

        else:
            self.items.append(weapon_to_add)
            self.update_bag()
            print(f"{weapon_to_add.rarity} {weapon_to_add.name} added to lootbag.")

    def remove_item(self, weapon_name) -> bool:
        weapon_to_remove = Weapon.get_weapon_by_name(weapon_name)

        if weapon_to_remove is None:
            print(f"Invalid Weapon: '{weapon_name}' does not exist.")
            return False
        
        elif weapon_to_remove not in self.items:
            print(f"Weapon '{weapon_name}' is not in your bag.")
            return False
        
        else:
            self.items.remove(weapon_to_remove)
            self.update_bag()
            print(f"{weapon_to_remove.rarity} {weapon_to_remove.name} removed from lootbag.")
            return True

    def get_items(self) -> list:
        item_names = []
        for item in self.items:
            item_names.append(item.name)
        return item_names
    
    def draw_bag(self) -> None:
        #print bag weight/weight_max
        print(f"Bag Weight: {self.weight}/{self.weight_max}")

        #print list of bag items including name, rarity, damage, atk rating
        print(f"Bag Contents: ")
        for item in self.items:
            print(f"{item.name}, dmg: {item.damage}, atk:{item.hit_rating}")
        print (f"Bag Damage: {self.damage}  Hit Rating: {self.hit_rating}")

    def __repr__(self):
        return (f"{self.__class__.__name__}({self.name}," 
        f"Weight: {self.weight}," 
        f"Weight_max: {self.weight_max}, "
        f"Items: {self.items})")