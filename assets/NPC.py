from randomEngine import RandomEngine


class NPC(RandomEngine):
    """
    NPC class to store NPCs and their attributes
    """

    # Add merchants here
    MERCHANT_TYPE = ["blacksmith", "alchemist", "priest", "wizard"]

    def __init__(self):
        """
        Default NPC constructor. Generates choices and stats
        :param name: a string with the NPC name
        """

        # initialize random engine functions
        super().__init__()

        # NPC attributes
        self.name = None
        self.choices = None

        # get a random NPC
        self.name = self.getRandom(self.MERCHANT_TYPE)

        # create the NPC
        self.create_NPC(self.name)


    def create_NPC(self, name):
        if name == "alchemist":
            self.name = name

        if name == "blacksmith":
            self.name = name

        if name == "priest":
            self.name = name

        if name == "wizard":
            self.name = name
