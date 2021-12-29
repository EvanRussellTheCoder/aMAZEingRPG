import random
import numpy as np


class RandomEngine:
    """
    Class to handle all random generation. Will be initialized by the game driver
    """

    def __init__(self):
        pass

    # takes a list (monster type, merchant type, etc) and returns a random element from the list
    def getRandom(self, list):
        the_choice = random.choice(list)
        return str(the_choice)

