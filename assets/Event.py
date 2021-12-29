import enum
from NPC import NPC
from items import Item
from Character import Character
import numpy as np
from randomEngine import RandomEngine


class EventType(enum.Enum):
    combat = 0
    friendly = 1
    item = 2
    end = 3


def is_plural(string) -> bool:
    if string[len(string) - 1:] == 's':
        return True
    else:
        return False


class Event(RandomEngine):
    # here lies all possible events
    # event types: Combat, friendly, item, trap
    # item events are simple, two choices, take the random item or leave the random item
    # trap event is a booby trap. Player would get choices -> Jump, flee, duck, stand still

    """
    NPC types below will have to be initialized as characters in the character class with stats
    """

    def __init__(self, event_type):
        # initialize random event generator super class
        super().__init__()
        self.enemy = None
        self._item = None
        self._type = event_type

        # Event is combat
        if self._type == EventType.combat:
            self.choices = ["fight", "flee"]
            self.generate_combat_event()

        # Event is friendly
        elif self._type == EventType.friendly:
            self.choices = ["kill", "walk away", "talk to", "trade"]
            self.generate_friendly_event()

        # Event is item
        elif self._type == EventType.item:
            # item event choices
            self.choices = ["take", "leave"]
            self.generate_item_event()

    # generate a random combat event
    def generate_combat_event(self):
        # generate a random combat event, with monsters, items, and choices
        self.enemy = Character(1, None, 0, 30, 5)
        self._item = Item('blacksmith')

    # generate a random friendly event
    def generate_friendly_event(self):
        # concatenate a random friendly event, with merchants, items, and choices
        self._NPC = NPC()
        print(self._NPC.name)
        self._item = Item(self._NPC.name)

    # generate a item event
    def generate_item_event(self):
        # concatenates a random item event
        self._item = Item(None)

    # prompts an event
    def promptEvent(self):
        """ Concatenates a string containing the event prompt
        :return strings -> The event prompt """
        prompts = []
        # For friendly events
        if self._type == EventType.friendly:
            if is_plural(self._item.name):
                prompts.append(
                    "You walk into a room, and meet a " + str(self._NPC.name) + " with " + str(self._item.name))
            else:
                prompts.append(
                    "You walk into a room, and meet a " + str(self._NPC.name) + " with a " + str(self._item.name))


        # For item event
        if self._type == EventType.item:
            prompts.append(
                "As you enter the room, a large stone chest rumbles up from the ground. Curious, you tip off the lid"
                " and peer inside.")
            if is_plural(self._item.name):
                prompts.append(f"You found {self._item.name}!")
            else:
                prompts.append(f"You found a {self._item.name}!")


        # for combat event
        if self._type == EventType.combat:
            prompts.append("You walk into the next room, and meet a " + str(self.enemy._name) + " with a " + self._item.name)

        prompts.append("Your choices are:")

        return prompts

    # get choices
    def get_choices(self):
        return self.choices

    # handle choices
    def handle_choice(self, player, choice, item):

        isCombat = False

        if choice == "fight":
            isCombat = True

        # player chose to walk away
        if choice == "walk away":
            self.flee(player)

        # player chose to kill the NPC
        if choice == "kill":
            print(f"You slay the poor {self._NPC.name}.")
            if bool(np.random.binomial(1, round(player._karma / 100, 2))):
                if is_plural(self._item.name):
                    print(f"You are granted {self._item.name}")
                else:
                    print(f"You are granted a {self._item.name}")
            self.change_karma(-10, player)

        # player chose to talk to the NPC
        if choice == "trade":
            # show the NPC's inventory
            player.edit_karma(10)

        # player chose to take the item
        if choice == "take":
            if len(player.inventory) < 12:
                print(f"You lift the {self._item.name} from the cobwebs, and place it in your bag.")
                player.inventory.append(item)

        # player chose to leave the item
        if choice == "leave":
            print(f"The {self._item.name} shows ware and abuse. Perhaps it is better to let it be forgotten.")

        return isCombat

    # call on fight class
    def start_fight(self):
        # call start_fight method and pass it the monster object
        pass

    # method to take health from a character
    def takeHealth(self):
        pass

    # method to get an item
    def get_item(self, player):
        pass

    # method to lose an item
    def lose_item(self):
        pass

    # method to flee
    def flee(self, player):
        if self._type == EventType.friendly:
            print(f"You leave the {self._NPC.name} in the dust.")
        if self._type == EventType.combat:
            # if the difference between the player level and the monster level is >= 4, the player is guarenteed a
            # flee. The formula is abs(player level - monster level) * 0.25. If the answer is 0, 25% chance to flee
            probablity = 0
            pass

    # method to initiate a trade
    def trade(self):
        pass

    # method to change karma
    def change_karma(self, amount, character):
        character.edit_karma(amount)

    # method to check if item is plural

# myPlayer = Character(0, None, None)
#
# for i in range(5):
#     myEvent = Event(EventType.item)
#     myEvent.promptEvent()
# # handle choices
#     myEvent.handle_choice(myPlayer)
#     print(myPlayer._inventory)
#     print(myPlayer._inventory[i].name)
