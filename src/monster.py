import random

class Monster:
    def __init__(self, name, description, hp, attack, vuln):
        self.name = name
        self.description = description
        self.hp = hp
        self.attack = attack
        self.vuln = vuln

monster = {
    'rat': Monster("Rat", "A small furry mammal squeaks before attacking!",
    4, (30, 4), None),
    'skeleton': Monster("Skeleton", """Bones clatter against each other as
this nightmarish creature lurches at you with sharp claws""",
    12, (40, 12), "Bludgeon"),
    'troll': Monster("Troll", """This grotesque creature lumbers aggressively
towards you, wielding a massive club""", 50, (50, 16), "Fire"),
    'minotaur': Monster("Minotaur", """With the head of a bull, and a powerful torso,
this beastial humanoid is a terror to behold. The gleaming, 
double-headed axe in his massive arms could fell the mightiest tree""",
    70, (60, 22), None)
}