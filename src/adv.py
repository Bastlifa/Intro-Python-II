from room import Room
from item import Item
from item import LightSource

from colorama import init, Fore, Back, Style
init(convert=True)

# Declare all the rooms

room = {
    'outside':  Room("Outside Cave Entrance",
                     "North of you, the cave mouth beckons"),

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
room['outside'].items.append(Item('Rope', 'Twisted hemp forms a long, flexible rope'))

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

game_running = True

def input_process(input_str):
    lower_input = input_str.lower()

    if lower_input == 'q' or lower_input == 'quit':
        print(Fore.RED + f"\n{player_1.name} is quitting this game!")
        global game_running
        game_running = False
    elif lower_input in ['n', 'north', 'e', 'east', 's', 'south', 'w', 'west']:
        player_1.move(lower_input)
    elif len(lower_input.split()) > 1:
        verb_noun(lower_input.split())
    else:
        print(Fore.RED + "\nThat command is not valid.")
        print(Style.RESET_ALL)

def verb_noun(cmd_list):
    if cmd_list[0] == "get":
        item_names = []
        for item in player_1.room.items:
            item_names.append(item.name.lower())
        if cmd_list[1] in item_names:
            player_1.get_item(player_1.room.items[item_names.index(cmd_list[1])])
        else:
            print("")
    elif cmd_list[0] == "check" and cmd_list[1] == "inventory":
        player_1.check_inventory()
    elif cmd_list[0] == "drop":
        item_names = []
        for item in player_1.inventory:
            item_names.append(item.name.lower())
        if cmd_list[1] in item_names:
            player_1.drop_item(player_1.inventory[item_names.index(cmd_list[1])])


print(Fore.YELLOW + '''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(                                     ) 
)            Python Quest             (
(                                     )
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~''')

while game_running:
    print(Fore.GREEN + "=======================================")
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

    input_process(cmd)

