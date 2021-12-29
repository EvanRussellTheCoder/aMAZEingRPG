from randomEngine import RandomEngine


class Item(RandomEngine):
    """
    Item class to store game items and their stats, as well as their graphical positions on a sprite sheet.
    It inherits the random generation methods of the RandomEngine class.
    """

    # Below are the item types which can be chosen. Each type must be uniquely initialized in the create_item() method
    ITEM_TYPE_WEAPON = ["sword", "dagger", "staff", "club"]
    ITEM_TYPE_WEARABLE = ["iron chest plate", "iron boots", "iron helmet", "magic cloak", "leather cloak"]
    ITEM_TYPE_USABLE = ["small health flask", "large health potion", "eggplant"]

    # These are not item types. They are the rarity of the item, to be probabilistically assigned to the item determined
    # by character stats.
    ITEM_RARITIES = ["common", "uncommon", "rare"]

    def __init__(self, NPC):
        """
        Default constructor for an item

        :param NPC: the kind of NPC the item will be associated with
        :param initialize: a boolean to initialize the item after its been constructed
        """

        # initialize random generation methods
        super().__init__()

        # initialize item attributes
        self.type = None    # can be weapon, usable, or wearable
        self.name = None    # the item name. Ex: "dagger"
        self.rarity = None
        self.damage = None
        self.speed = None
        self.armor = None
        self.healing = None
        self.position = None    # A tuple of the items location on a spread sheet
        self.pos_x = None   # The items x placement on the spreadsheet
        self.pos_y = None   # The items y placement on the spreadsheet
        self._dmgType = None

        # image path - the path to the spread sheet with the item graphics. Same for each item unless specified
        # in the create_item() method
        self.img_path = r"assets/items/"
        self.img_file = self.img_path + "transparentIcons.png"


        # we want the item to make sense with whome is owning, and potentially offering it to us
        # a priest should not give a weapon
        # a blacksmith should not give a usable
        if NPC == "alchemist" or NPC == "priest":
            # these only give usables
            # getRandom is a method of the RandomEngine class, and returns an element of a list using a random choice
            self.item = self.getRandom(self.ITEM_TYPE_USABLE)
        elif NPC == "blacksmith":
            # blacksmith could give weapon or wearable, so join lists
            tempList = self.ITEM_TYPE_WEAPON + self.ITEM_TYPE_WEARABLE
            self.item = self.getRandom(tempList)
        elif NPC == "monster":
            self.item = self.getRandom(self.ITEM_TYPE_WEAPON)
        else:
            # if any other NPC is given, including None, then pick from a master list (can be any item)
            tempList = self.ITEM_TYPE_WEAPON + self.ITEM_TYPE_WEARABLE + self.ITEM_TYPE_USABLE
            self.item = self.getRandom(tempList)

        # if intitialize, fill the chosen item with the corresponding attributes

        self.createItem(self.item)


    def createItem(self, name) -> bool:
        """
        Function to take a randomly selected string representing the items name, and initialize
         it with the correct stats. If the item is not implemented, a not implemented error exception is raised

        :param name: The name of the item
        :return: true if the item was initialized.
        """

        # Weapons
        if name == "dagger":
            self.type = "weapon"
            self.name = name
            self._dmgType = "Stab"
            self.damage = 75
            self.speed = 100
            self.img_file = self.img_path + "transparentIcons.png"
            self.pos_x = 6
            self.pos_y = 5
            self.position = (self.pos_x*32, self.pos_y*32, 32, 32)
        if name == "sword":
            self.type = "weapon"
            self._dmgType = "Slash"
            self.name = name
            self.damage = 100
            self.speed = 75
            self.img_file = self.img_path + "transparentIcons.png"
            self.pos_x = 2
            self.pos_y = 5
            self.position = (self.pos_x * 32, self.pos_y * 32, 32, 32)
        if name == "club":
            self.type = "weapon"
            self._dmgType = "Blunt"
            self.name = name
            self.damage = 125
            self.speed = 50
            self.img_file = self.img_path + "transparentIcons.png"
            self.pos_x = 13
            self.pos_y = 5
            self.position = (self.pos_x * 32, self.pos_y * 32, 32, 32)
        if name == "staff":
            self.type = "weapon"
            self._dmgType = "Blunt"
            self.name = name
            self.speed = 100
            self.damage = 100
            self.img_file = self.img_path + "transparentIcons.png"
            self.pos_x = 7
            self.pos_y = 6
            self.position = (self.pos_x * 32, self.pos_y * 32, 32, 32)

        # wearables
        if name == "iron chest plate":
            self.type = "wearable"
            self.name = name
            self.armor = 50
            self.img_file = self.img_path + "transparentIcons.png"
            self.pos_x = 5
            self.pos_y = 7
            self.position = (self.pos_x * 32, self.pos_y * 32, 32, 32)
        if name == "iron boots":
            self.type = "wearable"
            self.name = name
            self.armor = 50
            self.img_file = self.img_path + "transparentIcons.png"
            self.pos_x = 3
            self.pos_y = 8
            self.position = (self.pos_x * 32, self.pos_y * 32, 32, 32)
        if name == "iron helmet":
            self.type = "wearable"
            self.name = name
            self.armor = 50
            self.img_file = self.img_path + "transparentIcons.png"
            self.pos_x = 7
            self.pos_y = 3
            self.position = (self.pos_x * 32, self.pos_y * 32, 32, 32)
        if name == "magic cloak":
            self.type = "wearable"
            self.name = name
            self.armor = 50
            self.img_file = self.img_path + "transparentIcons.png"
            self.pos_x = 14
            self.pos_y = 7
            self.position = (self.pos_x * 32, self.pos_y * 32, 32, 32)
        if name == "leather cloak":
            self.type = "wearable"
            self.name = name
            self.armor = 50
            self.img_file = self.img_path + "transparentIcons.png"
            self.pos_x = 6
            self.pos_y = 7
            self.position = (self.pos_x * 32, self.pos_y * 32, 32, 32)

        # usables
        if name == "small health flask":
            self.type = "usable"
            self.name = name
            self.healing = 50
            self.img_file = self.img_path + "transparentIcons.png"
            self.pos_x = 12
            self.pos_y = 9
            self.position = (self.pos_x*32, self.pos_y*32, 32, 32)
        if name == "large health potion":
            self.type = "usable"
            self.name = name
            self.healing = 100
            self.img_file = self.img_path + "transparentIcons.png"
            self.pos_x = 0
            self.pos_y = 9
            self.position = (self.pos_x * 32, self.pos_y * 32, 32, 32)
        if name == "eggplant":
            self.type = "usable"
            self.name = name
            self.healing = 150
            self.img_file = self.img_path + "transparentIcons.png"
            self.pos_x = 10
            self.pos_y = 14
            self.position = (self.pos_x*32, self.pos_y*32, 32, 32)

        # if the name of the item object is still none, then the item selected is not
        # included above and has no stats initialized
        if self.name is None:
            raise NotImplementedError

        else:
            return True


    def upgrade_damage(self, multiplier):
        """
        Function to upgrade the damage of a weapon

        :param multiplier: How much additional damage will be added
        """

        # make sure the multiplier can only yield a positive increase
        if multiplier <= 0:
            raise ValueError("Multiplier must be greater than 0")

        # make sure the item has the correct attribute applied (speed)
        if self.type != "weapon":
            raise TypeError("The item type must be a weapon")

        self.damage += self.damage * multiplier

    def upgrade_speed(self, multiplier):
        """
        Function to upgrade the speed of a weapon

        :param multiplier: How much additional speed will be added
        """

        # make sure the multiplier can only yield a positive increase
        if multiplier <= 0:
            raise ValueError("Multiplier must be greater than 0")

        # make sure the item has the correct attribute applied (speed)
        if self.type != "weapon":
            raise TypeError("The item type must be a weapon")

        self.speed += self.speed * multiplier

    def upgrade_armor(self, multiplier):
        """
        Function to upgrade the armor of a wearable

        :param multiplier: How much additional armor will be added
        """

        # make sure the multiplier can only yield a positive increase
        if multiplier <= 0:
            raise ValueError("Multiplier must be greater than 0")

        # make sure the item is a wearable
        if self.type != "wearable":
            raise TypeError("The item must be a wearable")

        self.armor += self.armor * multiplier
