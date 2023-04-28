import pygame


class Attack(pygame.sprite.Sprite):
    # initializing
    def __init__(self, CLASS: str, DMG: int, path: str, player, game, group):
        """
        "game" and "player" needs to be class type
        """
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
        Attack.direction = "right"
        Attack.game = game
        Attack.player = player
        Attack.xRight = Attack.player.rect.center[0] + 48
        Attack.yRight = Attack.player.rect.center[1] + 14
        Attack.xLeft = Attack.player.rect.center[0] - 48
        Attack.yLeft = Attack.player.rect.center[1] + 14
        Attack.posRight = (Attack.xRight, Attack.yRight)
        Attack.posLeft = (Attack.xLeft, Attack.yLeft)

        Attack.image = pygame.image.load(
            Attack.spritePath + Attack.right).convert_alpha()
        Attack.rect = Attack.image.get_rect(center=Attack.posRight)

    # positioning the attack and set the attack key
    def input(self):
        self.keys = pygame.key.get_pressed()
        xRight = Attack.player.rect.center[0] + 48
        yRight = Attack.player.rect.center[1] + 14
        xLeft = Attack.player.rect.center[0] - 48
        yLeft = Attack.player.rect.center[1] + 14
        Attack.posRight = (xRight, yRight)
        Attack.posLeft = (xLeft, yLeft)

        if Attack.exist == False:
            if self.keys[pygame.K_e] or (Attack.game.gamepadInputs is not None and Attack.game.gamepadInputs[11] == 1):
                Attack.attacking = True
                if Attack.player.facingLeft is True:
                    Attack.image = pygame.image.load(
                        Attack.spritePath + Attack.left).convert_alpha()
                    Attack.rect = Attack.image.get_rect(center=Attack.posLeft)
                    Attack.direction = "left"
                elif Attack.player.facingRight is True:
                    Attack.image = pygame.image.load(
                        Attack.spritePath + Attack.right).convert_alpha()
                    Attack.rect = Attack.image.get_rect(center=Attack.posRight)
                    Attack.direction = "right"
                Attack.exist = True
            else:
                Attack.attacking = False
        else:
            if Attack.direction == "left":
                Attack.rect[0] -= 11
                if Attack.rect[0] <= Attack.player.rect[0] - (Attack.game.screen.get_size()[0] // 2) - 100:
                    Attack.exist = False
            elif Attack.direction == "right":
                Attack.rect[0] += 11
                if Attack.rect[0] >= Attack.player.rect[0] + (Attack.game.screen.get_size()[0] // 2) + 100:
                    Attack.exist = False

    # collision with 2 objects
    def aabb_collision(self, a_x, a_y, a_width, a_height, b_x, b_y, b_width, b_height):
        self.collision_x = a_x + a_width >= b_x and b_x + b_width >= a_x
        self.collision_y = a_y + a_height >= b_y and b_y + b_height >= a_y
        return self.collision_y and self.collision_x

    # collision attack and enemy
    def attack_enemy_collision(self, enemy):
        if Attack.exist:
            return self.aabb_collision(Attack.rect[0], Attack.rect[1], 30, 24, enemy.rect[0], enemy.rect[1], 64, 64)
