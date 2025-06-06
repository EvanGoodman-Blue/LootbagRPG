from items import Item

class Inventory:
    def __init__(self,
                 weight: int = 0,
                 weight_max: int = 10,
                 items: list = None
                 ) -> None:
        
        self.weight = weight
        self.weight_max = weight_max
        self.items = items if items is not None else []

        self.update_inventory()
        
    def update_weight(self) -> None:
        self.weight = 0
        if len(self.items) > 0:
            for item in self.items:
                self.weight += item.weight

    def update_inventory(self) -> None:
        self.update_weight()

    def add_item(self, item_name: str) -> None:
        item_to_add = Item.get_item_by_name(item_name)

        if item_to_add is None:
            print(f"Invalid Item: '{item_name}' does not exist.")

        elif item_to_add.weight > self.weight_max - self.weight:
            print(f"I can't carry any more.")

        else:
            self.items.append(item_to_add)
            self.update_inventory()
            print(f"{item_to_add.name} added to inventory.")

    def remove_item(self, item_name: str) -> bool:
        item_to_remove = Item.get_item_by_name(item_name)

        if item_to_remove is None:
            print(f"Invalid Item: '{item_name}' does not exist.")
            return False
        
        elif item_to_remove not in self.items:
            print(f"'{item_name}' is not in your inventory.")
            return False
        
        else:
            self.items.remove(item_to_remove)
            self.update_inventory()
            print(f"{item_to_remove.name} removed from inventory.")
            return True

    def get_items(self) -> list:
        item_names = []
        for item in self.items:
            item_names.append(item.name)
        return item_names
    
    def draw(self, hero, shop_flag : bool = False) -> None:
        #print inventory weight/weight_max
        print(f"Inventory Weight: {self.weight}/{self.weight_max}")

        #print list of inventory items including name
        print(f"Inventory: ")
        if shop_flag:
            for item in self.items:
                print(f"{item.name}: {item.value} Gold")
        else:
            for item in self.items:
                print(f"{item.name}")

        print(f"Gold: {hero.gold}")

    def __repr__(self):
        return (f"{self.__class__.__name__}({self.name}," 
        f"Weight: {self.weight}," 
        f"Weight_max: {self.weight_max}, "
        f"Items: {self.items})")