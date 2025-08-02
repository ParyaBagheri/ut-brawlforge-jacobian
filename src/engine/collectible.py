import pygame
from src.engine.assetmanager import AssetManager

class Powerup(pygame.sprite.Sprite):
    def __init__(self, game, x, y, type):
        super().__init__()
        self.game = game 
        self.x = x
        self.y = y
        self.rect = pygame.rect.Rect(x, y, 50, 50)
        self.type = type
        self.timer = 0
        self.visible = True
        self.is_inview = False
    def  update(self):
        if self.game.mode == "single_player" :
            pos = self.x - self.game.camera_x 
            if pos < 750 and pos > 0 :
                self.is_inview = True
            if self.visible and self.is_inview :
                self.timer += 1
                if self.timer >= 300:
                    self.visible = False
                    self.kill()
                    self.game.level.powerups.remove(self)
        else :
            if self.visible :
                self.timer += 1
                if self.timer >= 600 :
                    self.visible = False
                    self.kill()
                    self.game.level.powerups.remove(self)
    def draw(self):
        
        pos = self.x - self.game.camera_x 
        if self.visible:
            self.game.screen.blit(AssetManager.powerups_images[self.type], (pos,self.y))
            

