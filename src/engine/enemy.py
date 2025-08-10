import pygame
import config
from src.engine.platform import Platform
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

class Bomber (Enemy,pygame.sprite.Sprite ) :
    def __init__(self, game,start_x,start_y) :
        super().__init__(game)
        self.rect  = pygame.Rect(start_x,start_y , 50, 50 )
        self.velocity_x = config.INITIAL_ENEMY_SPEED
        self.direction = "right"
        self.current_frame = 0
        self.assets = AssetManager.enemy_assets["bomber"]
        self.image = self.assets["idle"][0]
        self.is_inview = False
        self.game = game
        self.state = "idle"
        self.type = "bomber"
    def update (self) :
        prev_state = self.state
        if (self.rect.x >= 0 + self.game.camera_x and self.rect.x - self.game.camera_x <= config.BASE_SCREEN_WIDTH ):
            self.is_inview = True
    
        if self.is_inview :

            if self.rect.colliderect(self.game.player.rect) or self.health <= 0 :
                self.state = "death"
            elif (self.game.player.rect.bottom >= self.rect.bottom) :
                self.state = "run"
            else :
                self.state = "idle"

            if self.state == "run" :

                if self.game.player.rect.x - self.rect.x >= 0 :
                    self.direction = "right"
                    self.rect.x += self.velocity_x
                else :
                    self.direction = "left"
                    self.rect.x -= self.velocity_x
            if self.rect.x <= 0 :
                self.rect.left = 0
                self.state = "idle"
                self.direction = "right"
            # Apply gravity
            self.velocity_y += config.GRAVITY
            self.check_platform_collision()
            self.rect.y += self.velocity_y
            self.update_animation(prev_state)
            
    def check_platform_collision (self):
        # Check vertical collision (falling)
        if self.velocity_y > 0 :
            for platform in self.game.level.platforms:
                if isinstance(platform, Platform) and platform.visible:
                    if (self.rect.bottom + self.velocity_y > platform.rect.top and
                        self.rect.top < platform.rect.top and
                        self.rect.right > platform.rect.left and 
                        self.rect.left < platform.rect.right):
                        self.rect.bottom = platform.rect.top
                        self.velocity_y = 0
                        break
                elif not isinstance(platform, Platform):
                    if (self.rect.bottom + self.velocity_y > platform.top and
                        self.rect.top < platform.top and
                        self.rect.right > platform.left and 
                        self.rect.left < platform.right):
                        self.rect.bottom = platform.top
                        self.velocity_y = 0
                        break


        for platform in self.game.level.platforms :
            if isinstance(platform, Platform) and platform.visible:
                if(self.rect.top < platform.rect.bottom and
                    self.rect.bottom > platform.rect.top) :
                    if(self.direction == "right" and
                       self.rect.right == platform.rect.left):
                        self.rect.right = platform.rect.left
                        return platform
                    elif(self.direction == "left" and
                         self.rect.left == platform.rect.right):
                        self.rect.left = platform.rect.right
                        return platform
    def update_animation (self, prev_state) :
        if self.state != prev_state :
            self.current_frame = 0
        self.image = self.assets[self.state][int(self.current_frame)]
        self.current_frame += config.PLAYER_FRAMES_SPEED
        if(self.current_frame >= len(self.assets[self.state])) :
            if self.state == "death" :
                self.kill()
            else :
                self.current_frame = 0
