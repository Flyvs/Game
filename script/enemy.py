import pygame

from player import Player
from main import Game

class Enemy(pygame.sprite.Sprite):
    # initializing
    def __init__(self, group, POS: tuple, LVL: int, HP: int, PHYATK: int, MAGATK: int, PHYDEF: int, MAGDEF: int, SPEED: int, SPAWNED: bool, SPRITE: str):
        super().__init__(group)

        self.POS = POS
        self.LVL = LVL
        self.HP = HP
        self.PHYATK = PHYATK
        self.MAGATK = MAGATK
        self.PHYDEF = PHYDEF
        self.MAGDEF = MAGDEF
        self.SPEED = SPEED
        self.SPAWNED = SPAWNED
        self.SPRITE = SPRITE

        self.image = pygame.image.load(Game.enemyPath + self.SPRITE).convert_alpha()
        self.rect = self.image.get_rect(topleft=self.POS)

    # track position of player
    def findPlayer(self):
        direction = pygame.math.Vector2()
        speed = 0

        if Player.rect.center[0] > self.rect.center[0]:
            direction.x = speed
        elif Player.rect.center[0] < self.rect.center[0]:
            direction.x = -speed

        if Player.rect.center[1] > self.rect.center[1]:
            direction.y = speed
        elif Player.rect.center[1] < self.rect.center[1]:
            direction.y = -speed

        self.rect.center += direction

    # start battle
    def attackPlayer(self):
        if (self.player_enemy_collision()) and (Player.hit):
            Player.hit = False
            Game.run = "battle"