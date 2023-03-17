import pygame

from attack import Attack

class Enemy(pygame.sprite.Sprite):
    # initializing
    def __init__(self, group, POS: tuple, LVL: int, HP: int, PHYATK: int, MAGATK: int, PHYDEF: int, MAGDEF: int, SPEED: int, MVMTSPEED: int, SPAWNED: bool, SPRITE: str, game, player):
        """
        "game" and "player" needs to be class type
        """
        super().__init__(group)

        self.POS = POS
        self.LVL = LVL
        self.HP = HP
        self.PHYATK = PHYATK
        self.MAGATK = MAGATK
        self.PHYDEF = PHYDEF
        self.MAGDEF = MAGDEF
        self.SPEED = SPEED
        self.MVMTSPEED = MVMTSPEED
        self.SPAWNED = SPAWNED
        self.SPRITE = SPRITE

        Enemy.game = game
        Enemy.player = player

        self.image = pygame.image.load(Enemy.game.enemyPath + self.SPRITE).convert_alpha()
        self.rect = self.image.get_rect(topleft=self.POS)

    # track position of player
    def findPlayer():
        direction = pygame.math.Vector2()
        recenter = pygame.math.Vector2()

        for enemy in Enemy.list:
            if enemy.SPAWNED:
                recenter.y = enemy.rect.center[1]
                
                if Enemy.player.rect.center[0] > enemy.rect.center[0]:
                    direction.x = enemy.MVMTSPEED
                elif Enemy.player.rect.center[0] < enemy.rect.center[0]:
                    direction.x = -enemy.MVMTSPEED

                enemy.rect.center += direction

                # recentering the enemy
                dif = enemy.rect.center[0] - Enemy.player.rect.center[0]
                if dif <= enemy.MVMTSPEED - 1: 
                    if Enemy.player.rect.center[0] < enemy.rect.center[0] + enemy.MVMTSPEED:
                        recenter.x = enemy.rect.center[0] - dif
                        enemy.rect.center = recenter                           

    # start battle
    def attackPlayer(self):
        if (self.player_enemy_collision()) and (Enemy.player.hit):
            Enemy.player.hit = False
            Enemy.game.run = "battle"

    # checks if the enemy is hit
    def hit(self):
        for enemy in Enemy.list:
            if Attack.attack_enemy_collision(self, enemy) and enemy.SPAWNED:
                enemy.SPAWNED = False
                Attack.exist = False