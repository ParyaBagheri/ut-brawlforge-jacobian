import pygame
import config
from src.engine.bullet import Bullet
from src.engine.assetmanager import AssetManager

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

    def got_shot(self, damage):
        self.health -= damage

class Freezerenemy(Enemy) :
    def __init__(self, game, start_x, start_y):
        super().__init__(game)
        self.start_x = start_x
        self.start_y = start_y
        self.rect = pygame.Rect(self.start_x, self.start_y, 50, 50)
        self.activated = False
        self.activation_timer = 0
        self.held_bullet = Bullet(self, 'freeze')
        self.direction = 'left'
        self.state = "idle"
        self.current_frame = 0
        self.assets = AssetManager.enemy_assets["freezer"]
        self.image = self.assets["idle"][0]
        self.type = "freezer"
    
    def update(self):
        prev_state = self.state
        if self.game.player.rect.x - self.rect.x <= 800 and self.game.player.rect.x - self.rect.x >= 0:
            self.activated = True
            self.direction = 'right'
        elif self.game.player.rect.x - self.rect.x <= 0 and self.game.player.rect.x - self.rect.x >= -800 :
            self.activated = True
            self.direction = 'right'
        else :
            self.activated = False
            self.activation_timer = 0
        if self.activated :
            self.activation_timer += 1
            if self.activation_timer % 180 == 0:
                self.state = "attack"
                self.shoot()
            if self.health <= 0 :
                self.health = 0
                self.state = "death"
            else :
                self.state = "idle"
            self.update_animation(prev_state)

    
    def shoot(self):
        self.held_bullet.fire([self.game.player.rect.x + 15 - self.rect.x , self.game.player.rect.y -self.rect.y])
        self.held_bullet = Bullet(self, 'freeze')

    def update_animation(self, prev_state):
        if self.state != prev_state:
            self.current_frame = 0
        self.image = self.assets[self.state][int(self.current_frame)]
        self.current_frame += config.PLAYER_FRAMES_SPEED
        if (self.current_frame >= len(self.assets[self.state])):
            if self.state == "death" :
                self.kill()
            else :
                self.current_frame = 0

