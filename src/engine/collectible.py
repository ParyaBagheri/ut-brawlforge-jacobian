import pygame

class Powerup(pygame.sprite.Sprite):
    def __init__(self, game, x, y, type):
        self.game = game 
        self.x = x
        self.y = y
        self.rect = pygame.rect.Rect(x, y, 50, 50)
        self.type = type
        self.timer = 0
        self.visible = True
        self.is_inview = False
    def  update(self):
        pos = self.x - self.game.camera_x 
        if pos < 750 and pos > 0 :
            self.is_inview = True
        if self.visible and self.is_inview :
            self.timer += 1
            if self.timer >= 300:
                self.visible = False
    def draw(self):
        shield_img = pygame.image.load("src/assets/images/powerups/shield.png").convert_alpha()
        doublejump_img = pygame.image.load("src/assets/images/powerups/doublejump.png").convert_alpha()
        boost_img = pygame.image.load("src/assets/images/powrups/boost.png").convert_alpha()
        pos = self.x - self.game.camera_x 
        if self.visible:
            if self.type == "shield":
                self.game.screen.blit(shield_img, (pos,self.y))
            if self.type == "doublejump":
                self.game.screen.blit(doublejump_img, (pos, self.y))
            if self.type == "damageboost" :
                self.game.screen.blit(boost_img, (pos, self.y))

