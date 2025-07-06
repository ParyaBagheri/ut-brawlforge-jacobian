import pygame
import config

class Platform(pygame.sprite.Sprite):
    def __init__(self,game, x, y, width, height, type, color=(139, 69, 19), is_solid=True, image=None):
        super().__init__()
        self.game = game
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        if image:
            self.image = image.convert()
        else:
            self.image = pygame.Surface((width, height))
            self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x,y))
        self.color = color
        self.is_solid = is_solid  # Determines if platform is solid for collision
        self.type = type
        self.activated = False
        self.visible = True
        self.visibility_timer = 0
        self.slowing_timer = 0

    def update(self):
        if self.activated :
            self.visibility_timer += 1
            if self.visibility_timer >= 180 :
                self.visible = False

    def draw(self, screen, camera_x):
        # Draw platform with camera offset
        if self.visible :
            pos_x = self.rect.x - camera_x
            pos_y = self.rect.y
            screen.blit(self.image, (pos_x, pos_y))

    def slowing_platform(self):
        self.game.player.is_slowed = True
        self.game.player.slowing_timer = 0

    def bouncy_platform(self):
        self.game.player.velocity_y -= 20
    def timed_platform(self):
        if not self.activated :
            self.activated = True
            self.visibility_timer = 0



        
        