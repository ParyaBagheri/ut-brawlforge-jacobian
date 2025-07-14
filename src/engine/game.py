import pygame
import sys
import os

import config



# Fonts 
pygame.font.init()
font = pygame.font.SysFont('Arial',  32, True, False)
heartfont = pygame.font.SysFont('Segoe UI Symbol', 40)
gameoverfont = pygame.font.SysFont('OCR A Extended', 72)
loadingscreen_font = pygame.font.SysFont('OCR A Extended', 36)

from src.engine.bullet import Bullet
from src.engine.player import Player
from src.engine.platform import Platform
from src.engine.enemy import Enemy
from src.engine.assetmanager import AssetManager

class Game:
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.BASE_SCREEN_WIDTH, config.BASE_SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Platformer Game")
        self.clock = pygame.time.Clock()
        self.start = False
        
        self.update_dimensions()
        
        # Create platforms and ground
        self.platforms = [
            Platform(300, 400, 200, 20),
            Platform(600, 350, 150, 20),
            Platform(900, 300, 100, 20),
            Platform(1200, 400, 200, 20),
            Platform(1400, 420,200, 20),
            self.ground_rect
        ]
        
        AssetManager.load_assets()

        self.Fired_bullets_list = []
        self.character_type = "girl"
        self.player = Player(self, self.character_type)
        self.camera_x = 0
        self.enemies = pygame.sprite.Group()
        enemy = Enemy(self)
        self.enemies.add(enemy)

        self.isGameover = False

    def update_dimensions(self):
        # Update screen and ground dimensions based on current window size
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.ground_rect = pygame.Rect(0, self.screen_height - config.BASE_GROUND_HEIGHT, self.screen_width * 10, config.BASE_GROUND_HEIGHT)

    def update_camera(self):
        # Camera follows the player horizontally
        self.camera_x = self.player.rect.centerx - self.screen_width // 2
        max_camera_x = self.ground_rect.width - self.screen_width
        self.camera_x = max(0, min(self.camera_x, max_camera_x))
    
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                # Resize window and update dimensions
                self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                self.update_dimensions()
            elif self.start == False and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.start = True
            elif event.type == pygame.MOUSEBUTTONDOWN :
                if event.button == 1 : #left mouse button
                    self.player.is_shooting = True

            # Restart after game over
            elif self.isGameover == True and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.player
                self.player.health = config.MAX_PLAYER_HEALTH
                self.player.color = (255, 0, 0)
                self.isGameover = False
    
    def update(self):
        if self.isGameover == False and self.start == True:
            self.player.update(self.platforms, self.enemies)
            self.update_camera()
            for enemy in self.enemies:
                enemy.update()

            # Update all fired bullets
            for bullet in self.Fired_bullets_list :
                if isinstance(bullet, Bullet) :
                    bullet.update()

            # Remove dead enemies and spawn new ones
            for enemy in self.enemies:
                if enemy.rect.x <= 0 + self.camera_x or enemy.health <= 0 or self.isGameover == True :
                    enemy.kill()
                    new_enemy = Enemy(self)
                    self.enemies.add(new_enemy)
    
    def draw(self):
        self.screen.fill((135, 206, 235))  # Sky blue background
        
        # Draw platforms and ground
        for platform in self.platforms:
            if isinstance(platform, Platform):
                platform.draw(self.screen, self.camera_x)
            else:
                pygame.draw.rect(self.screen, (34, 139, 34), 
                               pygame.Rect(platform.x - self.camera_x, 
                                          platform.y, 
                                          platform.width, 
                                          platform.height))
        
        # Draw player
        if(self.player.visible == True) :
            if self.player.direction == "left" :
                self.screen.blit( pygame.transform.flip(self.player.image,True,False), (self.player.rect.x - self.camera_x, self.player.rect.y))
            else :
                self.screen.blit( self.player.image, (self.player.rect.x - self.camera_x, self.player.rect.y))
        
        # Draw all fired bullets with camera offset
        for bullet in self.Fired_bullets_list :
            if isinstance(bullet, Bullet) :
                self.screen.blit(bullet.image, (bullet.rect.x - self.camera_x, bullet.rect.y))

        # Draw enemies
        for enemy in self.enemies:
            pygame.draw.rect(self.screen, enemy.color,
                             pygame.Rect(enemy.rect.x - self.camera_x, 
                                        enemy.rect.y, 
                                        enemy.rect.width, 
                                        enemy.rect.height))
            
        # Show health
        health_display = font.render("Health: " + str(self.player.health), True, 'white')
        self.screen.blit(health_display, (20,20))
        heart = heartfont.render("♥", True, "red")
        if self.player.health >= 0:
            for i in range(0,self.player.health):
                self.screen.blit(heart, (40 + 30*i , 40))
        # Show game over
        if self.isGameover == True:
            gameover_message = gameoverfont.render("GAME OVER!", True, 'black')
            text_rect = gameover_message.get_rect()
            text_rect.center = (self.screen_width //2, self.screen_height//2)
            self.screen.blit(gameover_message, text_rect)
        # Show loading screen 
        if self.start == False:
            self.screen.fill((0,0,0))
            loadingscreen_text = loadingscreen_font.render("Press space to start the game!", True, 'white')
            ls_text_rect = loadingscreen_text.get_rect()
            ls_text_rect.center = (self.screen_width //2, self.screen_height //2)
            self.screen.blit(loadingscreen_text, ls_text_rect)

    def gameover(self):
        self.isGameover = True
        self.player.color = (0, 0, 0)
        self.player.rect.x = 100
        self.player.invincibility_timer = 0
        self.player.is_invincible = False

if __name__ == "__main__":
    game = Game()
    game.run()
