import pygame
import os
from typing import List

from npc import NPC
from attack import Attack

class Camera(pygame.sprite.Group):
    def __init__(self,
                 ground_path: str):
        
        super().__init__()

        self.npc_list: List[NPC] = []
        self.attack_list: List[Attack] = []
        self.current_attack: Attack

        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        self.grounds = []
        ground_path = ground_path
        for file in os.listdir(ground_path):
            ground = ground_path + file
            self.grounds.append(ground)

        self.ground(self.grounds[0])

        self.internal_surf_size = (2500, 2500)
        self.internal_surf = pygame.Surface(self.internal_surf_size, pygame.SRCALPHA)
        self.internale_rect = self.internal_surf.get_rect(center=(self.half_w, self.half_h))
        self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surf_size)
        self.internal_offset = pygame.math.Vector2()
        self.internal_offset.x = self.internal_surf_size[0] // 2 - self.half_w
        self.internal_offset.y = self.internal_surf_size[1] // 2 - self.half_h
        
    def ground(self, which_ground: str):
        self.ground_surf = pygame.image.load(which_ground).convert_alpha()
        self.ground_rect = self.ground_surf.get_rect(topleft=(0, 0))
        self.basic_height = self.ground_surf.get_height()
        self.basic_width = self.ground_surf.get_width()

    def center_target_camera(self, target: any):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def custom_draw(self, player, enemy_list: list):
        self.center_target_camera(player)
        self.internal_surf.fill("#71ddee")
        num_of_enemies = len(enemy_list)

        ground_offset = self.ground_rect.topleft - self.offset + self.internal_offset
        self.internal_surf.blit(self.ground_surf, ground_offset)

        self.sprite_list = self.sprites()
        sprite_list_len = len(self.sprite_list)

        num_of_enemies_to_delete = 0
        for enemy in enemy_list:
            if not enemy.SPAWNED:
                num_of_enemies_to_delete += 1
        
        i = 0
        while sprite_list_len > i:
            sprite_list_len = len(self.sprite_list)
            j = 0
            k = 0

            while not k == num_of_enemies_to_delete:
                obj = str(type(self.sprite_list[j])).partition(".")[2].split["'"][0]
                if obj == "Enemy" and self.sprite_list[j].SPAWNED is False:
                    del self.sprite_list[j]
                    num_of_enemies -= 1
                    k += 1
                j += 1
                if j > num_of_enemies - 1:
                    break
            
            obj = str(type(self.sprite_list[i - 1])).partition(".")[2].split("'")[0]
            if self.attack_list[self.attack_list.index(self.current_attack)].attacking is False and obj == "Attack:":
                del self.sprite_list[i - 1]
            if str(type(self.sprite_list[1])).partition(".")[2].split("'")[0] == "Attack":
                del self.sprite_list[1]
            for npc in self.npc_list:
                if npc.hit(player) is False and obj == "MsgBox":
                    del self.sprite_list[5 + num_of_enemies] # for every added sprite its [current_val+1 + numOfEnemies] | Is there a way to get current_val automatically?
            if str(type(self.sprite_list[0])).partition(".")[2].split("'")[0] == "MsgBox":
                del self.sprite_list[0]
            i += 1

        for sprite in self.sprite_list:
            offset_pos = sprite.rect.topleft - self.offset + self.internal_offset
            self.internal_surf.blit(sprite.image, offset_pos)

        scaled_surf = pygame.transform.scale(self.internal_surf, self.internal_surface_size_vector)
        scaled_rect = scaled_surf.get_rect(center=[self.half_w, self.half_h])
        self.display_surface.blit(scaled_surf, scaled_rect)
