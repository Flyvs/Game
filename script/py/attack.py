import pygame

class Attack(pygame.sprite.Sprite):
    # initializing
    def __init__(self, CLASS: str, DMG: int, path: str, player, game, group):
        super().__init__(group)

        Attack.CLASS = CLASS
        Attack.DMG = DMG

        Attack.spritePath = path
        Attack.right = "attackRight.png"
        Attack.left = "attackLeft.png"
        Attack.firingLeft = False
        Attack.firingRight = False
        Attack.attacking = False
        Attack.exist = False
        self.left = False
        Attack.game = game
        Attack.player = player
        Attack.xRight = Attack.player.rect.center[0] + 48
        Attack.yRight = Attack.player.rect.center[1] + 14
        Attack.xLeft = Attack.player.rect.center[0] - 48
        Attack.yLeft = Attack.player.rect.center[1] + 14
        Attack.posRight = (Attack.xRight, Attack.yRight)
        Attack.posLeft = (Attack.xLeft, Attack.yLeft)

        Attack.image = pygame.image.load(Attack.spritePath + Attack.right).convert_alpha()
        Attack.rect = Attack.image.get_rect(center=Attack.posRight)

    # positioning the attack and set the attack key
    def input(self):
        self.keys = pygame.key.get_pressed()
        Attack.xRight = Attack.player.rect.center[0] + 48
        Attack.yRight = Attack.player.rect.center[1] + 14
        Attack.xLeft = Attack.player.rect.center[0] - 48
        Attack.yLeft = Attack.player.rect.center[1] + 14
        Attack.posRight = (Attack.xRight, Attack.yRight)
        Attack.posLeft = (Attack.xLeft, Attack.yLeft)

        if Attack.exist == False:
            if self.keys[pygame.K_e] or (Attack.game.gamepadInputs != None and Attack.game.gamepadInputs[11] == 1):
                Attack.attacking = True
                if Attack.player.facingLeft == True:
                    Attack.image = pygame.image.load(Attack.spritePath + Attack.left).convert_alpha()
                    Attack.rect = Attack.image.get_rect(center=Attack.posLeft)
                    self.left = True
                elif Attack.player.facingRight == True:
                    Attack.image = pygame.image.load(Attack.spritePath + Attack.right).convert_alpha()
                    Attack.rect = Attack.image.get_rect(center=Attack.posRight)
                    self.left = False
                Attack.exist = True
            else:
                Attack.attacking = False
        else:
            if self.left == True:
                Attack.rect[0] -= 11
                if Attack.rect[0] <= Attack.player.rect[0] - (Attack.game.screen.get_size()[0] // 2) - 100:
                    Attack.exist = False
            if self.left == False:
                Attack.rect[0] += 11
                if Attack.rect[0] >= Attack.player.rect[0] + (Attack.game.screen.get_size()[0] // 2) + 100:
                    Attack.exist = False