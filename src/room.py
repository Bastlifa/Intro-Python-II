# Implement a class to hold room information. This should have name and
# description attributes.

from item import Item

secret = {
    'plate': ("""Looking under a broken table, you find an old suit of plate armor!""",
    Item("Plate", """Steel, interlocking plates, make for a heavy, 
if effective defensive suit of armor"""))
}

class Room:
    def __init__(self, name, description, lit, monster = None):
        self.name = name
        self.description = description
        self.items = []
        self.lit = lit
        self.monster = monster
    
    def remove_item(self, item):
        self.items.remove(item)

class Room_Secret(Room):
    def __init__(self, name, description, lit, secret, monster = None):
        super().__init__(name, description, lit, monster)
        self.secret = secret


