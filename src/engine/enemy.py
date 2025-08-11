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
        self.held_bullet = Bullet(self, 'freeze_bullet')
        self.direction = 'left'
        self.current_frame = 0
        self.asset = AssetManager.enemy_assets["freezer"]
        self.state = "idle"
        self.image = self.asset[self.state][0]
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
                self.shoot()
        self.update_animation(prev_state) 
    def update_animation(self,prev_state) :
        if prev_state != self.state :
            self.current_frame = 0
        self.image = self.assets[self.state][int(self.current_frame)]
        self.current_frame += config.PLAYER_FRAMES_SPEED
        if(self.current_frame >= len(self.assets[self.state])) :
            self.current_frame = 0
    
    def shoot(self):
        self.held_bullet.fire()
        self.held_bullet = Bullet(self, 'freeze_bullet')


