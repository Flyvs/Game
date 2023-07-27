import pygame
import os
from typing import List

from npc import NPC
from attack import Attack
from expandList import ExpandList

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

        ground_offset = self.ground_rect.topleft - self.offset + self.internal_offset
        self.internal_surf.blit(self.ground_surf, ground_offset)

        sprite_list = self.sprites()
        player_sprite = None
        active_npc = None
        npc_sprites = []
        new_sprite_list = []

        for sprite in sprite_list:
            obj = str(type(sprite)).partition(".")[2].split("'")[0]
            if obj == "NPC":
                npc_sprites.append(sprite)
            elif obj == "HUD":
                new_sprite_list.append(sprite)
            elif obj == "Player":
                player_sprite = sprite
            elif obj == "Enemy":
                for enemy in enemy_list:
                    if sprite == enemy:
                        if enemy.SPAWNED:
                            new_sprite_list.append(sprite)
                        break
            elif obj == "Attack":
                attack = self.attack_list[self.attack_list.index(self.current_attack)]
                if attack.attacking and attack.exist:
                    new_sprite_list.append(sprite)
            elif obj == "MsgBox":
                for npc in self.npc_list:
                    if npc.msgbox.active:
                        active_npc = npc

                if active_npc is not None and sprite == active_npc.msgbox:
                    new_sprite_list.append(sprite)
                    active_npc = None
                        

        new_sprite_list = ExpandList.expand(new_sprite_list, player_sprite, *npc_sprites)

        for sprite in new_sprite_list:
            offset_pos = sprite.rect.topleft - self.offset + self.internal_offset
            self.internal_surf.blit(sprite.image, offset_pos)

        scaled_surf = pygame.transform.scale(self.internal_surf, self.internal_surface_size_vector)
        scaled_rect = scaled_surf.get_rect(center=[self.half_w, self.half_h])
        self.display_surface.blit(scaled_surf, scaled_rect)
