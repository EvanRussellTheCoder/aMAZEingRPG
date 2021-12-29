########################################################################################################################
##############################              aMAZEing RPG            ####################################################
##############################              CSC305 S21J             ####################################################
########################################################################################################################

import enum  # for enumerating the game play state and other features
import time
import random
import pygame  # for driving the game
import sys

from Character import Character  # to generate a character
from Event import Event, EventType  # to generate events
from items import Item  # to generate items
from maze import Maze  # to generate the maze
from combat import Combat


class GameState(enum.Enum):
    """ Emulates enumeration functionality from other language
        Add game-play states as needed
    """
    start_screen = 0
    in_room = 1
    choices = 2
    leave_room = 3
    combat = 4


class Compass(enum.Enum):
    """ Emulates enumeration functionality from other languages
        Used to keep track of player direction in the maze"""
    north = 0
    east = 1
    south = 2
    west = 3


class InventoryItem:
    """ Contains the functions to create a list of inventory items"""

    INDEX_TO_DISPLAY = 0

    def __init__(self, item):
        self.item = item
        self.itemSRC = pygame.image.load(self.item.img_file)
        self.itemFrame = self.item.position
        self.itemImage = None
        self.itemFramePosition = None
        self.itemButtonSurf = pygame.Surface((50, 50), pygame.SRCALPHA, 32)
        self.itemButton = None
        self.index = None
        self.equipped = False

    def update_positions(self):
        self.itemFramePosition = (285 + (self.index * 60), 135)


class Choice:
    """ Contains the functions to create a list of choices """

    BLACK = (0, 0, 0)
    BUTTON_RED = (150, 10, 10)

    def __init__(self, choice, font):
        self.choice = choice
        self.promptSurf = font.render(choice, True, self.BLACK)
        self.promptDime = self.promptSurf.get_size()
        self.promptButtonSurf = pygame.Surface(self.promptDime)
        self.promptButtonSurf.fill(self.BUTTON_RED)
        self.promptButton = None


class Engine:
    """ The game engine class
    This class manages all the graphics and states of the game
    """

    # Initialize pygame
    pygame.init()
    clock = pygame.time.Clock()

    # Title and icon
    icon = pygame.image.load(r'images/dungeon.png')
    pygame.display.set_caption("Random RPG")
    pygame.display.set_icon(icon)

    # Sprite Sheet
    sheet = pygame.image.load(r'images/sword_sheet.png')

    # Room graphics
    roomGraphic = pygame.image.load(r'images/room_base.png')
    backDoor = pygame.image.load(r'images/back_door.png')
    leftDoor = pygame.image.load(r'images/left_door.png')
    rightDoor = pygame.image.load(r'images/right_door.png')

    # Fonts
    mainFontBig = pygame.font.SysFont('Calibri', 48)
    mainFontMedium = pygame.font.SysFont('Calibri', 32)
    mainFontSmall = pygame.font.SysFont('Calibri', 18)

    # Create the player
    myPlayer = Character(0, "Jeff", 10, 1, None)

    # Useful constants
    topLeft = (0, 0)
    width = 1280
    height = 720
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BUTTON_RED = (150, 10, 10)

    def __init__(self):
        """ Default constructor for the game"""
        # create the play space
        self.screen = pygame.display.set_mode((self.width, self.height))

        # create the maze
        self.maze = Maze(6, 6)
        # run twice to make maze more complex
        self.maze.randomGenerate()
        self.maze.randomGenerate()
        self.rooms = self.maze.grid_cells

        # Inventory image
        self.inventoryBar = pygame.image.load(r'images/inventory_bar.png')
        self.inventoryDime = (self.inventoryBar.get_width(), self.inventoryBar.get_height())

        # Assign default item
        anItem = Item(None)
        anItem.createItem("dagger")
        newInventoryItem = InventoryItem(anItem)
        newInventoryItem.index = len(self.myPlayer.inventory)
        newInventoryItem.itemImage = self.image_at(newInventoryItem.itemFrame, newInventoryItem.itemSRC)
        newInventoryItem.update_positions()
        self.myPlayer.inventory.append(newInventoryItem)

        # Gameplay logic - conditionals for game-play loop - will end up being a state machine
        self.gameState = GameState.start_screen  # start the game state at the start screen
        self.inventoryState = False
        self.newRoom = False
        self.doorDirections = None  # a list of door directions for each wall in the room.
        self.event = None
        self.choices = []
        self.currentItem = None

        # Buttons
        self.startButton = None
        ### For doors
        self.forwardButton = None
        self.leftButton = None
        self.rightButton = None
        self.backButton = None
        self.equipButton = None
        self.dropButton = None

        # fader graphics
        self.fader = pygame.Surface((self.width, self.height))
        self.faderAlpha = 0
        self.fader.set_alpha(self.faderAlpha)
        self.fadeState = False

    def run_game(self):
        """ The main game loop, cascade events here"""
        while True:
            # always check events
            for event in pygame.event.get():
                # Game X button is pressed, quit
                if event.type == pygame.QUIT:
                    sys.exit()

                # Mouse button clicked.. Do we care?
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Game is in start screen state. Was the start game button clicked?
                    pos = pygame.mouse.get_pos()
                    if self.gameState == GameState.start_screen:
                        if self.start_button.collidepoint(pos):
                            self.newRoom = True
                            self.gameState = GameState.in_room
                    # Player is in a room and choices have been prompted, which was picked?
                    elif self.gameState == GameState.choices:
                        pass
                    # Player is ready to leave the room
                    elif self.gameState == GameState.leave_room:
                        # Is the button for the door there?
                        doorClicked = False
                        if self.forwardButton:
                            if self.forwardButton.collidepoint(pos):
                                print("Going straight!")
                                self.change_direction(0)
                                doorClicked = True
                        if self.rightButton:
                            if self.rightButton.collidepoint(pos):
                                print("Turning right!")
                                self.change_direction(1)
                                doorClicked = True
                        if self.backButton:
                            if self.backButton.collidepoint(pos):
                                print("Going back!")
                                self.change_direction(2)
                                doorClicked = True
                        if self.leftButton:
                            if self.leftButton.collidepoint(pos):
                                print("Going left!")
                                self.change_direction(3)
                                doorClicked = True

                        # A door was clicked, create the next room
                        if doorClicked:
                            self.inventoryState = False
                            self.newRoom = True

                    # Player is making choices
                    elif self.gameState == GameState.in_room:
                        for choice in self.choices:
                            if choice.promptButton.collidepoint(pos):
                                print(f"Choice {choice.choice} clicked at {pos}")
                                isCombat = self.event.handle_choice(self.myPlayer, choice.choice, self.currentItem)
                                if isCombat:
                                    self.combatObject = Combat(self.myPlayer, self.event.enemy, self.screen, self.mainFontSmall)
                                    self.screen.fill(self.BLACK)
                                    self.inventoryState = False
                                    self.gameState = GameState.combat
                                else:
                                    self.gameState = GameState.leave_room

                    # Game has inventory state
                    if self.inventoryState:
                        # clicked on an item?
                        for item in self.myPlayer.inventory:
                            if item.itemButton is not None:
                                if item.itemButton.collidepoint(pos):
                                    print(f"Item {item.index} is a {item.item.name}, clicked at {pos}")
                                    InventoryItem.INDEX_TO_DISPLAY = item.index

                        # clicked on equip button?
                        if self.gameState != GameState.combat:
                            if self.equipButton.collidepoint(pos):
                                self.myPlayer.inventory[InventoryItem.INDEX_TO_DISPLAY].equipped = not self.myPlayer.inventory[InventoryItem.INDEX_TO_DISPLAY].equipped
                                if len(self.myPlayer.equipped) < 4 and self.myPlayer.inventory[InventoryItem.INDEX_TO_DISPLAY].equipped:
                                    self.myPlayer.equipped.append(self.myPlayer.inventory[InventoryItem.INDEX_TO_DISPLAY])
                                    if self.myPlayer.inventory[InventoryItem.INDEX_TO_DISPLAY].item.type == "wearable":
                                        self.myPlayer._resistance += self.myPlayer.inventory[InventoryItem.INDEX_TO_DISPLAY].item.armor
                                    print(self.myPlayer.equipped)

                                if not self.myPlayer.inventory[InventoryItem.INDEX_TO_DISPLAY].equipped:
                                    for i in range(len(self.myPlayer.equipped)):
                                        if self.myPlayer.equipped[i] == self.myPlayer.inventory[InventoryItem.INDEX_TO_DISPLAY]:
                                            if self.myPlayer.inventory[InventoryItem.INDEX_TO_DISPLAY].item.type == "wearable":
                                                self.myPlayer._resistance -= self.myPlayer.inventory[InventoryItem.INDEX_TO_DISPLAY].item.armor
                                            del self.myPlayer.equipped[i]
                                            break

                                    print(self.myPlayer.equipped)
                                print("Clicked Equip")
                                print(self.myPlayer._resistance)

                        # clicked on drop button?
                        if self.dropButton.collidepoint(pos):
                            if len(self.myPlayer.inventory) > 1:
                                del(self.myPlayer.inventory[InventoryItem.INDEX_TO_DISPLAY])
                                # check if index to display is out of range
                                if InventoryItem.INDEX_TO_DISPLAY >= len(self.myPlayer.inventory):
                                    InventoryItem.INDEX_TO_DISPLAY = len(self.myPlayer.inventory) - 1
                            print("Clicked Drop")

                # Inventory button pressed
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_i:
                        if self.gameState != GameState.combat:
                            self.inventoryState = not self.inventoryState

            # start game-play conditionals here
            # game states for logic
            if self.newRoom:
                # set the event (attribute of a room)
                # testing combat
                alist = [EventType.item, EventType.combat]
                aEvent = random.choice(alist)
                self.event = Event(aEvent)
                self.get_new_room()
                self.gameState = GameState.in_room
                self.newRoom = False

            # game states for graphics
            # player is in start screen state, display start screen
            if self.gameState == GameState.start_screen:
                self.start_screen_state()
            # player is being prompted with a room event, display prompt
            elif self.gameState == GameState.in_room:
                self.draw_room()
                self.prompt_event_state()
                self.draw_event()
                self.prompt_choices_state()
                pass
            # player is being prompted with choices, display choices
            elif self.gameState == GameState.choices:
                pass
            # player is ready to leave the room, give options
            elif self.gameState == GameState.leave_room:
                self.draw_room()
                self.leave_room_state()
                pass
            # player is in a combat state
            elif self.gameState == GameState.combat:
                self.screen.fill(self.BLACK)
                fight = self.combatObject.displayCombatUI(pygame.mouse.get_pos(), event)
                if not fight:
                    self.gameState = GameState.leave_room

            # game is in inventory state, show the inventory
            if self.inventoryState:
                self.inventory_state()

            self.screen.blit(self.fader, self.topLeft)

            # always update the screen
            pygame.display.update()
            self.clock.tick(60)

    # the first state of the game
    def start_screen_state(self):
        """The start screen state is the first state of the game, where the player can press start game. """
        # Display room and all doors
        self.screen.blit(self.roomGraphic, self.topLeft)
        self.screen.blit(self.leftDoor, self.topLeft)
        self.screen.blit(self.backDoor, self.topLeft)
        self.screen.blit(self.rightDoor, self.topLeft)

        # Display start game button
        # Create button surface
        button_dime = (250, 100)
        start_game_button = pygame.Surface(button_dime)
        start_game_button.fill((150, 10, 10))

        # Create start game text
        start_game_text = self.mainFontBig.render("Start", 48, self.RED)
        start_game_text_rect = start_game_text.get_rect()
        text_dime = (start_game_text_rect.width, start_game_text_rect.height)  # Use to get text dimensions

        # Blit additions
        self.start_button = self.screen.blit(start_game_button, self.center_offset(button_dime, (0, 100)))
        self.screen.blit(start_game_text, self.center_offset(text_dime, (0, 100)))

    # game state where the event's prompt is shown on the screen
    def prompt_event_state(self):
        # generate choice prompt
        counter = 0
        if self.event._type == EventType.item:
            for text in self.event.promptEvent():
                # create a text box for each prompt
                promptSurf, promptRect = self.text_objects(text, self.mainFontSmall, self.WHITE)
                promptBG = pygame.Surface((promptRect.width, promptRect.height))
                promptBG.set_alpha(100)
                self.screen.blit(promptBG, (50, 500 + (counter * 25)))
                self.screen.blit(promptSurf, (50, 500 + (counter * 25)))
                counter += 1

        if self.event._type == EventType.combat:
            for text in self.event.promptEvent():
                # create a text box for each prompt
                promptSurf, promptRect = self.text_objects(text, self.mainFontSmall, self.WHITE)
                promptBG = pygame.Surface((promptRect.width, promptRect.height))
                promptBG.set_alpha(100)
                self.screen.blit(promptBG, (50, 200 + (counter * 25)))
                self.screen.blit(promptSurf, (50, 200 + (counter * 25)))
                counter += 1

    def prompt_choices_state(self):
        # fill choice button array
        counter = 0
        for choice in self.choices:
            choice.promptButton = self.screen.blit(choice.promptButtonSurf,
                                                   self.center_offset(choice.promptDime, (200, -250 - (counter * 25))))
            self.screen.blit(choice.promptSurf, self.center_offset(choice.promptDime, (200, -250 - (counter * 25))))
            counter += 1

    def draw_event(self):
        if self.event._type == EventType.item:
            currentItemImageCopy = self.currentItem.itemImage
            currentItemImageCopy = pygame.transform.scale(currentItemImageCopy, (100, 100))
            self.screen.blit(currentItemImageCopy, self.center_offset((100, 100), (0, -250)))

        if self.event._type == EventType.combat:
            monsterImagePath = self.event.enemy.idleImage
            monsterImage = pygame.image.load(monsterImagePath)
            monsterImage = pygame.transform.scale(monsterImage, (250, 250))
            self.screen.blit(monsterImage, self.center_offset((250, 250), (0, -150)))

    # a game state
    def leave_room_state(self):
        """ Display the door buttons for the player to leave"""

        # Create buttons
        button_dime = (150, 50)
        forward_button = pygame.Surface(button_dime)
        forward_button.fill((150, 10, 10))
        right_button = pygame.Surface(button_dime)
        right_button.fill((150, 10, 10))
        back_button = pygame.Surface(button_dime)
        back_button.fill((150, 10, 10))
        left_button = pygame.Surface(button_dime)
        left_button.fill((150, 10, 10))

        # Create text
        textList = []
        textList.append(self.text_objects("North", self.mainFontMedium, self.BLACK))
        textList.append(self.text_objects("East", self.mainFontMedium, self.BLACK))
        textList.append(self.text_objects("South", self.mainFontMedium, self.BLACK))
        textList.append(self.text_objects("West", self.mainFontMedium, self.BLACK))

        # spacing between buttons
        spacing = 20

        # blit additions
        # forward button
        if self.Doors[self.doorDirections[0]]:
            self.forwardButton = self.screen.blit(forward_button, self.center_offset(button_dime, (0, -220)))
            self.screen.blit(textList[self.doorDirections[0]][0], self.center_offset(
                (textList[self.doorDirections[0]][1].width, textList[self.doorDirections[0]][1].height), (0, -220)))
        else:
            self.forwardButton = None
        # right button
        if self.Doors[self.doorDirections[1]]:
            self.rightButton = self.screen.blit(right_button, self.center_offset(button_dime, (-160, -250)))
            self.screen.blit(textList[self.doorDirections[1]][0], self.center_offset(
                (textList[self.doorDirections[1]][1].width, textList[self.doorDirections[0]][1].height), (-160, -250)))
        else:
            self.rightButton = None
        # back button
        if self.Doors[self.doorDirections[2]]:
            self.backButton = self.screen.blit(back_button, self.center_offset(button_dime, (0, -280)))
            self.screen.blit(textList[self.doorDirections[2]][0], self.center_offset(
                (textList[self.doorDirections[2]][1].width, textList[self.doorDirections[0]][1].height), (0, -280)))
        else:
            self.backButton = None
        # left button
        if self.Doors[self.doorDirections[3]]:
            self.leftButton = self.screen.blit(left_button, self.center_offset(button_dime, (160, -250)))
            self.screen.blit(textList[self.doorDirections[3]][0], self.center_offset(
                (textList[self.doorDirections[3]][1].width, textList[self.doorDirections[0]][1].height), (160, -250)))
        else:
            self.leftButton = None

    # game state where inventory is showing
    def inventory_state(self):
        """
        Displays the inventory on screen
        :return:
        """

        # inventory bar
        self.screen.blit(self.inventoryBar, self.center_offset(self.inventoryDime, (0, 200)))

        # item info box
        infoBox = pygame.Surface((200, 70))
        infoBox.fill((153, 153, 153))

        # item name text
        itemInfoToDisplay = self.myPlayer.inventory[InventoryItem.INDEX_TO_DISPLAY]
        itemNameInfoText = self.text_object("Name: " + itemInfoToDisplay.item.name, self.mainFontSmall, self.BLACK)
        textHeight = itemNameInfoText.get_height()
        infoBox.blit(itemNameInfoText, (0, 0))
        # item attributes text
        attributes = []
        # if weapon get damage and speed
        if self.myPlayer.inventory[InventoryItem.INDEX_TO_DISPLAY].item.type == "weapon":
            attributes.append(
                self.text_object("Damage: " + str(itemInfoToDisplay.item.damage), self.mainFontSmall, self.BLACK))
            attributes.append(
                self.text_object("Speed: " + str(itemInfoToDisplay.item.speed), self.mainFontSmall, self.BLACK))
        # if wearable get armor
        if self.myPlayer.inventory[InventoryItem.INDEX_TO_DISPLAY].item.type == "wearable":
            attributes.append(
                self.text_object("Armor: " + str(itemInfoToDisplay.item.armor), self.mainFontSmall, self.BLACK))
        # if usable get healing
        if self.myPlayer.inventory[InventoryItem.INDEX_TO_DISPLAY].item.type == "usable":
            attributes.append(
                self.text_object("Healing: " + str(itemInfoToDisplay.item.healing), self.mainFontSmall, self.BLACK))

        # 1 because the item name is there by default
        spacer = 1
        for attribute in attributes:
            infoBox.blit(attribute, (0, spacer * textHeight))
            spacer += 1

        self.screen.blit(infoBox, self.center_offset((infoBox.get_width(), infoBox.get_height()), (0, 130)))

        # equip/unequip button
        equipButtonSurf = pygame.Surface((70, 30))
        equipButtonSurf.fill((3, 171, 37))
        # equip/unequip text
        if itemInfoToDisplay.equipped:
            equipText = self.text_object("Unequip", self.mainFontSmall, self.BLACK)
        else:
            equipText = self.text_object("Equip", self.mainFontSmall, self.BLACK)

        equipButtonSurf.blit(equipText, (0, 0))
        self.equipButton = self.screen.blit(equipButtonSurf, self.center_offset((equipButtonSurf.get_width(), equipButtonSurf.get_height())
                                                             , (-135, 145)))
        # drop button
        dropButtonSurf = pygame.Surface((70, 30))
        dropButtonSurf.fill(self.BUTTON_RED)
        dropText = self.text_object("Drop", self.mainFontSmall, self.BLACK)
        dropButtonSurf.blit(dropText, (0, 0))
        self.dropButton = self.screen.blit(dropButtonSurf, self.center_offset((equipButtonSurf.get_width(), equipButtonSurf.get_height())
                                                            , (-135, 115)))
        # items
        equipBar = pygame.Surface((45, 8))
        equipBar.fill((3, 171, 37))
        index = 0
        for item in self.myPlayer.inventory:
            item.index = index
            item.update_positions()
            self.screen.blit(item.itemImage, item.itemFramePosition)
            item.itemButton = self.screen.blit(item.itemButtonSurf, item.itemFramePosition)
            if item.equipped:
                self.screen.blit(equipBar, (287 + (item.index * 60), 186))
            index += 1

    # logic functions
    def change_direction(self, door):
        # update the players direction with the direction linked to the door they chose
        self.myPlayer.direction = self.doorDirections[door]

        # update the players coordinates
        # because no doors will ever exist where a player could go out of bounds, so there is no need to check.
        # we can if we want, im not going to do it now for sake of time

        if self.myPlayer.direction == 0:
            self.myPlayer.x_location -= 1
        elif self.myPlayer.direction == 1:
            self.myPlayer.y_location += 1
        elif self.myPlayer.direction == 2:
            self.myPlayer.x_location += 1
        else:
            self.myPlayer.y_location -= 1

    def draw_room(self):
        # Display room and correct doors
        self.screen.blit(self.roomGraphic, self.topLeft)

        # check if doors in each direction exist
        if self.Doors[self.doorDirections[0]]:
            self.screen.blit(self.backDoor, self.topLeft)
        if self.Doors[self.doorDirections[1]]:
            self.screen.blit(self.rightDoor, self.topLeft)
        if self.Doors[self.doorDirections[3]]:
            self.screen.blit(self.leftDoor, self.topLeft)

    def get_new_room(self):
        """ This function builds all members necessary in a room. IE, the doors, the event prompt, etc."""

        # Get the door directions of the room
        self.doorDirections = self.get_door_directions()

        # get the new event choices
        self.choices.clear()
        for choice in self.event.get_choices():
            self.choices.append(Choice(choice, self.mainFontSmall))

        # create the current item
        self.currentItem = InventoryItem(self.event._item)
        self.currentItem.index = len(self.myPlayer.inventory)
        self.currentItem.itemImage = self.image_at(self.currentItem.itemFrame, self.currentItem.itemSRC)
        self.currentItem.update_positions()

    def get_door_directions(self):
        direction = self.myPlayer.direction
        doorDirections = []

        # rooms is a 1d array representing a 2 dimensional space.
        # index with width * row + column
        self.Doors = self.rooms[self.maze.width * self.myPlayer.x_location + self.myPlayer.y_location].Doors
        print(f"in room ({self.myPlayer.y_location}, {self.myPlayer.x_location})")

        for i in range(4):
            # no turn, still looking straight
            if i == 0:
                forward = direction
                doorDirections.append(forward)
            if i == 1:
                right = direction
                doorDirections.append(right)
            if i == 2:
                behind = direction
                doorDirections.append(behind)
            if i == 3:
                left = direction
                doorDirections.append(left)
            # make a right turn. If direction is > 3 (west) youve returned to north (0)
            direction += 1
            if direction == 4:
                direction = 0

        return doorDirections

    def fade(self, direction, speed):
        fade = True
        pygame.image.save(self.screen, "temp.png")
        screenCPY = pygame.image.load("temp.png")
        while fade:
            for event in pygame.event.get():
                # Game X button is pressed, quit
                if event.type == pygame.QUIT:
                    sys.exit()
            self.screen.blit(screenCPY, (0, 0))
            self.fader.set_alpha(self.faderAlpha)
            self.screen.blit(self.fader, self.topLeft)
            if direction:
                if self.faderAlpha < 255:
                    self.faderAlpha += speed
                else:
                    fade = False
            else:
                if self.faderAlpha >= 0:
                    self.faderAlpha -= speed
                else:
                    fade = False

            pygame.display.update()

    # useful helper functions below
    def image_at(self, rectangle, src):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(src, (0, 0), rect)
        image = pygame.transform.scale(image, (50, 50))
        colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def center(self, xy):
        center = (1280 // 2 - xy[0] // 2, 720 // 2 - xy[1] // 2)
        return center

    def center_offset(self, xy, offset):
        center = self.center(xy)
        center_offset = (center[0] - offset[0], center[1] - offset[1])
        return center_offset

    def text_objects(self, text, font, color):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()

    def text_object(self, text, font, color):
        textSurface = font.render(text, True, color)
        return textSurface


# Run the game
if __name__ == "__main__":
    aMAZEingRPG = Engine()
    aMAZEingRPG.run_game()
