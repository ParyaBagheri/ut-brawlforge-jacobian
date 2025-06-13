import pygame
import config

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.rect = pygame.Rect(self.game.screen_width + self.game.camera_x , 450, 50, 50)
        self.velocity_y = 0
        self.on_ground = False
        self.color = (60, 77, 217) 
        self.health = config.MAX_ENEMY_HEALTH
        self.velocity_x = -1*(config.INITIAL_ENEMY_SPEED)
        self.is_collided = False
    def update(self):
        self.rect.x += self.velocity_x

    def got_shot(self):
        self.health -= config.BULLET_DAMAGE