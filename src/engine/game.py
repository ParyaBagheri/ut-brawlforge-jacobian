import pygame
import sys
import os

import config


background_path = os.path.join("src", "assets", "images", "background.jpg")

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
from src.engine.level import Level
from src.engine import data_loader
from src.engine.assetmanager import AssetManager

class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.BASE_SCREEN_WIDTH, config.BASE_SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Platformer Game")
        self.clock = pygame.time.Clock()
        self.is_paused = False
        self.update_dimensions()
        self.PAUSE_BUTTON = Button(self, None, [750,10], "Pause", 'Blox2', 30, 'white', 'grey') #Add pause button image later

        #self.platforms = self.platform_maker()


        AssetManager.load_assets()

        self.Fired_bullets_list = []

        #self.player = Player(self)
        self.camera_x = 0
        self.enemies = pygame.sprite.Group()
        enemy = Enemy(self)
        self.enemies.add(enemy)

        self.isGameover = False

        self.level = None
        self.state = "main_menu"

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
                        self.state = "char_menu"
                        self.character_menu()
        while True:
            main_menu_render()
            main_menu_event_handler()
            pygame.display.flip()
            self.clock.tick(config.FPS)

    def character_menu(self):
        background = pygame.image.load(background_path)
        background = pygame.transform.scale(background, (800,600))
        self.screen.blit(background, (0,0))

        char_menu_font = pygame.font.SysFont('OCR A Extended', 45)
        char_menu_text = char_menu_font.render("Choose a character!", True, 'indigo')
        char_menu_text_rect = char_menu_text.get_rect(center= (self.screen_width // 2, self.screen_height//6))
        self.screen.blit(char_menu_text, char_menu_text_rect)

        self.screen.blit(char_menu_text, char_menu_text_rect)
        CHAR_1 = Button(self, AssetManager.player_images["knight"]["idle"], [self.screen_width//4,self.screen_height//2], "knight",'OCRAEXT', 40, (0, 38, 21), (0, 89, 21))
        CHAR_2 = Button(self, AssetManager.player_images["girl"]["idle"], [3 *self.screen_width//4, self.screen_height//2], "girl", 'OCRAEXT', 40, (117, 96,0), (42, 32, 0))
        CHAR_3 = Button(self, AssetManager.player_images["wizard"]["idle"], [self.screen_width//4, 5 * self.screen_height//6], "wizard","OCRAEXT", 40, (255, 181, 118), (81, 1, 109))
        CHAR_4 = Button(self, None, [3 * self.screen_width//4, 5 * self.screen_height//6], "char 4","OCRAEXT", 40, (0, 13, 72), (229, 134, 169))
        CHAR_MENU_MOUSE_POS = pygame.mouse.get_pos
        def char_menu_render():
            CHAR_1.draw(CHAR_MENU_MOUSE_POS())
            CHAR_2.draw(CHAR_MENU_MOUSE_POS())
            CHAR_3.draw(CHAR_MENU_MOUSE_POS())
            CHAR_4.draw(CHAR_MENU_MOUSE_POS())

        def char_menu_events():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if CHAR_1.is_pressed(CHAR_MENU_MOUSE_POS()):
                        self.state = "map_menu"
                        self.player = Player(self, character_type='knight')
                        self.map_menu()
                    elif CHAR_2.is_pressed(CHAR_MENU_MOUSE_POS()):
                        self.state = "map_menu"
                        self.player = Player(self, character_type='girl')
                        self.map_menu()
                    elif CHAR_3.is_pressed(CHAR_MENU_MOUSE_POS()):
                        self.state = "map_menu"
                        self.player = Player(self, character_type='wizard')
                        self.map_menu()

        while True:
            char_menu_render()
            char_menu_events()
            pygame.display.flip()
            self.clock.tick(config.FPS)

    def forest_win(self):
        if self.player.rect.x >= 3200 :
            return True
        return False
    def desert_win(self):
        if self.player.rect.x >= 6000 :
            return True
        return False
    def lostcity_win(self):
        if self.player.rect.x >= 7700 :
            return True
        return False
    def underwater_win(self):
        if self.player.rect.x >= 15600 :
            return True
        return False
    

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
        MAP_1 = Button(self, None, [self.screen_width//4,self.screen_height//2], "Forest",'OCRAEXT', 40, (0, 38, 21), (0, 89, 21))
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
                        self.state = "playing"
                        self.level = Level("forest", self, self.forest_win)
                        self.run()
                    if MAP_2.is_pressed(MAP_MENU_MOUSE_POS()):
                        self.state = "playing"
                        self.level = Level("desert", self, self.desert_win)
                        self.run()
                    if MAP_3.is_pressed(MAP_MENU_MOUSE_POS()):
                        self.state = "playing"
                        self.level = Level("lost_city", self, self.lostcity_win)
                        self.run()
                    if MAP_4.is_pressed(MAP_MENU_MOUSE_POS()):
                        self.state = "playing"
                        self.level = Level("underwater", self, self.underwater_win)
                        self.run()

        while True:
            map_menu_render()
            map_menu_event_handler()
            pygame.display.flip()
            self.clock.tick(config.FPS)

    def finish_menu(self):
        self.screen.fill((0,0,0))
        self.restart()
        RESTART_BUTTON = Button(self, None, [400, 150], "restart", 'OCRAEXT', 50, 'white', 'yellow')
        NEXTLEVEL_BUTTON = Button(self, None, [400, 250], "next level", 'OCRAEXT', 50, 'white', 'yellow')
        MENU_BUTTON = Button(self, None, [400, 350], "main menu", 'OCRAEXT', 50, 'white', 'yellow')
        MOUSE_POS = pygame.mouse.get_pos
        def finish_menu_render():
            RESTART_BUTTON.draw(MOUSE_POS())
            if self.level.name != "underwater" :
                NEXTLEVEL_BUTTON.draw(MOUSE_POS())
            MENU_BUTTON.draw(MOUSE_POS())
        def finish_menu_event_handler():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if RESTART_BUTTON.is_pressed(MOUSE_POS()):
                        self.state = "playing"
                        self.run()
                    if NEXTLEVEL_BUTTON.is_pressed(MOUSE_POS()):
                        self.state = "playing"
                        if self.level.name == "forest":
                            self.level = Level("desert", self, self.desert_win)
                        elif self.level.name == "desert":
                            self.level = Level("lost_city", self, self.lostcity_win)
                        elif self.level.name == "lost_city":
                            self.level = Level("underwater", self, self.underwater_win)
                        self.run()
                    if MENU_BUTTON.is_pressed(MOUSE_POS()):
                        self.state = "main_menu"
                        self.main_menu()
        while True :
            finish_menu_render()
            finish_menu_event_handler()
            pygame.display.flip()
            self.clock.tick(config.FPS)



    def platform_maker(self):
        platform_img = pygame.image.load("src/assets/images/platform.png").convert_alpha()
        platforms = [
            Platform(self, 300, 400, 150, 20, 'solid', image=platform_img),
            Platform(self, 600, 300, 150, 20, 'solid', image=platform_img),
            Platform(self, 750, 300, 250, 20, 'solid'), #Fragile platform
            Platform(self, 1050, 200, 100, 20, 'solid'), # Bonus on this platform
            Platform(self, 1140, 560 - config.BASE_GROUND_HEIGHT, 50, 40, 'bouncy'), #Bouncy platform
            Platform(self, 1250, 300, 300, 20, 'solid'),
            Platform(self, 1400, 600 - config.BASE_GROUND_HEIGHT, 350, 20, 'slowing'), #Muddy platform
            Platform(self, 1630, 200, 100, 20, 'timed'),
            Platform(self, 1700, 300, 100, 20, 'solid'),
            Platform(self, 1800, 300, 250, 20, 'slowing'),
            Platform(self, 2250, 200, 100, 20, 'timed'),
            Platform(self, 2400, 300, 300, 20, 'solid'),
            Platform(self, 2800, 200, 100, 20, 'timed'),
            Platform(self, 3000, 100, 100, 20, 'timed'),
            Platform(self, 3150, 250, 200, 100, 'solid'), #Finish platform
            #Platform(self, 3050, 560 - config.BASE_GROUND_HEIGHT, 50, 40, 'bouncy')
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
            #elif event.type == pygame.VIDEORESIZE:
                # Resize window and update dimensions
                #self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                #self.update_dimensions()
            elif ((event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or 
                  (event.type == pygame.MOUSEBUTTONDOWN and self.PAUSE_BUTTON.is_pressed(GAME_MOUSE_POS()))) and self.state != "gameover" :
                # Press esc or pause button to pause
                self.state = "paused"

            elif event.type == pygame.MOUSEBUTTONDOWN :
                if event.button == 1 : #left mouse button
                    self.player.is_shooting = True

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.state != "paused" and self.state != "gameover":
                #if event.button == 1 : #left mouse button
                    self.player.shoot()
            elif (event.type == pygame.KEYDOWN or (event.type == pygame.MOUSEBUTTONDOWN and self.PAUSE_BUTTON.is_pressed(GAME_MOUSE_POS()))) and self.state == "paused": # press space to resume
                if event.key == pygame.K_SPACE:
                    self.state = "playing"
            # Restart after game over
            elif self.state == "gameover" and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.restart()

    def update(self):
        #if self.isGameover == False and self.is_paused == False:
        if self.state == "playing" and self.level != None:
            if self.level.won() :
                self.state = "won"
                self.player.reset()
                self.finish_menu()
            self.player.update(self.level.platforms, self.enemies, self.level.powerups)
            self.update_camera()

            for platform in self.level.platforms :
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
            for powerup in self.level.powerups :
                powerup.update()


    def draw(self):
        self.screen.fill((135, 206, 235))  # Sky blue background
        '''if self.level.background_layers is not None:
            for image, scroll_factor in self.level.background_layers :
                offset = int(self.camera_x * scroll_factor)
                scaled_image = pygame.transform.scale(image, (self.screen_width, self.screen_height))
                image_width = scaled_image.get_width()
                start_x = -offset % image_width
                #self.screen.blit(scaled_image, (-offset, 0))
            for i in range(-1, self.screen_width // image_width + 2):
                self.screen.blit(scaled_image, (start_x + i * image_width, 0))
'''
        # Draw platforms and ground
        for platform in self.level.platforms:
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
            if self.player.direction == "left" :
                self.screen.blit( pygame.transform.flip(self.player.image,True,False), (self.player.rect.x - self.camera_x, self.player.rect.y))
            else :
                self.screen.blit( self.player.image, (self.player.rect.x - self.camera_x, self.player.rect.y))

        # Draw all fired bullets with camera offset
        for bullet in self.Fired_bullets_list :
            if isinstance(bullet, Bullet) :
                self.screen.blit(bullet.image, (bullet.rect.x - self.camera_x, bullet.rect.y))

        # Draw enemies
        self.draw_enemies()
        # Draw powerups 
        for powerup in self.level.powerups :
            powerup.draw()
        # Show health
        self.show_health()
        # Draw pause button 
        GAME_MOUSE_POS = pygame.mouse.get_pos
        self.PAUSE_BUTTON.draw(GAME_MOUSE_POS())
        if self.state == "paused": 
            self.pause_render()
        # Show game over
        if self.state == "gameover":
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
        self.state = "gameover"
        self.player.color = (0, 0, 0)
    def gameover_render(self):
        gameover_font = pygame.font.Font("src/assets/fonts/OCRAEXT.ttf", 72)
        gameover_message = gameover_font.render("GAME OVER!", True, 'black')
        text_rect = gameover_message.get_rect()
        text_rect.center = (self.screen_width //2, self.screen_height//2)
        self.screen.blit(gameover_message, text_rect)

    def restart(self):
        self.player.reset()
        for platform in self.level.platforms :
            if isinstance(platform, Platform):
                platform.activated = False
                platform.visible = True
        for powerup in self.level.powerups :
            powerup.visible = True
            powerup.timer = 0
            powerup.is_inview = False
        
        self.state = "playing"

    def pause_render(self):
        pause_msg_font =  pygame.font.Font("src/assets/fonts/OCRAEXT.ttf", 50)
        pause_msg_text = pause_msg_font.render("Press space to resume!", True, 'indigo')
        pause_msg_rect = pause_msg_text.get_rect(center=(self.screen_width//2, self.screen_height//2))
        self.screen.blit(pause_msg_text, pause_msg_rect)

if __name__ == "__main__":
    game = Game()
    game.main_menu()
