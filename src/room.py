# Implement a class to hold room information. This should have name and
# description attributes.

class Room:
    def __init__(self, name, description, lit):
        self.name = name
        self.description = description
        self.items = []
        self.lit = lit
    
    def remove_item(self, item):
        self.items.remove(item)

class Room_Secret(Room):
    def __init__(self, name, description, lit, secret):
        super().__init__(name, description, lit)
        self.secret = secret
    