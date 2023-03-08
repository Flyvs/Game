import pygame

class Enemy(pygame.sprite.Sprite):
    # initializing
    def __init__(self, group, pos: tuple, LVL: int, HP: int, PHYATK: int, MAGATK: int, PHYDEF: int, MAGDEF: int, SPEED: int, SPAWNED: bool, SPRITE: str, game, player):
        """
        "game" and "player" needs to be class type
        """
        super().__init__(group)

        self.pos = pos
        self.LVL = LVL
        self.HP = HP
        self.PHYATK = PHYATK
        self.MAGATK = MAGATK
        self.PHYDEF = PHYDEF
        self.MAGDEF = MAGDEF
        self.SPEED = SPEED
        self.SPAWNED = SPAWNED
        self.SPRITE = SPRITE

        Enemy.game = game
        Enemy.player = player

        self.image = pygame.image.load(Enemy.game.enemyPath + self.SPRITE).convert_alpha()
        Enemy.rect = self.image.get_rect(topleft=self.pos)

    # track position of player
    def findPlayer(player):
        """
        "player" needs to be class type
        """
        for enemy in Enemy.list:
            direction = pygame.math.Vector2()
            speed = 1

            if Enemy.player.rect.center[0] > enemy.rect.center[0]:
                direction.x = speed
            elif Enemy.player.rect.center[0] < enemy.rect.center[0]:
                direction.x = -speed

            jumping = False
            jumpcount = 1
            fallingspeed = 5
            fall = pygame.math.Vector2()
            fall.y = fallingspeed

            keys = pygame.key.get_pressed()
            if (keys[pygame.K_SPACE] or (player.game.gamepadInputs != None and player.game.gamepadInputs[10] == 1)) and not jumping:
                if jumpcount >= 1:
                    Enemy.rect.center -= fall
                    jumpcount -= 1
                if jumpcount == 0:
                    jumping = True          

            elif Enemy.rect.center[1] <= 1800 - fall.y:
                jumpcount = 0
                if Enemy.rect.center[1] == 1800 - fall.y:
                    jumping = False
                    jumpcount = 1
                fall.y = fallingspeed
                Enemy.rect.center += fall

            enemy.rect.center += direction

    # start battle
    def attackPlayer(self):
        if (self.player_enemy_collision()) and (Enemy.player.hit):
            Enemy.player.hit = False
            Enemy.game.run = "battle"