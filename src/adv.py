from room import Room, Room_Secret
from item import Item, LightSource, Weapon
from monster import monster
# import time
# import multiprocessing

import random
from playsound import playsound
from colorama import init, Fore, Back, Style
init(convert=True)

# Declare all the rooms

room = {
    'outside':  Room("Outside Cave Entrance",
                     "North of you, the cave mouth beckons", True),

    'foyer':    Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east.""", True),

    'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm.""", False),

    'narrow':   Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air.""", False),

    'treasure': Room("Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. Next to the chest, you see an old grappling hook.
The only exit is to the south.""", False),
    'fountain': Room("Fountain", """You find yourself in a marble-floored room
with a fountain in the center. The water gives off a faint light.
There are exits to the north, and west, and south crosses a chasm""", True),
    'armory': Room("Armory", """You enter an old armory. 
Most of the weapons have been long-removed.
The only exit is to the east.""", False),
    'hall': Room_Secret("Hall", """Arriving in a large room,
with pillars supporting the ceiling,
you see this was once a great hall. Alcoves once held
suits of armor, walls once bore elaborate tapestries.
Now, it's been ransacked, and is majestic no more.
Exits are to all directions.""", False, "plate"),
    'larder': Room("Larder", """You see before you a disused larder,
its contents having rotted away.
The only exit is to the west.""", False, monster['rat']),
    'indev': Room("In Development", """You see an unfinished room, the sign of a lazy dev.
Due to its default nature, there are no exits. Hope you enjoyed the game!""", True)
}


# Link rooms together

room['outside'].n_to = room['foyer']
room['foyer'].s_to = room['outside']
room['foyer'].n_to = room['overlook']
room['foyer'].e_to = room['narrow']
room['overlook'].s_to = room['foyer']
room['overlook'].n_to = None
room['narrow'].w_to = room['foyer']
room['narrow'].n_to = room['treasure']
room['treasure'].s_to = room['narrow']
room['fountain'].s_to = None
room['fountain'].w_to = room['armory']
room['armory'].e_to = room['fountain']
room['fountain'].n_to = room['hall']
room['hall'].e_to = room['larder']
room['hall'].s_to = room['fountain']
room['hall'].w_to = room['indev']
room['hall'].n_to = room['indev']
room['larder'].w_to = room['hall']

# Populate rooms

room['outside'].items.append(LightSource('Lamp', 'A small metal lamp with glass windows'))
room['outside'].items.append(Item('Rope', 'Twisted hemp forms a long, flexible rope'))
room['treasure'].items.append(Item('Grappling Hook', 'A metal hook, with three prongs'))
room['armory'].items.append(Weapon('Rusty Sword', 'A metal sword, rusty from long neglect',
    6, "Slashing"))
room['larder'].items.append(Item('Tasty Cake', 'A tasty old cake. Fills you up!'))

#
# Main
#

# Make a new player object that is currently in the 'outside' room.

from player import Player

player_1 = Player(room["outside"])

last_item = None

can_attack = False

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

is_fighting = False

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
    elif lower_input == "i" or lower_input == "inventory":
        player_1.check_inventory()
    elif (lower_input == "f" or lower_input == "fight") and player_1.room.monster != None:
        fight(player_1.room.monster)
    else:
        print(Fore.RED + "\nThat command is not valid.")
        playsound('./assets/game_sounds/buzz.mp3', False)
        print(Style.RESET_ALL)

def verb_noun(cmd_list):
    if cmd_list[0] == "get" or cmd_list[0] == "take":
        item_names = [item.name.lower() for item in player_1.room.items]
        cmd_list.pop(0)
        global last_item
        if last_item == None:
            print("get what?")
            playsound('./assets/game_sounds/buzz.mp3')
        elif ' '.join(cmd_list) in item_names:
            last_item = player_1.room.items[item_names.index(' '.join(cmd_list))]
            player_1.get_item(player_1.room.items[item_names.index(' '.join(cmd_list))])
            playsound('./assets/game_sounds/coin.mp3')
        elif cmd_list[0] == "it" and last_item.name.lower() in item_names:
            last_item = player_1.room.items[item_names.index(last_item.name.lower())]
            player_1.get_item(player_1.room.items[item_names.index(last_item.name.lower())])
            playsound('./assets/game_sounds/coin.mp3')
        else:
            print("get what?")
            playsound('./assets/game_sounds/buzz.mp3')
    elif cmd_list[0] == "check" and cmd_list[1] == "inventory":
        player_1.check_inventory()
    elif cmd_list[0] == "drop":
        item_names = [item.name.lower() for item in player_1.inventory]
        cmd_list.pop(0)
        if last_item == None:
            print("drop what?")
            playsound('./assets/game_sounds/buzz.mp3')
        elif ' '.join(cmd_list) in item_names:
            last_item = player_1.inventory[item_names.index(' '.join(cmd_list))]
            playsound('./assets/game_sounds/thunk_sound.mp3')
            player_1.drop_item(player_1.inventory[item_names.index(' '.join(cmd_list))])
        elif cmd_list[0] == "it" and last_item.name.lower() in item_names:
            player_1.drop_item(player_1.inventory[item_names.index(last_item.name.lower())])
            playsound('./assets/game_sounds/thunk_sound.mp3')
        else:
            print("drop what?")
            playsound('./assets/game_sounds/buzz.mp3')
    else:
        print("Say again?")
        playsound('./assets/game_sounds/buzz.mp3')


def situation_process():
    # not using comprehension here in order to modify can_attack
    # maybe a better way, set it in comprehension? Not sure if possible
    inventory_names = []
    global can_attack
    can_attack = False
    for item in player_1.inventory:
        inventory_names.append(item.name.lower())
        if isinstance(item, Weapon):
            can_attack = True

    if "rope" in inventory_names and "grappling hook" in inventory_names:
        room['overlook'].n_to = room["fountain"]
        room['fountain'].s_to = room["overlook"]
    else:
        room['overlook'].n_to = None
        room['fountain'].s_to = None

    
def fight(monst):
    global game_running
    while monst.hp > 0 and player_1.hp > 0 and game_running:
        print(Fore.MAGENTA + f"\nThe {monst.name} attacks!")
        if random.randint(1, 100) < monst.attack[0]:
            dmg = random.randint(1, monst.attack[1])
            print(f"\n{player_1.name} took " + Style.RESET_ALL + f" {dmg} " + Fore.MAGENTA + "damage!")
            player_1.hp -= dmg
        else:
            print(f"\nMiss!")
        print(Fore.GREEN)
        cmd = (input("\nWhat will you do? ")).lower()
        if cmd == "a" or cmd == "attack":
            wep = None
            for item in player_1.inventory:
                if isinstance(item, Weapon):
                    wep = item
                    break
            print(Fore.CYAN + f"\n{player_1.name} attacks!")
            dmg = random.randint(1, wep.dmg)
            monst.hp -= dmg
            print(Fore.CYAN + f"\n{player_1.name} hit for {dmg} damage!")
            if(monst.hp <= 0):
                print(f"\n{player_1.name} has slain the {monst.name}!")
                player_1.room.monster = None
        elif cmd == "q" or cmd == "quit":
            game_running = False

# def music_play():
#     while True:
#         try:
#             playsound('./assets/game_sounds/music.mp3')
#         except:
#             print("Error with music, stop trying to be fancy")

# if __name__ == '__main__':
#     p = multiprocessing.Process(target=music_play)
#     p.start()

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
    
    lit_area = False

    for item in player_1.inventory + player_1.room.items:
        if isinstance(item, LightSource):
            lit_area = True
    
    if player_1.room.lit:
        lit_area = True
    
    if lit_area:
        print(Fore.CYAN + f"\nYou are in {player_1.room.name}.")
        print(f"\n{player_1.room.description}")
        if player_1.room.monster != None:
            print(Fore.MAGENTA + f"\nThere is a {player_1.room.monster.name} here!")
            print(f"\n{player_1.room.monster.description}")
            print(f"\nDo you want to" + Style.RESET_ALL + f" fight?" + Fore.CYAN)
        item_str = ""
        for i in range(len(player_1.room.items)):
            if i < len(player_1.room.items) - 1:
                item_str += player_1.room.items[i].name + ', '
            else:
                item_str += player_1.room.items[i].name + '.'
                # global last_item
                last_item = player_1.room.items[i]

        if item_str:
            print(f"\nIn the room, you see: " + Fore.YELLOW + f"{item_str}")
    else:
        print(Fore.CYAN + f"\nIt's pitch black!")


    print(Fore.GREEN + "")
    cmd = input("What do you want to do? ")

    input_process(cmd)

    situation_process()
