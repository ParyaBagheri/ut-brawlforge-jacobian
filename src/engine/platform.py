import pygame
import config
from src.engine.assetmanager import AssetManager

class Platform(pygame.sprite.Sprite):
    def __init__(self,game, x, y, width, height, type='solid', is_solid=True, image=None):
        super().__init__()
        self.game = game
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        if type == 'bouncy' :
            self.image = AssetManager.platform_images["bouncy"][0]
        if type == 'timed' :
            self.image = AssetManager.platform_images["timed"]
        if image:
            self.image = pygame.transform.scale(image,(width,height))
        

        else:
            self.image = pygame.Surface((width, height))
            #self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x,y))
        #self.color = color
        self.is_solid = is_solid  # Determines if platform is solid for collision
        self.type = type
        self.activated = False
        self.visible = True
        self.visibility_timer = 0
        self.slowing_timer = 0
         #bouncy platform animation
        self.bounce_animation = False
        self.current_frame = 0

    def update(self):
        if self.activated :
            self.visibility_timer += 1
            if self.visibility_timer >= 60 :
                self.visible = False

    def draw(self, screen, camera_x):
        # Draw platform with camera offset
        if self.visible :
            pos_x = self.rect.x - camera_x
            pos_y = self.rect.y
            if self.bounce_animation :
                self.current_frame += 0.3
                if int(self.current_frame) >= 5 :
                    self.current_frame = 0
                    self.bounce_animation = False
                self.image = AssetManager.platform_images["bouncy"][int(self.current_frame)]
            elif self.type == 'bouncy' :
                self.image = AssetManager.platform_images["bouncy"][int(self.current_frame)]
            screen.blit(self.image, (pos_x, pos_y))
            
    def slowing_platform(self):
        if self.game :
            self.game.player.is_slowed = True
            self.game.player.slowing_timer = 0

    def bouncy_platform(self):
        if self.game:
            self.bounce_animation = True
            self.game.player.velocity_y -= 20
    def timed_platform(self):
        if not self.activated :
            self.activated = True
            self.visibility_timer = 0



        
        