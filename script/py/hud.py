import pygame

class HUD(pygame.sprite.Sprite):
    def __init__(self,
                 group,
                 pos: tuple,
                 text: str,
                 font: str,
                 fontSize: int,
                 rgb: tuple):
        
        super().__init__(group)
        
        font_ = pygame.font.SysFont(font, fontSize)
        self.image = font_.render(text, True, rgb)
        self.rect = self.image.get_rect(center=pos)
    
    def update_hud(self, text: str, font: str, fontSize: int, rgb: tuple, posx: int, posy: int, player, game):
        hud_x = player.rect.center[0] + (game.screen.get_size()[0] // 2) - posx
        hud_y = player.rect.center[1] - (game.screen.get_size()[1] // 2) + posy
        pos = (hud_x, hud_y)

        font_ = pygame.font.SysFont(font, fontSize)
        self.image = font_.render(text, True, rgb)
        self.rect = self.image.get_rect(center=pos)