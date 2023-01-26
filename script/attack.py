import pygame

from player import Player
from main import Game

class Attack(pygame.sprite.Sprite):
    # initializing
    def __init__(self, group, CLASS: str, DMG: int):
        super().__init__(group)

        Attack.CLASS = CLASS
        Attack.DMG = DMG

        Attack.spritePath = Game.path("sprites", "attack")
        Attack.right = "attackRight.png"
        Attack.left = "attackLeft.png"
        Attack.firingLeft = False
        Attack.firingRight = False
        Attack.space = False
        Attack.xRight = Player.rect.center[0] + 48
        Attack.yRight = Player.rect.center[1] + 14
        Attack.xLeft = Player.rect.center[0] - 48
        Attack.yLeft = Player.rect.center[1] + 14
        Attack.posRight = (Attack.xRight, Attack.yRight)
        Attack.posLeft = (Attack.xLeft, Attack.yLeft)

        Attack.image = pygame.image.load(Attack.spritePath + Attack.right).convert_alpha()
        Attack.rect = Attack.image.get_rect(center=Attack.posRight)

    # positioning the attack and set the attack key
    def input(self):
        self.keys = pygame.key.get_pressed()
        Attack.xRight = Player.rect.center[0] + 48
        Attack.yRight = Player.rect.center[1] + 14
        Attack.xLeft = Player.rect.center[0] - 48
        Attack.yLeft = Player.rect.center[1] + 14
        Attack.posRight = (Attack.xRight, Attack.yRight)
        Attack.posLeft = (Attack.xLeft, Attack.yLeft)

        if self.keys[pygame.K_SPACE]:
            Attack.space = True
            if Player.facingLeft == True:
                Attack.image = pygame.image.load(Attack.spritePath + Attack.left).convert_alpha()
                Attack.rect = Attack.image.get_rect(center=Attack.posLeft)
            elif Player.facingRight == True:
                Attack.image = pygame.image.load(Attack.spritePath + Attack.right).convert_alpha()
                Attack.rect = Attack.image.get_rect(center=Attack.posRight)
        else:
            Attack.space = False