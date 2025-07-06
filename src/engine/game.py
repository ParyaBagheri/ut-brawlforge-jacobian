import pygame
import sys
import os

import config

#press esc to pause, shift to shoot

right_bullet_image_path = os.path.join("src","assets", "images" , "rightpaintball.png")
left_bullet_image_path = os.path.join("src","assets", "images" , "rightpaintball.png")
background_path = os.path.join("src", "assets", "images", "background.jpg")


right_bullet_image = pygame.image.load(right_bullet_image_path)
#right_bullet_image = pygame.image.load(config.IMAGE_PATH, "rightpaintball.png")
right_bullet_image = pygame.transform.scale(right_bullet_image, (20, 20))
left_bullet_image = pygame.image.load(left_bullet_image_path)
#left_bullet_image = pygame.image.load(config.IMAGE_PATH, "leftpaintball.png")
left_bullet_image = pygame.transform.scale(left_bullet_image, (20, 20))

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
from src.engine.button import Button


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.BASE_SCREEN_WIDTH, config.BASE_SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Platformer Game")
        self.clock = pygame.time.Clock()
        self.is_paused = False
        self.update_dimensions()
        self.PAUSE_BUTTON = Button(self, None, [750,10], "Pause", 'Blox2', 30, 'white', 'grey') #Add pause button image later
                
        self.platforms = self.platform_maker()

        #list of fired bullets
        self.Fired_bullets_list = []

        self.player = Player(self)
        self.camera_x = 0
        self.enemies = pygame.sprite.Group()
        enemy = Enemy(self)
        self.enemies.add(enemy)

        self.isGameover = False

    def main_menu(self):
        #self.screen.fill((0, 0, 0))
        background = pygame.image.load(background_path)
        background = pygame.transform.scale(background, (800,600))
        self.screen.blit(background, (0,0))
        MENU_PLAY = Button(self, None, [400, 100], "PLAY","OCRAEXT", 50, (255,255,255), (0,146,155))
        MENU_HOWTO = Button(self, None, [400, 300], "HOW TO PLAY",'OCRAEXT', 50, 'white', (0, 146, 155))
        MENU_MOUSE_POS = pygame.mouse.get_pos
        def main_menu_render():        
            MENU_PLAY.draw(MENU_MOUSE_POS())
            MENU_HOWTO.draw(MENU_MOUSE_POS())
        def main_menu_event_handler():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if MENU_PLAY.is_pressed(MENU_MOUSE_POS()):
                        self.map_menu()
        while True:
            main_menu_render()
            main_menu_event_handler()
            pygame.display.flip()
            self.clock.tick(config.FPS)
    def map_menu(self):
        #self.screen.fill((22, 15, 133))
        #self.screen.fill((246, 231, 143))
        #self.screen.fill((123, 145, 155))
        #self.screen.fill((242, 239, 131))
        background = pygame.image.load(background_path)
        background = pygame.transform.scale(background, (800,600))
        self.screen.blit(background, (0,0))

        map_menu_font = pygame.font.SysFont('OCR A Extended', 45)
        map_menu_text = map_menu_font.render("Choose a map!", True, 'indigo')
        map_menu_text_rect = map_menu_text.get_rect(center= (self.screen_width // 2, self.screen_height//6))
        self.screen.blit(map_menu_text, map_menu_text_rect)
        MAP_1 = Button(self, None, [self.screen_width//4,self.screen_height//2], "Jungle",'OCRAEXT', 40, (0, 38, 21), (0, 89, 21))
        MAP_2 = Button(self, None, [3 *self.screen_width//4, self.screen_height//2], "Desert", 'OCRAEXT', 40, (117, 96,0), (42, 32, 0))
        MAP_3 = Button(self, None, [self.screen_width//4, 5 * self.screen_height//6], "Lost City","OCRAEXT", 40, (255, 181, 118), (81, 1, 109))
        MAP_4 = Button(self, None, [3 * self.screen_width//4, 5 * self.screen_height//6], "Under Water","OCRAEXT", 40, (0, 13, 72), (229, 134, 169))
        MAP_MENU_MOUSE_POS = pygame.mouse.get_pos
        def map_menu_render():
            MAP_1.draw(MAP_MENU_MOUSE_POS())
            MAP_2.draw(MAP_MENU_MOUSE_POS())
            MAP_3.draw(MAP_MENU_MOUSE_POS())
            MAP_4.draw(MAP_MENU_MOUSE_POS())
        def map_menu_event_handler():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if MAP_1.is_pressed(MAP_MENU_MOUSE_POS()):
                        self.run()

        while True:
            map_menu_render()
            map_menu_event_handler()
            pygame.display.flip()
            self.clock.tick(config.FPS)

    def platform_maker(self):
        platforms = [
            Platform(self, 300, 400, 150, 20, 'solid'),
            Platform(self, 600, 300, 150, 20, 'solid'),
            Platform(self, 750, 300, 250, 20, 'solid'), #Fragile platform
            Platform(self, 1050, 200, 100, 20, 'solid'), # Bonus on this platform
            Platform(self, 1140, 560 - config.BASE_GROUND_HEIGHT, 50, 40, 'bouncy'), #Bouncy platform
            Platform(self, 1250, 300, 300, 20, 'solid'),
            Platform(self, 1400, 580 - config.BASE_GROUND_HEIGHT, 350, 20, 'slowing'), #Muddy platform
            Platform(self, 1630, 200, 100, 20, 'timed'),
            self.ground_rect
        ]
        return platforms

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
        GAME_MOUSE_POS = pygame.mouse.get_pos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                # Resize window and update dimensions
                self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                self.update_dimensions()
            elif ((event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or 
                  (event.type == pygame.MOUSEBUTTONDOWN and self.PAUSE_BUTTON.is_pressed(GAME_MOUSE_POS()))) and self.isGameover == False :
                # Press esc or pause button to pause
                self.is_paused = True

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_paused == False and self.isGameover == False:
                #if event.button == 1 : #left mouse button
                    self.player.shoot()
            elif event.type == pygame.KEYDOWN and self.is_paused == True: # press space to resume
                if event.key == pygame.K_SPACE:
                    self.is_paused = False
            # Restart after game over
            elif self.isGameover == True and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.restart()
    
    def update(self):
        if self.isGameover == False and self.is_paused == False:
            self.player.update(self.platforms, self.enemies)
            self.update_camera()

            for platform in self.platforms :
                if isinstance(platform, Platform):
                    platform.update()
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
        GAME_MOUSE_POS = pygame.mouse.get_pos
        self.PAUSE_BUTTON.draw(GAME_MOUSE_POS())
        if self.is_paused == True: 
            self.pause_render()

        # Draw platforms and ground
        for platform in self.platforms:
            if isinstance(platform, Platform) and platform.visible == True:
                platform.draw(self.screen, self.camera_x)
            elif not isinstance(platform, Platform) :
                pygame.draw.rect(self.screen, (34, 139, 34), 
                               pygame.Rect(platform.x - self.camera_x, 
                                          platform.y, 
                                          platform.width, 
                                          platform.height))
        
        # Draw player
        if(self.player.visible == True) :
            pygame.draw.rect(self.screen, self.player.color, 
                        pygame.Rect(self.player.rect.x - self.camera_x, 
                                   self.player.rect.y, 
                                   self.player.rect.width, 
                                   self.player.rect.height))
        
        # Draw all fired bullets with camera offset
        for bullet in self.Fired_bullets_list :
            if isinstance(bullet, Bullet) :
                self.screen.blit(bullet.bulletimg, (bullet.rect.x - self.camera_x, bullet.rect.y))

        # Draw enemies
        self.draw_enemies()
        # Show health
        self.show_health()
        # Show game over
        if self.isGameover == True:
            self.gameover_render()
        # Show loading screen 
        '''if self.is_started == False:
            self.screen.fill((0,0,0))
            loadingscreen_text = loadingscreen_font.render("Press space to start the game!", True, 'white')
            ls_text_rect = loadingscreen_text.get_rect()
            ls_text_rect.center = (self.screen_width //2, self.screen_height //2)
            self.screen.blit(loadingscreen_text, ls_text_rect)'''
        
    def draw_enemies(self):
        for enemy in self.enemies:
            pygame.draw.rect(self.screen, enemy.color,
                             pygame.Rect(enemy.rect.x - self.camera_x, 
                                        enemy.rect.y, 
                                        enemy.rect.width, 
                                        enemy.rect.height))
    def show_health(self):
        health_display = font.render("Health: " + str(self.player.health), True, 'white')
        self.screen.blit(health_display, (20,20))
        heart = heartfont.render("♥", True, "red")
        if self.player.health >= 0:
            for i in range(0,self.player.health):
                self.screen.blit(heart, (40 + 30*i , 40))

    def gameover(self):
        self.isGameover = True
        self.player.color = (0, 0, 0)
        self.player.rect.x = 100
        self.player.rect.bottom = 600 - config.BASE_GROUND_HEIGHT
        self.player.invincibility_timer = 0
        self.player.is_invincible = False

    def gameover_render(self):
        gameover_font = pygame.font.Font("src/assets/fonts/OCRAEXT.ttf", 72)
        gameover_message = gameover_font.render("GAME OVER!", True, 'black')
        text_rect = gameover_message.get_rect()
        text_rect.center = (self.screen_width //2, self.screen_height//2)
        self.screen.blit(gameover_message, text_rect)

    def restart(self):
        self.player.health = config.MAX_PLAYER_HEALTH
        self.player.color = (255, 0, 0)
        self.isGameover = False

    def pause_render(self):
        pause_msg_font =  pygame.font.Font("src/assets/fonts/OCRAEXT.ttf", 50)
        pause_msg_text = pause_msg_font.render("Press space to resume!", True, 'indigo')
        pause_msg_rect = pause_msg_text.get_rect(center=(self.screen_width//2, self.screen_height//2))
        self.screen.blit(pause_msg_text, pause_msg_rect)

if __name__ == "__main__":
    game = Game()
    game.main_menu()
