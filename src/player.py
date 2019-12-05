# Write a class to hold player information, e.g. what room they are in
# currently.

from room import Room
from item import LightSource

from playsound import playsound
from colorama import init, Fore, Back, Style
init(convert=True)

def lit_area(player):
    for item in player.inventory + player.room.items:
        if isinstance(item, LightSource):
            return True
    
    if player.room.lit:
        return True
    
    return False

class Player:
    def __init__(self, room):
        self.name = ""
        self.room = room
        self.inventory = []
        self.hp = 100

    def move(self, direction):
        lower_dir = direction.lower()

        def check_and_move(dir_str):
            str_dict = {"n": "north", "e": "east", "s": "south", "w": "west"}
            try:
                if getattr(self.room, f"{dir_str}_to") != None:
                    if (self.room.name == "Grand Overlook" and dir_str == "n")\
                    or (self.room.name == "Fountain" and dir_str == "s"):
                        self.room = getattr(self.room, f"{dir_str}_to")
                        print(Fore.CYAN + f"\nYou use your rope and grappling hook to cross the chasm!")
                        playsound('./assets/game_sounds/footsteps.mp3', False)
                    else:
                        self.room = getattr(self.room, f"{dir_str}_to")
                        print(Fore.CYAN + f"\nYou move to the {str_dict[dir_str]}")
                        playsound('./assets/game_sounds/footsteps.mp3', False)
                else:
                    raise("")
            except:
                if lit_area(self):
                    print(Fore.RED + f"\n{self.room.name} has no exits to the {str_dict[dir_str]}")
                    playsound('./assets/game_sounds/buzz.mp3', False)
                else:
                    print(Fore.RED + f"\nThere are no exits that way!")
                    playsound('./assets/game_sounds/buzz.mp3', False)
                return

        if lower_dir == "north" or lower_dir == "n":
            check_and_move("n")
        elif lower_dir == "east" or lower_dir == "e":
            check_and_move("e")
        elif lower_dir == "south" or lower_dir == "s":
            check_and_move("s")
        elif lower_dir == "west" or lower_dir == "w":
            check_and_move("w")
        else:
            print(Fore.RED + f"\n{direction} is not a valid move")
            playsound('./assets/game_sounds/buzz.mp3', False)
            return

    def get_item(self, item):
        item.on_take(self)

    def check_inventory(self):
        print(Fore.YELLOW + f"\n{self.name} has the following items:")
        for item in self.inventory:
            print(Fore.YELLOW + f"{item.name}")
        print(Style.RESET_ALL)
    
    def drop_item(self,item):
        item.on_drop(self)
