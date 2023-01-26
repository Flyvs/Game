import pygame
import os

from expandList import ExpandList
from msgbox import MsgBox
from camera import Camera
from attack import Attack
from enemy import Enemy
from main import Game

class Player(pygame.sprite.Sprite):
    # initializing
    def __init__(self, pos, group):
        super().__init__(group)

        Player.LVL = Game.data["LVL"]
        Player.XP = Game.data["XP"]
        Player.HP = Game.data["HP"]
        Player.PHYATK = Game.data["PHYATK"]
        Player.MAGATK = Game.data["MAGATK"]
        Player.PHYDEF = Game.data["PHYDEF"]
        Player.MAGDEF = Game.data["MAGDEF"]
        Player.SPEED = Game.data["SPEED"]

        Player.path = Game.path("sprites", "player")
        Player.right = "playerR.png"
        Player.left = "playerL.png"
        Player.rightB = "playerRblack.png"
        Player.leftB = "playerLblack.png"
        Player.facingLeft = False
        Player.facingRight = True
        Player.hit = True

        Player.color = "w" # w: white; b: black

        Player.image = pygame.image.load(Player.path + Player.right).convert_alpha()
        Player.rect = Player.image.get_rect(center=pos)
        self.direction = pygame.math.Vector2()
        self.speed = 5

        Enemy.list = []
        enemy1 = Enemy(Game.camera, (100, 100), 1, 32, 10, 9, 12, 7, 15, False, "testenemy.png")
        enemy2 = Enemy(Game.camera, (200, 200), 1, 32, 10, 9, 12, 7, 15, False, "testenemy2.png")
        enemy3 = Enemy(Game.camera, (300, 300), 1, 32, 10, 9, 12, 7, 15, False, "testenemy3.png")
        ExpandList.expand(Enemy.list, enemy1, enemy2, enemy3)
        

        Player.attack = Attack(Game.camera, "PHY", 55)

    # set the keys for movement
    def input(self):
        self.keys = pygame.key.get_pressed()

        if self.keys[pygame.K_w]:
            if self.col_top == False:
                self.direction.y = -1
            else:
                self.direction.y = 0
        elif self.keys[pygame.K_s]:
            if self.col_bottom == False:
                self.direction.y = 1
            else:
                self.direction.y = 0
        else:
            self.direction.y = 0

        if self.keys[pygame.K_d]:
            Player.facingRight = True
            Player.facingLeft = False
            if self.col_right == False:
                self.direction.x = 1
            else:
                self.direction.x = 0
        elif self.keys[pygame.K_a]:
            Player.facingRight = False
            Player.facingLeft = True
            if self.col_left == False:
                self.direction.x = -1
            else:
                self.direction.x = 0
        else:
            self.direction.x = 0

        if Player.facingLeft == True:
            if Player.color == "w":
                Player.image = pygame.image.load(Player.path + Player.left).convert_alpha()
            elif Player.color == "b":
                Player.image = pygame.image.load(Player.path + Player.leftB).convert_alpha()
        elif Player.facingRight == True:
            if Player.color == "w":
                Player.image = pygame.image.load(Player.path + Player.right).convert_alpha()
            elif Player.color == "b":
                Player.image = pygame.image.load(Player.path + Player.rightB).convert_alpha()

        if self.keys[pygame.K_TAB] and Game.ticksToIgnoreTAB == 0:
            Game.ticksToIgnoreTAB = 30
            if Player.color == "w":
                Player.color = "b"
            elif Player.color == "b":
                Player.color = "w"

        if Game.ticksToIgnoreTAB > 0:
            Game.ticksToIgnoreTAB -= 1

    # updating details
    def update(self):
        if self.screen_collision_left():
            self.col_left = True
        else:
            self.col_left = False
        if self.screen_collision_right():
            self.col_right = True
        else:
            self.col_right = False
        if self.screen_collision_top():
            self.col_top = True
        else:
            self.col_top = False
        if self.screen_collision_bottom():
            self.col_bottom = True
        else:
            self.col_bottom = False

        if NPC.hit() and NPC.hitted == False:
            NPC.hitted = True
            for _ in os.listdir(Game.msgboxPath):
                MsgBox.init()

        self.input()
        Player.rect.center += self.direction * self.speed
        Attack.input(self)

        Enemy.attackPlayer(self)
        Game.teleport(self, 1948, 900, 52, 200)

    # collision with 2 objects
    def aabb_collision(self, a_x, a_y, a_width, a_height, b_x, b_y, b_width, b_height):
        self.collision_x = a_x + a_width >= b_x and b_x + b_width >= a_x
        self.collision_y = a_y + a_height >= b_y and b_y + b_height >= a_y
        return self.collision_y and self.collision_x

    # left screen collision
    def screen_collision_left(self):
        return Player.rect.center[0] <= 0

    # right screen collision
    def screen_collision_right(self):
        return Player.rect.center[0] >= Camera.basic_width

    # top screen collision
    def screen_collision_top(self):
        return Player.rect.center[1] <= 0

    # bottom screen collision
    def screen_collision_bottom(self):
        return Player.rect.center[1] >= Camera.basic_height

    # player enemy collision
    def player_enemy_collision(self):
        enemyToCheck = Enemy.list.pop(0)
        Enemy.list.append(enemyToCheck)
        return self.aabb_collision(Player.rect.center[0], Player.rect.center[1], 64, 64, enemyToCheck.rect.center[0], enemyToCheck.rect.center[1], 64, 64)

    # player teleport collision
    def player_teleport_collision(self, hitboxX: int, hitboxY: int, hitboxWidth: int, hitboxHeigth: int):
        return self.aabb_collision(Player.rect.center[0], Player.rect.center[1], 64, 64, hitboxX, hitboxY, hitboxWidth, hitboxHeigth)


class NPC(pygame.sprite.Sprite):
    # initializing
    def __init__(self, pos, group):
        super().__init__(group)

        NPC.hitted = False
        NPC.path = Game.path("sprites", "NPCs")

        NPC.allItems = []
        NPC.image = pygame.image.load(NPC.path + NPC.spawn("testNPC")).convert_alpha()
        NPC.rect = NPC.image.get_rect(topleft=pos)

    # spawn the npc
    def spawn(item: str):
        for file in os.listdir(NPC.path):
            casefoldFile = file[:-4].casefold()
            item = item.casefold()
            if casefoldFile == item:
                return file

    # check if npc is hit
    def hit():
        collision_x = Player.rect[0] + 64 >= NPC.rect[0] and NPC.rect[0] + 64 >= Player.rect[0]
        collision_y = Player.rect[1] + 64 >= NPC.rect[1] and NPC.rect[1] + 64 >= Player.rect[1]
        return collision_y and collision_x