# Write a class to hold player information, e.g. what room they are in
# currently.

from room import Room
from colorama import init, Fore, Back, Style

init(convert=True)

class Player:
    def __init__(self, room):
        self.name = ""
        self.room = room

    def move(self, direction):
        lower_dir = direction.lower()

        def check_and_move(dir_str):
            str_dict = {"n": "north", "e": "east", "s": "south", "w": "west"}
            try:
                self.room = getattr(self.room, f"{dir_str}_to")
                print(Fore.CYAN + f"You move to the {str_dict[dir_str]}")
            except:
                print(Fore.RED + f"{self.room.name} has no exits to {str_dict[dir_str]}")
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
            print(Fore.RED + f"{direction} is not a valid move")
            return

        