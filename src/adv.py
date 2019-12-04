from room import Room
from item import Item
from item import LightSource

from colorama import init, Fore, Back, Style
init(convert=True)

# Declare all the rooms

room = {
    'outside':  Room("Outside Cave Entrance",
                     "North of you, the cave mount beckons"),

    'foyer':    Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east."""),

    'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm."""),

    'narrow':   Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air."""),

    'treasure': Room("Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south."""),
}


# Link rooms together

room['outside'].n_to = room['foyer']
room['foyer'].s_to = room['outside']
room['foyer'].n_to = room['overlook']
room['foyer'].e_to = room['narrow']
room['overlook'].s_to = room['foyer']
room['narrow'].w_to = room['foyer']
room['narrow'].n_to = room['treasure']
room['treasure'].s_to = room['narrow']

# Populate rooms

room['outside'].items.append(LightSource('Lamp', 'A small metal lamp with glass windows'))
room['outside'].items.append(LightSource('Rope', 'Twisted hemp forms a long, flexible rope'))

#
# Main
#

# Make a new player object that is currently in the 'outside' room.

from player import Player

player_1 = Player(room["outside"])

# Write a loop that:
#
# * Prints the current room name
# * Prints the current description (the textwrap module might be useful here).
# * Waits for user input and decides what to do.
#
# If the user enters a cardinal direction, attempt to move to the room there.
# Print an error message if the movement isn't allowed.
#
# If the user enters "q", quit the game.

while True:
    print(Fore.GREEN + "==============")
    if not player_1.name:
        name = input("What is your name? ")
        player_1.name = name
    
    print(Fore.CYAN + f"\nYou are in {player_1.room.name}.")
    
    print(f"\n{player_1.room.description}")

    item_str = ""
    for i in range(len(player_1.room.items)):
        if i < len(player_1.room.items) - 1:
            item_str += player_1.room.items[i].name + ', '
        else:
            item_str += player_1.room.items[i].name + '.'

    if item_str:
        print(f"\nIn the room, you see: " + Fore.YELLOW + f"{item_str}")

    print(Fore.GREEN + "")
    cmd = input("What do you want to do? ")

    if cmd.lower() == "q" or cmd.lower() == "quit":
        print(Fore.RED + f"\n{player_1.name} is quitting this game!")
        break
    else:
        player_1.move(cmd)

