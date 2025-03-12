import os
import math
os.system("")

class HealthBar:
    symbol_remaining: str = "█"
    symbol_lost: str = "_"
    barrier: str = "|"
    colors: dict = {"red": "\033[91m",
                    "purple": "\33[95m",
                    "blue": "\33[34m",
                    "blue2": "\33[36m",
                    "blue3": "\33[96m",
                    "green": "\033[92m",
                    "green2": "\033[32m",
                    "brown": "\33[33m",
                    "yellow": "\33[93m",
                    "grey": "\33[37m",
                    "default": "\033[0m"
                    }

    def __init__(self,                 
                 entity,
                 length: int = 20,
                 color: str = ""
                 ) -> None:
        
        self.entity = entity
        self.max_value = entity.health_max
        self.current_value = entity.health
        #optional for hard coded lengths, otherwise dynamically scaled to max health
        #self.length = length
        self.length = (self.max_value // 4)
        self.color = self.colors.get(color, self.colors.get("default"))

    def update(self) -> None:
        self.max_value = self.entity.health_max
        self.length = max(min((self.max_value // 4), 30),10)
        self.current_value = self.entity.health

    def draw(self) -> None:
        remaining_bars = round((self.current_value / self.max_value) * self.length)
        lost_bars = self.length - remaining_bars

        print(f"{self.entity.name}'s Health: {self.entity.health}/{self.entity.health_max}")
        print(f"{self.barrier}"
              f"{self.color}"
              f"{remaining_bars * self.symbol_remaining}"
              f"{lost_bars * self.symbol_lost}"
              f"{self.colors['default']}"
              f"{self.barrier}")
        

class ManaBar:
    symbol_remaining: str = "█"
    symbol_lost: str = "_"
    barrier: str = "|"
    colors: dict = {"red": "\033[91m",
                    "purple": "\33[95m",
                    "blue": "\33[34m",
                    "blue2": "\33[36m",
                    "blue3": "\33[96m",
                    "green": "\033[92m",
                    "green2": "\033[32m",
                    "brown": "\33[33m",
                    "yellow": "\33[93m",
                    "grey": "\33[37m",
                    "default": "\033[0m"
                    }

    def __init__(self,                 
                 entity,
                 length: int = 20,
                 color: str = ""
                 ) -> None:
        
        self.entity = entity
        self.max_value = entity.mana_max
        self.current_value = entity.mana
        #optional for hard coded lengths, otherwise dynamically scaled to max mana (1 per point)
        #self.length = length
        self.length = (self.max_value)
        self.color = self.colors.get(color, self.colors.get("default"))

    def update(self) -> None:
        self.current_value = self.entity.mana

    def draw(self) -> None:
        remaining_bars = round((self.current_value / self.max_value) * self.length)
        lost_bars = self.length - remaining_bars

        print(f"{self.entity.name}'s Mana: {self.entity.mana}/{self.entity.mana_max}")
        print(f"{self.barrier}"
              f"{self.color}"
              f"{remaining_bars * self.symbol_remaining}"
              f"{lost_bars * self.symbol_lost}"
              f"{self.colors['default']}"
              f"{self.barrier}")