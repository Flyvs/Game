import pygame
import json

from camera import Camera
from enemy import Enemy
from npc import NPC
from hud import HUD
from msgbox import MsgBox
from attack import Attack

class Player(pygame.sprite.Sprite):
    # initializing
    def __init__(self, pos: tuple, game, jsonPath: str, playerPath: str, attackPath: str, group):
        """
        "game" needs to be class type
        """
        super().__init__(group)

        playerdatafile = open(jsonPath + "playerdata.json", "r")
        playerdata = json.load(playerdatafile)
        playerdatafile.close()

        Player.LVL = playerdata["LVL"]
        Player.XP = playerdata["XP"]
        Player.HP = playerdata["HP"]
        Player.PHYATK = playerdata["PHYATK"]
        Player.MAGATK = playerdata["MAGATK"]
        Player.PHYDEF = playerdata["PHYDEF"]
        Player.MAGDEF = playerdata["MAGDEF"]
        Player.SPEED = playerdata["SPEED"]
        Player.STAMINA = playerdata["STAMINA"]
        Player.game = game

        Player.path = playerPath
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
        self.fall = pygame.math.Vector2()
        self.jumpV = pygame.math.Vector2()
        self.standard = 10
        self.speed = self.standard

        self.fallingspeed = 10
        self.fall.y = self.fallingspeed
        self.fall.x = 0

        self.jumpcount = 30
        self.jumping = False

        self.camera = group
        
        Player.attack = Attack("PHY", 7, attackPath, Player, Player.game, self.camera)

        Player.HUD_w = 0
        Player.HUD_h = 0
        Player.HUD = HUD(self.camera, (Player.HUD_w, Player.HUD_h), f"Stamina: {Player.STAMINA}", None, 60, (255, 0, 0))
        
   # drains the players stamina
    def drain(self):
        timer = Player.game.tracktime(Player.game.playerHitTicks, Player.game.playerHitSeconds, Player.game.playerHitMinutes, Player.game.playerHitHours)
        if Player.color == "b" and Player.STAMINA > 0:
            Player.game.playerHitTicks = timer["ticks"]
            Player.game.playerHitSeconds = timer["seconds"]

            if timer["seconds"] % 2 == 0:
                Player.STAMINA -= 1
                Player.game.playerHitTicks = 0
                Player.game.playerHitSeconds = 0
        if Player.STAMINA == 0:
            Player.color = "w"
            self.playerImage()
        if Player.color == "w" and Player.STAMINA < Player.game.playerdata["STAMINA"]:
            if timer["seconds"] % 2 == 0:
                Player.STAMINA += 1
                Player.game.playerHitTicks = 0
                Player.game.playerHitSeconds = 0
        if Player.color == "b":
            self.speed = self.standard * 1.5
        else:
            self.speed = self.standard
    
    # jumping
    def jump(self):
        self.keys = pygame.key.get_pressed()
        if (self.keys[pygame.K_SPACE] or (Player.game.gamepadInputs != None and Player.game.gamepadInputs[10] == 1)) and not self.jumping:
            if self.jumpcount >= 1:
                Player.rect.center -= self.fall
                self.jumpcount -= 1
            if self.jumpcount == 0:
                self.jumping = True          

        elif Player.rect.center[1] <= 1800 - self.fall.y:
            self.jumpcount = 0
            if Player.rect.center[1] == 1800 - self.fall.y:
                self.jumping = False
                self.jumpcount = 30
            self.fall.y = self.fallingspeed
            Player.rect.center += self.fall

    # set controls for gamepad movement
    def gamepad(self):
        """
        try:
            if Game.gamepadInputs[4] > 0:
                if self.col_bottom == False:
                    self.direction.y = Game.gamepadInputs[4]
                else:
                    self.direction.y = 0
            elif Game.gamepadInputs[4] < 0:
                if self.col_top == False:
                    self.direction.y = Game.gamepadInputs[4]
                else:
                    self.direction.y = 0
        """
        try:
            if Player.game.gamepadInputs[3] > 0:
                if self.col_right == False:
                    Player.facingRight = True
                    Player.facingLeft = False
                    self.direction.x = Player.game.gamepadInputs[3]
                else:
                    self.direction.x = 0
            elif Player.game.gamepadInputs[3] < 0:
                if self.col_left == False:
                    Player.facingRight = False
                    Player.facingLeft = True
                    self.direction.x = Player.game.gamepadInputs[3]
                else:
                    self.direction.x = 0
        except:
            pass

    # set the keys for movement
    def keyboard(self):
        self.keys = pygame.key.get_pressed()

        """
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
        """

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

    
    def playerImage(self):
        if Player.facingLeft == True:
            if Player.color == "w":
                Player.image = pygame.image.load(Player.path + Player.left).convert_alpha()
            elif Player.color == "b" and Player.STAMINA > 0:
                Player.image = pygame.image.load(Player.path + Player.leftB).convert_alpha()
        elif Player.facingRight == True:
            if Player.color == "w":
                Player.image = pygame.image.load(Player.path + Player.right).convert_alpha()
            elif Player.color == "b" and Player.STAMINA > 0:
                Player.image = pygame.image.load(Player.path + Player.rightB).convert_alpha()

        if (self.keys[pygame.K_TAB] and Player.game.ticksToIgnoreTAB == 0) or (Player.game.gamepadInputs != None and Player.game.gamepadInputs[13] == 1 and Player.game.ticksToIgnoreTAB == 0):
            Player.game.ticksToIgnoreTAB = 30
            if Player.color == "w":
                Player.color = "b"
            elif Player.color == "b":
                Player.color = "w"

        if Player.game.ticksToIgnoreTAB > 0:
            Player.game.ticksToIgnoreTAB -= 1

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

        if NPC.hit(Player) and NPC.hitted == False:
            NPC.hitted = True
            MsgBox((NPC.rect[0] - 224, NPC.rect[1] - 192), "This is a demo text", None, 60, (66, 135, 245), "test.png", Player.game.msgboxPath, Player.game.mergePath, self.camera)

        self.keyboard()
        self.gamepad()
        self.playerImage()
        self.drain()
        self.jump()

        Player.rect.center += self.direction * self.speed
        Attack.input(self)
        HUD.updateHUD(f"Stamina: {Player.STAMINA - 1}", None, 60, (255, 0, 0), Player, Player.game)
        Enemy.attackPlayer(self)
        Player.game.teleport(self, "ground:0", "ground:1", 1948, 900, 52, 200)

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
        try:
            enemyToCheck = Enemy.list.pop(0)
            Enemy.list.append(enemyToCheck)
            return self.aabb_collision(Player.rect.center[0], Player.rect.center[1], 64, 64, enemyToCheck.rect.center[0], enemyToCheck.rect.center[1], 64, 64)
        except:
            pass

    # player teleport collision
    def player_teleport_collision(self, hitboxX: int, hitboxY: int, hitboxWidth: int, hitboxHeigth: int):
        return self.aabb_collision(Player.rect.center[0], Player.rect.center[1], 64, 64, hitboxX, hitboxY, hitboxWidth, hitboxHeigth)