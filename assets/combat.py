import time
import pygame
from random import randint


# requires that you have the mouse position defined in your main loop as such:
# This code below generates "i" amount of buttons with their own corresponding functionalities

class button:

    def __init__(self, x, y, text, screen, smallfont, item, index):
        self.item = item
        self.index = index
        self.smallfont = smallfont
        self._x = x
        self._y = y
        self.screen = screen
        self._imgSrc = r'assets/buttons/buttonSprite.png'
        buttonSprite = pygame.image.load(self._imgSrc)
        textObject = self.smallfont.render(text, False, (255, 255, 255))
        self.width = buttonSprite.get_width()
        self.height = buttonSprite.get_height()
        self.screen.blit(buttonSprite, (x, y))
        self.screen.blit(textObject, ((x + self.width / 4), (y + self.height / 4)))

    def clicked(self, mouse, event):
        if (mouse[0] >= self._x and mouse[0] <= self._x + self.width and mouse[1] >= self._y and mouse[
            1] <= self._y + self.height and event.type == pygame.MOUSEBUTTONUP):
            return True
        else:

            return False


class Combat:
    width = 1280
    height = 720

    def __init__(self, player, enemy, screen, font):
        self.smallfont = font
        self.screen = screen
        self._player = player
        self._enemy = enemy

    def playerAttack(self, item):

        if item is None:
            damage = self._player._strength
        else:
            damage = self._player._strength

            if (self._enemy._weakness == item._dmgType):
                damage += (item.damage * 2)
            elif (self._enemy._resistance == item._dmgType):
                damage += (int(item.damage * 0.65))
            else:
                damage += item.damage

        self._enemy.take_health(damage)

        damageTextObject = self.smallfont.render("-" + str(damage), False, (250, 100, 100))
        self.screen.blit(damageTextObject, (self.width / 2 + 100, self.height / 2 - 150))

        pygame.draw.rect(self.screen, (0, 0, 0), [80, self.height - 100, 140, 40])
        print(self._enemy._name, "takes", damage, "damage....", self._enemy._health, "remaining.")
        return

    def enemyAttack(self):
        if (self._enemy._health > 0):
            damage = self._enemy._strength + randint(1, 20)
            damage = damage - self._player._resistance
            if damage <= 0:
                damage = 0
            self._player.take_health(damage)
            damageTextObject = self.smallfont.render("-" + str(damage), False, (250, 100, 100))
            self.screen.blit(damageTextObject, (80, self.height - 100))
            pygame.draw.rect(self.screen, (0, 0, 0), [80, self.height - 50, 140, 40])

            print("You take", damage, "damage....", self._player._health, "remaining.")
        pygame.draw.rect(self.screen, (0, 0, 0), [self.width / 2 + 10, self.height / 2 - 150, 140, 40])
        return

    def displayCombatUI(self, mouse, event):

        attackButtons = []
        haveWeapon = False

        for i in range(len(self._player.equipped)):
            if self._player.equipped[i].item.type == "weapon":
                haveWeapon = True

        if len(self._player.equipped) == 0 or haveWeapon == False:
            itemButton = button(self.width / 2 - 450, self.height / 2 + (1 * 50),
                                "punch", self.screen, self.smallfont, None, None)
            attackButtons.append(itemButton)

        for i in range(len(self._player.equipped)):
            if self._player.equipped[i].item.type == "weapon" or self._player.equipped[i].item.type == "usable":
                itemButton = button(self.width / 2 - 450, self.height / 2 + (i * 50),
                                    self._player.equipped[i].item.name, self.screen, self.smallfont, self._player.equipped[i].item, i)
                attackButtons.append(itemButton)

        for x in range(len(attackButtons)):
            if attackButtons[x].clicked(mouse, event):
                # for punch
                if len(self._player.equipped) == 0 or haveWeapon == False:
                    # sorry Doc
                    try:
                        if attackButtons[x].item.type == "usable":
                            self._player.give_health(attackButtons[x].item.healing)
                            del(self._player.equipped[attackButtons[x].index])
                    except:
                        self.playerAttack(None)
                        time.sleep(2)
                        self.enemyAttack()
                else:
                    self.playerAttack(attackButtons[x].item)
                    time.sleep(2)
                    self.enemyAttack()

        if self._enemy._health == 0:
            print("You are victorious! The", self._enemy._name, "has been defeated!")
            return False

        enemyImg = pygame.image.load(self._enemy.idleImage)
        enemyImg = pygame.transform.scale(enemyImg, (250, 250))
        playerHPString = str(self._player._health)
        enemyHPString = str(self._enemy._health)

        playerHP = self.smallfont.render(playerHPString, False, (255, 255, 255))
        enemyHP = self.smallfont.render(enemyHPString, False, (255, 255, 255))
        HPText = self.smallfont.render("HP: ", False, (255, 255, 255))
        self.screen.blit(HPText, (20, self.height - 50))
        self.screen.blit(enemyImg, (self.width / 2 - 100, self.height / 2 - 90))
        self.screen.blit(HPText, (self.width / 2 - 50, self.height / 2 - 150))
        self.screen.blit(enemyHP, (self.width / 2 + 10, self.height / 2 - 150))
        self.screen.blit(playerHP, (80, self.height - 50))

        return True

# Testing
# jeff = Character(0, "Jeff", 0, "", 20, 10)
# skeleton = Character(1, "Demon", 0, "testEnemy.png", 30, 5)
# combatTest = combat(jeff, skeleton)

# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#             pygame.quit()
# 
#         mouse = pygame.mouse.get_pos()  # gets x/y of mouse
#         ev = pygame.event.get()
#         combatTest.displayCombatUI()
#         pygame.display.flip()  # clears the canvas for new graphics.
#         pygame.display.update()  # runs every frame constantly updating graphics
