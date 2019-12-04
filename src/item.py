from colorama import init, Fore, Back, Style
init(convert=True)

class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def on_take(self, player):
        print(Fore.YELLOW + f"\n{player.name} has picked up {self.name}")
        player.room.items.remove(self)

    def on_drop(self, player):
        print(Fore.YELLOW + f"\n{player.name} has dropped {self.name}")
        player.room.items.append(self)


class LightSource(Item):
    def __init__(self, name, description):
        super().__init__(name, description)

    def on_drop(self, player):
        print(Fore.YELLOW + f"\nIt's not wise to drop your source of light, {player.name}")
        player.room.items.append(self)
