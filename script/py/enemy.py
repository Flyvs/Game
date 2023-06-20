import pygame
from typing import List

from attack import Attack

class Enemy(pygame.sprite.Sprite):
    def __init__(self,
                 group,
                 POS: tuple,
                 HP: int,
                 ATK: int,
                 DEF: int, 
                 SPEED: int, 
                 SPAWNED: bool, 
                 SPRITE: str,
                 LIST: list,
                 game, 
                 player):
        
        super().__init__(group)

        self.POS = POS
        self.HP = HP
        self.ATK = ATK
        self.DEF = DEF
        self.SPEED = SPEED
        self.SPAWNED = SPAWNED
        self.SPRITE = SPRITE
        self.LIST: List[Enemy] = LIST

        self.game = game
        self.player = player
        self.attack_list: List[Attack] = []
        self.current_attack: Attack

        self.image = pygame.image.load(self.game.enemy_path + self.SPRITE).convert_alpha()
        self.rect = self.image.get_rect(topleft=self.POS)

    def find_player(self):
        direction = pygame.math.Vector2()
        recenter = pygame.math.Vector2()

        recenter.y = self.rect.center[1]

        if self.player.rect.center[0] > self.rect.center[0]:
            direction.x = self.SPEED
        elif self.player.rect.center[0] < self.rect.center[0]:
            direction.x = -self.SPEED

        if self.player.rect.center[1] > self.rect.center[1]:
            direction.y = self.SPEED
        elif self.player.rect.center[1] < self.rect.center[1]:
            direction.y = -self.SPEED

        self.rect.center += direction

        if (self.player.rect.center[0] != self.rect.center[0]) or (self.player.rect.center[1] != self.rect.center[1]):
            if self.player.rect.center[0] < self.rect.center[0]:
                recenter.x = self.rect.center[0] - self.SPEED
            else:
                recenter.x = self.rect.center[0] + self.SPEED

            if self.player.rect.center[1] < self.rect.center[1]:
                recenter.y = self.rect.center[1] - self.SPEED
            else:
                recenter.y = self.rect.center[1] + self.SPEED

            self.rect.center = recenter
    
    def attack_player(self):
        if self.player.player_enemy_collision() and self.player.hit:
            self.player.hit = False

            if self.player.HP > 0:
                if self.SPAWNED:
                    self.player.HP -= self.ATK
            elif self.player.HP < 0:
                self.player.HP = 0

    def hit(self):
        attack = self.attack_list[self.attack_list.index(self.current_attack)]
        for enemy in self.LIST:
            if attack.attack_enemy_collision(enemy) and enemy.SPAWNED:
                enemy.SPAWNED = False
                attack.exist = False