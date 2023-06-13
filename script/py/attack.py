import pygame
from gamepad import Inputs

class Attack(pygame.sprite.Sprite):
    def __init__(self,
                 group,
                 TYPE: str,
                 DMG: int,
                 sprite_path: str,
                 sprite_left: str,
                 sprite_right: str,
                 width: int,
                 height: int,
                 player,
                 game):
        
        super().__init__(group)

        self.TYPE = TYPE
        self.DMG = DMG
        self.sprite_path = sprite_path
        self.right = sprite_right
        self.left = sprite_left
        self.width = width
        self.height = height
        self.player = player
        self.game = game

        self.firingLeft = False
        self.firingRight = False
        self.attacking = False
        self.exist = False
        self.direction = "right"

        x_right = self.player.rect.center[0] + 48
        y_right = self.player.rect.center[1] + 14
        x_left = self.player.rect.center[0] - 48
        y_left = self.player.rect.center[1] + 14
        self.pos_right = (x_right, y_right)
        self.pos_left = (x_left, y_left)

        self.image = pygame.image.load(self.sprite_path + self.right).convert_alpha()
        self.rect = self.image.get_rect(center=self.pos_right)

    def update(self):
        inputs = Inputs.scan()[0]
        keys = pygame.key.get_pressed()
        return inputs, keys

    def input(self):
        update_result = self.update()
        inputs, keys = update_result[0], update_result[1]

        x_right = self.player.rect.center[0] + 48
        y_right = self.player.rect.center[1] + 14
        x_left = self.player.rect.center[0] - 48
        y_left = self.player.rect.center[1] + 14
        self.pos_right = (x_right, y_right)
        self.pos_left = (x_left, y_left)

        if self.exist is False:
            if keys[pygame.K_e] or (inputs is not None and inputs[11] == 1):
                Attack.attacking = True
                if self.player.facing_left is True:
                    self.image = pygame.image.load(self.sprite_path + self.left).convert_alpha()
                    self.rect = self.image.get_rect(center=Attack.pos_left)
                    self.direction = "left"
                elif self.player.facing_right is True:
                    self.image = pygame.image.load(self.sprite_path + self.right).convert_alpha()
                    self.rect = self.image.get_rect(center=self.pos_right)
                    self.direction = "right"
                self.exist = True
            else:
                self.attacking = False
        else:
            if self.direction == "left":
                self.rect[0] -= 11
                if self.rect[0] <= self.player.rect[0] - (self.game.screen.get_size()[0] // 2) - 100:
                    self.exist = False
            elif self.direction == "right":
                self.rect[0] += 11
                if self.rect[0] >= self.player.rect[0] + (self.game.screen.get_size()[0] // 2) + 100:
                    self.exist = False

    def aabb_collision(self, a_x, a_y, a_width, a_height, b_x, b_y, b_widht, b_height):
        collision_x = a_x + a_width >= b_x and b_x + b_widht >= a_x
        collision_y = a_y + a_height >= b_y and b_y + b_height >= a_y
        return collision_x and collision_y
    
    def attack_enemy_collision(self, enemy):
        if self.exist:
            return self.aabb_collision(self.rect[0], self.rect[1], self.width, self.height, enemy.rect[0], enemy.rect[1], 64, 64)