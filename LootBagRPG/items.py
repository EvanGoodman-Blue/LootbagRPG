import random

class Item:
    all_items_list = []

    def __init__(self,
                 name: str,
                 item_type: str,
                 value: int,
                 weight: int,
                 ):
        self.name = name
        self.item_type = item_type
        self.value = value
        self.weight = weight
        # ADD DESCRIPTIONS HERE FOR ALL ITEMS, REFACTOR POTION DESCRIPTIONS

        Item.all_items_list.append(self)

    @classmethod
    def get_item_by_name(cls, name: str) -> object:
        #Finds and returns item object by name (case insensitive)
        return next(
            (item for item in cls.all_items_list 
             if item.name.lower() == name.lower()),
            None
        )
    
    def to_dict(self):
        #implement generic item to dict function that checks which class object is and calls appropriate function.
        pass
    
    def __repr__(self):
        return (f"{self.__class__.__name__}({self.name}," 
        f"Type: {self.item_type}," 
        f"Value: {self.value}, "
        f"Weight: {self.weight})")

class Weapon(Item):   
    all_weapons_list = []
    WEAPON_PREFIXES = {
        "": {
            "damage": 0,
            "hit_rating": 0,
            "affix_rarity": 0,
            "value": 0
        },
        "Cracked": {
            "damage": -1,
            "hit_rating": -10,
            "affix_rarity": 5,
            "value": -2
        },
        "Sharp": {
            "damage": 1,
            "hit_rating": 5,
            "affix_rarity": 10,
            "value": +5
        }

    }
    WEAPON_SUFFIXES = {
        "": {
            "damage": 0,
            "hit_rating": 0,
            "affix_rarity": 0,
            "value": 0
        },
        "of Imbalance": {
            "hit_rating": -10,
            "affix_rarity": 5,
            "value": -2
        },
        "of Pain": {
            "damage": 1,
            "affix_rarity": 10,
            "value": 5
        }
    }
    WEAPON_BASES = [
        {
            "name": "Wooden Stick",
            "weapon_type": "club",
            "rarity": "Crude",
            "damage": 2,
            "hit_rating": 75,
            "value": 5,
            "weight": 1
        },
        {
            "name": "Iron Dagger",
            "weapon_type": "dagger",
            "rarity": "Common",
            "damage": 5,
            "hit_rating": 50,
            "value": 10,
            "weight": 1
        }

    ]

    # Generate lists of prefixes paired with their rarity weights, use later when choosing which affix to add
    WEAPON_PREFIX_NAMES, WEAPON_PREFIX_RARITY = zip(*[(prefix, data["affix_rarity"]) for prefix, data in WEAPON_PREFIXES.items()])
    WEAPON_SUFFIX_NAMES, WEAPON_SUFFIX_RARITY = zip(*[(suffix, data["affix_rarity"]) for suffix, data in WEAPON_SUFFIXES.items()])

    def __init__(self, 
                 name: str, 
                 weapon_type: str, 
                 rarity: str, 
                 damage: int, 
                 hit_rating: int,
                 value: int, 
                 weight: int,
                 prefix: str = None,
                 suffix: str = None,
                 weapon_base: str = None
                 ) -> None:
        super().__init__(name=name, item_type="Weapon", value=value, weight=weight)
        self.weapon_type = weapon_type
        self.rarity = rarity
        self.damage = damage
        self.hit_rating = hit_rating

        self.prefix = prefix
        self.suffix = suffix
        self.weapon_base = weapon_base

        if self.prefix and self.prefix in Weapon.WEAPON_PREFIXES:
            self.apply_affix(Weapon.WEAPON_PREFIXES[self.prefix])

        if self.suffix and self.suffix in Weapon.WEAPON_SUFFIXES:
            self.apply_affix(Weapon.WEAPON_SUFFIXES[self.suffix])

        self.update_name()

        Weapon.all_weapons_list.append(self)

    def apply_affix(self, affix: dict):
        for stat, value in affix.items():
            if hasattr(self, stat):
                setattr(self, stat, getattr(self, stat) + value)

    def update_name(self):
        new_name = self.name
        if self.prefix:
            new_name = f"{self.prefix} {new_name}"
        if self.suffix:
            new_name = f"{new_name} {self.suffix}"
        self.name = new_name

    @classmethod
    def generate_weapon(cls, weapon_base: str = None, prefix: str = None, suffix: str = None) -> object:
        
        #If no weapon base provided, choose randomly
        if weapon_base is None:
            weapon_base = random.choice(cls.WEAPON_BASES)
        #Otherwise, get weapon_base by name
        else:
            weapon_base = next(
                (base for base in cls.WEAPON_BASES if base["name"].lower() == weapon_base.lower()),
                None
            )
        if prefix is None:
            if random.random() < 0.5: # Change to "enchantability" later
                prefix = random.choices(cls.WEAPON_PREFIX_NAMES, weights=cls.WEAPON_PREFIX_RARITY, k=1)[0]
            else:
                prefix = None

        if suffix is None:
            if random.random() < 0.25: # Change to "enchantability / 2" later
                suffix = random.choices(cls.WEAPON_SUFFIX_NAMES, weights=cls.WEAPON_SUFFIX_RARITY, k=1)[0]
            else:
                suffix = None

        weapon_base_name = weapon_base["name"]

        return cls(
            name=weapon_base["name"],
            weapon_type=weapon_base["weapon_type"],
            rarity=weapon_base["rarity"],
            damage=weapon_base["damage"],
            hit_rating=weapon_base["hit_rating"],
            value=weapon_base["value"],
            weight=weapon_base["weight"],
            prefix=prefix,
            suffix=suffix,
            weapon_base=weapon_base_name
        )
    
    def to_dict(self):
        if self.prefix is None:
            self.prefix = ""
        if self.suffix is None:
            self.suffix = ""
        return {
            "name": self.name,
            "item_type": self.item_type,
            "weapon_type": self.weapon_type,
            "rarity": self.rarity,
            "damage": self.damage,
            "hit_rating": self.hit_rating,
            "value": self.value,
            "weight": self.weight,
            "prefix": self.prefix,
            "suffix": self.suffix,
            "weapon_base": self.weapon_base
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        #call generate weapon with weapon base, prefix and suffix
        weapon_base = data["weapon_base"]
        prefix = data["prefix"]
        suffix = data["suffix"]
        weapon = Weapon.generate_weapon(weapon_base=weapon_base, prefix=prefix, suffix=suffix)
        return weapon

    @classmethod
    def get_weapon_by_name(cls, weapon_name: str, prefix: str = None, suffix: str = None) -> object:
        #Finds and returns weapon object by name (case insensitive)
        #If no weapon found in current weapon list, generate weapon according to specs
        #If generating weapon, weapon_name becomes base name, then optional affixes added
        found_weapon = next(
            (weapon for weapon in cls.all_weapons_list 
             if weapon.name.lower() == weapon_name.lower()),
            None
        )
        if found_weapon == None:
            weapon_base = next(
                (base for base in cls.WEAPON_BASES if base["name"].lower() == weapon_name.lower()),
                None
            )
            if weapon_base == None:
                #invalid weapon base found, return error
                print(f"Invalid Weapon")
                return None
            else:
                generated_weapon = Weapon.generate_weapon(weapon_base=weapon_base["name"], prefix=prefix, suffix=suffix)
                return generated_weapon
        else:
            return found_weapon

    
    def __repr__(self) -> str:
        return (f"OBJECT.Weapon({self.name}, Type: {self.weapon_type}, Rarity: {self.rarity}, Damage: {self.damage}, Hit Rating: {self.hit_rating}, Value: {self.value}, Weight: {self.weight})")

class Potion(Item):
    all_potions_list = []

    def __init__(self, 
                 name: str, 
                 potion_type: str,
                 effect_value: int,
                 value: int, 
                 weight: int,
                 description: str,
                 duration: int = 0):
        super().__init__(name=name, item_type="Potion", value=value, weight=weight)
        self.potion_type = potion_type
        self.duration = duration
        self.effect_value = effect_value
        self.description = description

        Potion.all_potions_list.append(self)

    @classmethod
    def get_potion_by_name(cls, name: str) -> object:
        #Finds and returns item object by name (case insensitive)
        return next(
            (potion for potion in cls.all_potions_list 
             if potion.name.lower() == name.lower()),
            None
        )
    
    def to_dict(self):
        return {
            "name": self.name,
            "item_type": self.item_type,
            "potion_type": self.potion_type,
            "effect_value": self.effect_value,
            "duration": self.duration,
            "value": self.value,
            "weight": self.weight,
            "description": self.description
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data["name"],
            potion_type=data["potion_type"],
            effect_value=data["effect_value"],
            value=data["value"],
            weight=data["weight"],
            description=data["description"],
            duration=data["duration"]
        )

    def __repr__(self):
        return (f"Potion({self.name}, "
        f"Type: {self.potion_type}, "
        f"Effect Value: {self.effect_value}, "
        f"Value: {self.value}, "
        f"Weight: {self.weight}, "
        f"Duration: {self.duration},"
        f"Description: {self.description})")
    

#Template weapon
"""
temp = Weapon(name="temp",
                      weapon_type="temp",
                      rarity="temp",
                      damage=1,
                      hit_rating=1,
                      value=1,
                      weight=1)
"""

"""
fists = Weapon(name="Fists",
                      weapon_type="fists",
                      rarity="Crude",
                      damage=1,
                      hit_rating=100,
                      value=1,
                      weight=1)
"""


"""wooden_stick = Weapon(name="Wooden Stick",
                      weapon_type="club",
                      rarity="Crude",
                      damage=2,
                      hit_rating=75,
                      value=5,
                      weight=1)"""

"""iron_dagger = Weapon(name="Iron Dagger",
                      weapon_type="dagger",
                      rarity="Common",
                      damage=5,
                      hit_rating=50,
                      value=10,
                      weight=1)
                      """

mana_potion = Potion(name="Mana Potion",
                     potion_type="mana",
                     effect_value=5,
                     value=10,
                     weight=1,
                     description="Restores 5 Mana. Tastes Bitter.")