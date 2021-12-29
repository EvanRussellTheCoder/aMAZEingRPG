from randomEngine import RandomEngine


class Character(RandomEngine):
    # Game Character Mechanics
    _MAX_HEALTH = 100

    # Default base character stats
    _DEFAULT_STRENGTH = 10
    _DEFAULT_HEALTH = 100
    _DEFAULT_STAMINA = 20
    _DEFAULT_RESISTANCE = 3
    _DEFAULT_MAGIC = 1
    _DEFAULT_SPEED = 1
    _DEFAULT_INVENTORY = 50
    _DEFAULT_KARMA = 25

    MONSTER_TYPE = ["archer", "bandit"]

    # Default constructor, type is 0 or 1, 0 for player 1 for monster
    def __init__(self, type_, name, attack, resist, weakness):
        super().__init__()
        self._type = type_
        self._name = name
        self._imageSource = None
        self._strength = attack
        self._health = self._DEFAULT_HEALTH
        self._stamina = self._DEFAULT_STAMINA
        self._resistance = resist
        self._weakness = weakness
        self._magic = self._DEFAULT_MAGIC
        self._speed = self._DEFAULT_SPEED
        self._karma = self._DEFAULT_KARMA
        self._state = 1
        self.inventory = []
        self.equipped = []
        self.direction = 2
        self.x_location = 0
        self.y_location = 0

        if self._type == 1:
            self.create_monster()

        if self._type == 0:
            self.create_player()

    # Functions give / take health may find their way into the combat class
    def take_health(self, amount) -> int:
        self._health = self._health - amount
        if self._health < 0:
            self._health = 0
            self._state = 0
        # Return if character is dead or alive
        return self._state

    def give_health(self, amount):
        self._health = self._health + amount
        # Prevents characters health from going over max health
        if self._health > self._MAX_HEALTH:
            self._health = self._MAX_HEALTH

    def edit_karma(self, amount):
        self._karma += amount
        if self._karma > 50:
            self._karma = 50
        elif self._karma < 0:
            self._karma = 0

    def create_monster(self):
        self._name = self.getRandom(self.MONSTER_TYPE)

        if self._name == "archer":
            self._weakness = "Slash"
            self._imagePath = r'assets/enemies/Archer'
            self.idleImage = r'assets/enemies/Archer' + '/attack_3.png'

        if self._name == "bandit":
            self._weakness = "Stab"
            self._imagePath = r'assets/enemies/Bandit'
            self.idleImage = r'assets/enemies/Bandit' + '/run_2.png'


    def create_player(self):
        pass
