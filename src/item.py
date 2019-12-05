from colorama import init, Fore, Back, Style
init(convert=True)

class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def on_take(self, player):
        print(Fore.YELLOW + f"\n{player.name} has picked up {self.name}")
        print(Style.RESET_ALL)
        player.room.items.remove(self)
        player.inventory.append(self)
        player.last_item = self

    def on_drop(self, player):
        print(Fore.YELLOW + f"\n{player.name} has dropped {self.name}")
        print(Style.RESET_ALL)
        player.room.items.append(self)
        player.inventory.remove(self)
        

class LightSource(Item):
    def __init__(self, name, description):
        super().__init__(name, description)

    def on_drop(self, player):
        print(Fore.YELLOW + f"\nIt's not wise to drop your source of light, {player.name}")
        print(Fore.YELLOW + f"\n{player.name} has dropped {self.name}")
        print(Style.RESET_ALL)
        player.room.items.append(self)
        player.inventory.remove(self)
