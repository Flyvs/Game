import pygame
import json
from typing import List

from hud import HUD
from msgbox import MsgBox
from npc import NPC
from attack import Attack
from enemy import Enemy

class Player(pygame.sprite.Sprite):
    def __init__(self,
                 group,
                 pos: tuple,
                 json_path: str,
                 player_path: str,
                 game):
        
        super().__init__(group)

        with open(json_path + "playerdata.json", "r") as file:
            self.player_data = json.load(file)

        self.LVL = self.player_data["LVL"]
        self.XP = self.player_data["XP"]
        self.HP = self.player_data["HP"]
        self.ATK = self.player_data["ATK"]
        self.DEF = self.player_data["DEF"]
        self.STAMINA = self.player_data["STAMINA"]
        self.player_path = player_path
        self.npc_list: List[NPC] = []
        self.attack_list: List[Attack] = []
        self.enemy_list: List[Enemy] = None
        self.current_attack: Attack

        self.right = "playerR.png"
        self.left = "playerL.png"
        self.right_b = "playerRblack.png"
        self.left_b = "playerLblack.png"

        self.facing_left = False
        self.facing_right = True
        self.facing_up = False
        self.facing_down = False
        self.hit = True

        self.color = "w"

        self.image = pygame.image.load(self.player_path + self.right).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.direction = pygame.math.Vector2()
        self.standard = 10
        self.speed = self.standard
        self.ticks_to_ignore_tab = 30

        self.game = game
        self.camera = group

        self.stamina_HUD_w = 0
        self.stamina_HUD_h = 0
        self.hp_HUD_w = 0
        self.hp_HUD_h = 0
        self.stamina_HUD = HUD(self.camera, (self.stamina_HUD_w, self.stamina_HUD_h), f"Stamina: {self.STAMINA}", None, 60, (255, 0, 0))
        self.hp_HUD = HUD(self.camera, (self.hp_HUD_w, self.hp_HUD_h), f"Health: {self.HP}", None, 60, (255, 0, 0))

    def drain_stamina(self):
        timer = self.game.timer(self.game.player_hit_ticks, self.game.player_hit_seconds,
                                    self.game.player_hit_minutes, self.game.player_hit_hours)
        if self.color == "b" and self.STAMINA > 0:
            self.game.player_hit_ticks = timer["ticks"]
            self.game.player_hit_seconds = timer["seconds"]

            if timer["seconds"] % 2 == 0:
                self.STAMINA -= 1
                self.game.player_hit_ticks = 0
                self.game.player_hit_seconds = 0

        if self.STAMINA == 0:
            self.color = "w"
            self.player_image()
        
        if self.color == "w" and self.STAMINA < self.player_data["STAMINA"]:
            if timer["seconds"] % 2 == 0:
                self.STAMINA += 1
                self.game.player_hit_ticks = 0
                self.game.player_hit_seconds = 0
        
        if self.color == "b":
            self.speed = self.standard * 1.5
        else:
            self.speed = self.standard

    def gamepad(self):
        if self.game.gamepad_inputs is not None:
            if self.game.gamepad_inputs[4] > 0:
                if self.col_bottom is False:
                    self.direction.y = self.game.gamepad_inputs[4]
                else:
                    self.direction.y = 0
            elif self.game.gamepad_inputs[4] < 0:
                if self.col_top is False:
                    self.direction.y = self.game.gamepad_inputs[4]
                else:
                    self.direction.y = 0

            if self.game.gamepad_inputs[3] > 0:
                if self.col_right is False:
                    self.facing_right = True
                    self.facing_left = False
                    self.direction.x = self.game.gamepad_inputs[3]
                else:
                    self.direction.x = 0
            elif self.game.gamepad_inputs[3] < 0:
                if self.col_left is False:
                    self.facing_right = False
                    self.facing_left = True
                    self.direction.x = self.game.gamepad_inputs[3]
                else:
                    self.direction.x = 0
            
    def keyboard(self):
        self.keys = pygame.key.get_pressed()

        if self.keys[pygame.K_w]:
            if self.col_top is False:
                self.direction.y = -1
            else:
                self.direction.y = 0
        elif self.keys[pygame.K_s]:
            if self.col_bottom is False:
                self.direction.y = 1
            else:
                self.direction.y = 0
        else:
            self.direction.y = 0

        if self.keys[pygame.K_d]:
            self.facing_right = True
            self.facing_left = False
            if self.col_right is False:
                self.direction.x = 1
            else:
                self.direction.x = 0
        elif self.keys[pygame.K_a]:
            self.facing_right = False
            self.facing_left = True
            if self.col_left is False:
                self.direction.x = -1
            else:
                self.direction.x = 0
        else:
            self.direction.x = 0
    
    def player_image(self):
        if self.ticks_to_ignore_tab > 0:
            self.ticks_to_ignore_tab -= 1

        if self.facing_left is True:
            if self.color == "w":
                self.image = pygame.image.load(self.player_path + self.left).convert_alpha()
            elif self.color == "b" and self.STAMINA > 0:
                self.image = pygame.image.load(self.player_path + self.left_b).convert_alpha()
        elif self.facing_right is True:
            if self.color == "w":
                self.image = pygame.image.load(self.player_path + self.right).convert()
            elif self.color == "b" and self.STAMINA > 0:
                self.image = pygame.image.load(self.player_path + self.right_b).convert_alpha()
        
        if (self.keys[pygame.K_TAB] and self.ticks_to_ignore_tab == 0) or (self.game.gamepad_inputs is not None and self.game.gamepad_inputs[13] == 1 and self.ticks_to_ignore_tab == 0):
            self.ticks_to_ignore_tab = 30
            if self.color == "w":
                self.color = "b"
            elif self.color == "b":
                self.color = "b"

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

        if self.npc_list is not None:
            for npc in self.npc_list:
                if npc.hit(self) and npc.hitted is False:
                    npc.hitted = True
                    MsgBox(group=self.camera,
                        pos = (npc.rect[0] - 224, npc.rect[1] - 192),
                        text = "This is a demo text",
                        font = None,
                        fontSize = 60,
                        rgbText = (66, 135, 245),
                        rgbaBox = (255, 200, 0, 255),
                        width = 512,
                        height = 128,
                        mergePath = self.game.path("temp"))
        
        self.keyboard()
        self.gamepad()
        self.player_image()
        self.drain_stamina()

        self.rect.center += self.direction * self.speed
        
        if self.attack_list is not None:
            for attack in self.attack_list:
                if attack.TYPE == "classic":
                    use_attack = attack

        use_attack.input()
        self.stamina_HUD.update_hud(text = f"Stamina: {self.STAMINA - 1}",
                                    font = None,
                                    fontSize = 60,
                                    rgb = (255, 0, 0),
                                    posx = 125,
                                    posy = 25,
                                    player = self,
                                    game = self.game)
        self.hp_HUD.update_hud(text = f"Health: {self.HP}",
                               font = None,
                               fontSize = 60,
                               rgb = (255, 0, 0),
                               posx = 125,
                               posy = 100,
                               player = self,
                               game = self.game)
        
        if self.enemy_list is not None:
            for enemy in self.enemy_list:
                enemy.attack_player()
                enemy.hit()
        
        self.game.tp("ground:0", "ground:1", 1946, 900, 52, 200, (640, 1780))

    def aabb_collision(self, a_x, a_y, a_width, a_height, b_x, b_y, b_widht, b_height):
        collision_x = a_x + a_width >= b_x and b_x + b_widht >= a_x
        collision_y = a_y + a_height >= b_y and b_y + b_height >= a_y
        return collision_x and collision_y
    
    def screen_collision_left(self):
        return self.rect.center[0] <= 0
    
    def screen_collision_right(self):
        return self.rect.center[0] >= self.camera.basic_width
    
    def screen_collision_top(self):
        return self.rect.center[1] <= 0
    
    def screen_collision_bottom(self):
        return self.rect.center[1] >= self.camera.basic_height
    
    def player_enemy_collision(self):
        enemyToCheck: Enemy = self.enemy_list.pop(0)
        self.enemy_list.append(enemyToCheck)
        if enemyToCheck.SPAWNED:
            return self.aabb_collision(self.rect.center[0], self.rect.center[1], 64, 64, enemyToCheck.rect.center[0], enemyToCheck.rect.center[1], 64, 64)
        
    def player_tp_collision(self, hitbox_x: int, hitbox_y: int, hitbox_w: int, hitbox_h: int):
        return self.aabb_collision(self.rect.center[0], self.rect.center[1], 64, 64, hitbox_x, hitbox_y, hitbox_w, hitbox_h)