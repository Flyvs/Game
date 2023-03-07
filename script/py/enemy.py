import pygame

class Enemy(pygame.sprite.Sprite):
    # initializing
    def __init__(self, group, POS: tuple, LVL: int, HP: int, PHYATK: int, MAGATK: int, PHYDEF: int, MAGDEF: int, SPEED: int, SPAWNED: bool, SPRITE: str, game, player):
        super().__init__(group)

        self.POS = POS
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
        self.rect = self.image.get_rect(topleft=self.POS)

    # track position of player
    def findPlayer():
        for enemy in Enemy.list:
            direction = pygame.math.Vector2()
            speed = 1

            if Enemy.player.rect.center[0] > enemy.rect.center[0]:
                direction.x = speed
            elif Enemy.player.rect.center[0] < enemy.rect.center[0]:
                direction.x = -speed

            if Enemy.player.rect.center[1] > enemy.rect.center[1]:
                direction.y = speed
            elif Enemy.player.rect.center[1] < enemy.rect.center[1]:
                direction.y = -speed

            enemy.rect.center += direction

    # start battle
    def attackPlayer(self):
        if (self.player_enemy_collision()) and (Enemy.player.hit):
            Enemy.player.hit = False
            Enemy.game.run = "battle"