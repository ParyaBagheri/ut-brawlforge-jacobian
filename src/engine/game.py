import pygame, time, random
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

        # Load all assets
        AssetManager.load_assets()
        # Track which music is playing
        self.current_music_state = None

        self.Fired_bullets_list = []

        #self.player = Player(self)
        self.camera_x = 0
        self.enemies = pygame.sprite.Group()
        enemy = Enemy(self)
        self.enemies.add(enemy)

        self.isGameover = False

        self.level = None
        self.state = "main_menu"
        self.mode = "single_player"
        self.player = None
        self.other_player = None
        self.powerup_spawn_interval = 10
        self.last_powerup_spawn = time.time()

    def main_menu(self):
        #self.screen.fill((0, 0, 0))
        background = pygame.image.load(background_path)
        background = pygame.transform.scale(background, (800,600))
        self.screen.blit(background, (0,0))
        MENU_PLAY = Button(self, None, [400, 100], "PLAY","OCRAEXT", 50, (255,255,255), (0,146,155))
        MENU_HOWTO = Button(self, None, [400, 300], "HOW TO PLAY",'OCRAEXT', 50, 'white', (0, 146, 155))
        MENU_MULTIPLAYER = Button(self, None, [400, 500], "MULTIPLAYER", "OCRAEXT", 50, 'white', (0, 146, 155)) 
        MENU_MOUSE_POS = pygame.mouse.get_pos
        def main_menu_render():        
            MENU_PLAY.draw(MENU_MOUSE_POS())
            MENU_HOWTO.draw(MENU_MOUSE_POS())
            MENU_MULTIPLAYER.draw(MENU_MOUSE_POS())
        def main_menu_event_handler():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if MENU_PLAY.is_pressed(MENU_MOUSE_POS()):
                        self.state = "char_menu"
                    if MENU_HOWTO.is_pressed(MENU_MOUSE_POS()):
                        self.state = "how_to_play"    
                    if MENU_MULTIPLAYER.is_pressed(MENU_MOUSE_POS()):
                        self.mode ="multiplayer"
                        self.state = "char_menu"
                        
        while self.state == "main_menu":
            main_menu_render()
            main_menu_event_handler()
            pygame.display.flip()
            self.clock.tick(config.FPS)

    def mp_win(self):
        if self.other_player :
            if self.other_player.health == 0:
                return True
        return False
    def mp_lose(self):
        if self.player :
            if self.player.health == 0 :
                return True
        return False
    def how_to_play(self) :
        background = pygame.image.load(background_path)
        background = pygame.transform.scale(background, (800,600))
        self.screen.blit(background, (0,0))
        BACK = Button(self, None, [50, 550], "BACK", "OCRAEXT", 50, 'white', (0, 146, 155)) 
        HOW_TO_PLAY_MOUSE_POS = pygame.mouse.get_pos
        
        demo_state = "idle"
        demo_direction ="right"
        demo_frames = AssetManager.player_images["knight"]
        demo_image = demo_frames["idle"][0]
        demo_rect = demo_image.get_rect(topleft=(500, 250))
        demo_current_frame = 0
        demo_can_jump = True
        demo_can_attack = True
        # keys' animations 
        A_key_is_pressed = False
        A_key_frames = AssetManager.UI_images["A_key"]
        A_key_image = A_key_frames[0]
        A_current_frame = 0
        A_rect = A_key_image.get_rect(topleft=( 100, 120))
        D_key_is_pressed = False
        D_key_frames = AssetManager.UI_images["D_key"]
        D_key_image = D_key_frames[0]
        D_current_frame = 0
        D_rect = D_key_image.get_rect(topleft=( 100, 240))
        SPACE_key_is_pressed = False
        SPACE_key_frames = AssetManager.UI_images["SPACE_key"]
        SPACE_key_image = SPACE_key_frames[0]
        SPACE_current_frame = 0
        SPACE_rect = SPACE_key_image.get_rect(topleft=( 100, 360))
        SHIFT_key_is_pressed = False
        SHIFT_key_frames = AssetManager.UI_images["SHIFT_key"]
        SHIFT_key_image = SHIFT_key_frames[0]
        SHIFT_current_frame = 0 
        SHIFT_rect = SHIFT_key_image.get_rect(topleft=( 100, 480))
        def how_to_play_render():        
            BACK.draw(HOW_TO_PLAY_MOUSE_POS())
            self.screen.blit (demo_image,demo_rect)
            self.screen.blit (A_key_image,A_rect)
            self.screen.blit (D_key_image,D_rect)
            self.screen.blit (SPACE_key_image,SPACE_rect)
            self.screen.blit (SHIFT_key_image,SHIFT_rect)
            
        def how_to_play_event_handler():
            nonlocal demo_current_frame
            nonlocal demo_state
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN :
                    if event.button == 1 : #left mouse button
                        if demo_state != "attack" :
                            demo_current_frame = 0
                        demo_state = "attack"
                    if BACK.is_pressed(HOW_TO_PLAY_MOUSE_POS()):
                        self.state = "main_menu"
            
        def how_to_play_update() :
            nonlocal demo_state 
            nonlocal demo_direction 
            nonlocal demo_frames 
            nonlocal demo_image 
            nonlocal demo_current_frame 
            nonlocal demo_can_jump 
            nonlocal demo_can_attack 
            # demo animation update
            if demo_direction == "right" :
                demo_image = demo_frames[demo_state][int(demo_current_frame)]
            else :
                demo_image = pygame.transform.flip(demo_frames[demo_state][int(demo_current_frame)], True, False)
            demo_current_frame += config.PLAYER_FRAMES_SPEED
            if(demo_current_frame >= len(demo_frames[demo_state])) :
                demo_current_frame = 0
                if demo_state == "jumping" :
                    demo_can_jump = True
                    demo_state = "idle"
                if demo_state == "attack" :
                    demo_can_attack = True
                    demo_state = "idle"
            keys = pygame.key.get_pressed() 
            if keys[pygame.K_a] :
                if demo_state != "run" :
                    demo_current_frame = 0
                demo_direction ="left"
                demo_state = "run"
            elif keys[pygame.K_d] :
                if demo_state != "run" :
                    demo_current_frame = 0
                demo_direction ="right"
                demo_state = "run"
            elif keys[pygame.K_SPACE] and demo_can_jump :
                demo_state = "jumping"
                demo_current_frame = 0
                demo_can_jump = False
            elif (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] )and demo_can_attack:
                if demo_state != "attack":
                    demo_current_frame = 0
                    demo_can_attack = False
                demo_state = "attack" 
            else :
                if demo_state != "idle" :
                    demo_current_frame =0
                demo_state ="idle"
            update_keys(keys)
        def update_keys(keys) :
            nonlocal A_key_is_pressed 
            nonlocal A_key_frames 
            nonlocal A_key_image 
            nonlocal A_current_frame 
            nonlocal D_key_is_pressed 
            nonlocal D_key_frames 
            nonlocal D_key_image 
            nonlocal D_current_frame 
            nonlocal SPACE_key_is_pressed 
            nonlocal SPACE_key_frames 
            nonlocal SPACE_key_image 
            nonlocal SPACE_current_frame 
            nonlocal SHIFT_key_is_pressed 
            nonlocal SHIFT_key_frames 
            nonlocal SHIFT_key_image 
            nonlocal SHIFT_current_frame  
            
            if keys[pygame.K_a] :
                A_key_is_pressed = True
                A_current_frame = 1 
            

            if keys[pygame.K_d] :
                D_key_is_pressed = True
                D_current_frame = 1 
                
            if keys[pygame.K_SPACE]  :
                SPACE_key_is_pressed = True
                SPACE_current_frame = 1
             
            if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] ):
                SHIFT_key_is_pressed = True
                SHIFT_current_frame = 1
                
            if A_key_is_pressed :
                A_key_image = A_key_frames[int(A_current_frame)]
                A_current_frame += 0.15
                if A_current_frame >= len(A_key_frames) :
                    A_current_frame = 0
                    A_key_is_pressed = False
            if D_key_is_pressed :
                D_key_image = D_key_frames[int(D_current_frame)]
                D_current_frame += 0.15
                if D_current_frame >= len(D_key_frames) :
                    D_current_frame = 0
                    D_key_is_pressed = False
            if SPACE_key_is_pressed :
                SPACE_key_image = SPACE_key_frames[int(SPACE_current_frame)]
                SPACE_current_frame += 0.15
                if SPACE_current_frame >= len(SPACE_key_frames) :
                    SPACE_current_frame = 0
                    SPACE_key_is_pressed = False
            if SHIFT_key_is_pressed :
                SHIFT_key_image = SHIFT_key_frames[int(SHIFT_current_frame)]
                SHIFT_current_frame += 0.15
                if SHIFT_current_frame >= len(SHIFT_key_frames) :
                    SHIFT_current_frame = 0
                    SHIFT_key_is_pressed = False
        while self.state == "how_to_play":
            how_to_play_render()
            how_to_play_event_handler()
            how_to_play_update()
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
                        self.player = Player(self, character_type='knight')
                        if self.mode == "single_player" :
                            self.state = "map_menu"
                            
                        elif self.mode == "multiplayer" :
                            self.other_player = Player(self, 'wizard', 3300)
                            self.level = Level("multiplayer", self, 3350, self.mp_win, self.mp_lose)
                            self.state = "playing"
                            
                    elif CHAR_2.is_pressed(CHAR_MENU_MOUSE_POS()):
                        self.player = Player(self, character_type='girl')
                        if self.mode == "single_player" :
                            self.state = "map_menu"
                            
                        elif self.mode == "multiplayer" :
                            self.other_player = Player(self, 'knight', 3300)
                            self.level = Level("multiplayer", self, 3350, self.mp_win, self.mp_lose)
                            self.state = "playing"
                                               
                    elif CHAR_3.is_pressed(CHAR_MENU_MOUSE_POS()):
                        self.player = Player(self, character_type='wizard')
                        if self.mode == "single_player" :
                            self.state = "map_menu"
                            
                        elif self.mode == "multiplayer" :
                            self.other_player = Player(self, 'girl', 3300)
                            self.level = Level("multiplayer", self, 3350, self.mp_win, self.mp_lose)
                            self.state = "playing"
                            

        while self.state == "char_menu":
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
                        self.level = Level("forest", self, 3350, self.forest_win)
                        
                    if MAP_2.is_pressed(MAP_MENU_MOUSE_POS()):
                        self.state = "playing"
                        self.level = Level("desert", self, 6600, self.desert_win)
                        
                    if MAP_3.is_pressed(MAP_MENU_MOUSE_POS()):
                        self.state = "playing"
                        self.level = Level("lost_city", self, 8000, self.lostcity_win)
                        
                    if MAP_4.is_pressed(MAP_MENU_MOUSE_POS()):
                        self.state = "playing"
                        self.level = Level("underwater", self, 16000, self.underwater_win)
                        

        while self.state == "map_menu":
            map_menu_render()
            map_menu_event_handler()
            pygame.display.flip()
            self.clock.tick(config.FPS)

    def finish_menu(self):
        self.screen.fill((0,0,0))
        self.player.reset()
        AssetManager.UI_sounds["win"].play()
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
                        self.restart()
                        
                    elif NEXTLEVEL_BUTTON.is_pressed(MOUSE_POS()):
                        self.state = "playing"
                        if self.level.name == "forest":
                            self.level = Level("desert", self, 6600, self.desert_win)
                        elif self.level.name == "desert":
                            self.level = Level("lost_city", self, 8000,self.lostcity_win)
                        elif self.level.name == "lost_city":
                            self.level = Level("underwater", self, 16000, self.underwater_win)
                        self.restart()
                        
                    elif MENU_BUTTON.is_pressed(MOUSE_POS()):
                        self.state = "main_menu"
                        
                        
        while self.state == "won" :
            finish_menu_render()
            finish_menu_event_handler()
            pygame.display.flip()
            self.clock.tick(config.FPS)

    def lose_screen(self):
        self.screen.fill((0, 0, 0))
        lose_font = pygame.font.Font("src/assets/fonts/OCRAEXT.ttf", 72)
        lose_msg = lose_font.render("YOU LOST !", True, 'yellow')
        text_rect = lose_msg.get_rect()
        text_rect.center = (self.screen_width//2, 200)
        self.screen.blit(lose_msg, text_rect)
    def win_screen(self):
        self.screen.fill((0, 0, 0))
        win_font = pygame.font.Font("src/assets/fonts/OCRAEXT.ttf", 72)
        win_msg = win_font.render("YOU WIN!", True, 'yellow')
        text_rect = win_msg.get_rect()
        text_rect.center = (self.screen_width//2, 200)
        self.screen.blit(win_msg, text_rect)

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
    def spawn_random_powerup(self):
        from src.engine.collectible import Powerup
        powerup_types = ['shield', 'doublejump', 'damageboost', 'health']
        p_type = random.choice(powerup_types)

        valid_platforms = [p for p in self.level.platforms if isinstance(p, Platform) and p.visible]
        if not valid_platforms:
            return

        platform = random.choice(valid_platforms)
        x = platform.rect.centerx
        y = platform.rect.top - 50

        new_powerup = Powerup(self, x, y, p_type)
        self.level.powerups.append(new_powerup)

    def update_dimensions(self):
        # Update screen and ground dimensions based on current window size
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.ground_rect = pygame.Rect(0, self.screen_height - config.BASE_GROUND_HEIGHT, self.screen_width * 10, config.BASE_GROUND_HEIGHT)

    def update_camera(self):
        # Camera follows the player horizontally
        
        self.camera_x = self.player.rect.centerx - self.screen_width // 2
        max_camera_x = self.level.width - self.screen_width
        self.camera_x = max(0, min(self.camera_x, max_camera_x))
        if self.camera_x + self.screen_width > config.FINISHING_POINTS[self.level.name] :
            self.camera_x = config.FINISHING_POINTS[self.level.name] - self.screen_width
 
    def run(self):
        while True:
            self.music_manager()
            if self.state == "playing" or self.state == "paused" or self.state == "gameover" :
                self.handle_events()
                self.update()
                self.draw()
                pygame.display.flip()
                self.clock.tick(60)
            else :
                if self.state == "main_menu" :
                    self.main_menu()
                if self.state == "how_to_play":
                    self.how_to_play()
                if self.state == "char_menu" :
                    self.character_menu()
                if self.state == "map_menu" :
                    self.map_menu()
                if self.state == "won":
                    self.finish_menu()
            

    def music_manager(self):
        if self.current_music_state == None :
            if self.state == "playing" :
                pygame.mixer.music.load(config.MUSIC_PATHS["game_music"])
                pygame.mixer.music.set_volume(0.1)
                pygame.mixer.music.play (loops=-1)
                
                self.current_music_state = "playing"
            elif self.state == "main_menu" :
                pygame.mixer.music.load(config.MUSIC_PATHS["menu_music"])
                pygame.mixer.music.set_volume(0.1)
                pygame.mixer.music.play (loops=-1)
                
                self.current_music_state = "menu"
        elif self.current_music_state == "playing" :
            if self.state != "playing" :
                pygame.mixer.music.stop()
                if self.state == "main_menu" :
                    pygame.mixer.music.load(config.MUSIC_PATHS["menu_music"])
                    pygame.mixer.music.set_volume(0.1)
                    pygame.mixer.music.play (loops=-1)
                    
                    self.current_music_state = "menu"
                else :
                    self.current_music_state = None
        elif self.current_music_state == "menu" :
            if self.state == "playing" :
                pygame.mixer.music.stop()
                pygame.mixer.music.load(config.MUSIC_PATHS["game_music"])
                pygame.mixer.music.set_volume(0.1)
                pygame.mixer.music.play (loops=-1)
                
                self.current_music_state = "playing"


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
            if self.mode != "multiplayer" and self.level.won() :
                self.state = "won"
                
                
            if self.mode == "multiplayer" :
                if self.level.won():
                    self.player.reset()
                    self.win_screen()
                if self.level.lost() :
                    self.player.reset()
                    self.lose_screen()
                #self.other_player.update(self.level.platforms, self.enemies, self.level.powerups)
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
            if self.mode == "multiplayer" :
                for bullet in self.Fired_bullets_list:
                    if isinstance(bullet, Bullet) and self.other_player:
                        if bullet.owner == self.player and bullet.rect.colliderect(self.other_player.rect):
                            if not self.other_player.is_invincible:
                                self.other_player.health -= bullet.damage
                                self.other_player.is_invincible = True
                                bullet.visible = False

            # Remove dead enemies and spawn new ones
            for enemy in self.enemies:
                if enemy.rect.x <= 0 + self.camera_x or enemy.health <= 0 or self.isGameover == True :
                    enemy.kill()
                    new_enemy = Enemy(self)
                    self.enemies.add(new_enemy)

            # spawning random powerups :
            if self.mode == "multiplayer":
                current_time = time.time()
                if current_time - self.last_powerup_spawn > self.powerup_spawn_interval:
                    self.spawn_random_powerup()
                    self.last_powerup_spawn = current_time

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
        self.screen.blit(self.level.background_layers,(0 - int(self.camera_x/10), 0))
        # Draw platforms and ground
        for platform in self.level.platforms:
            if isinstance(platform, Platform) and platform.visible == True:
                platform.draw(self.screen, self.camera_x)
            '''elif not isinstance(platform, Platform) :
                pygame.draw.rect(self.screen, (34, 139, 34), 
                               pygame.Rect(platform.x - self.camera_x, 
                                          platform.y, 
                                          platform.width, 
                                          platform.height))'''
        # Draw map
        if self.level.map != None:
            self.screen.blit(self.level.map,( 0 - self.camera_x , 0))
            

        # Draw player
        if(self.player.visible == True) :
            if self.player.direction == "left" :
                self.screen.blit( pygame.transform.flip(self.player.image,True,False), (self.player.rect.x - self.camera_x, self.player.rect.y))
            else :
                self.screen.blit( self.player.image, (self.player.rect.x - self.camera_x, self.player.rect.y))
        if self.other_player :
            self.screen.blit(self.other_player.image, (self.other_player.rect.x - self.camera_x, self.player.rect.y))

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
        health_display = font.render("Your Health: " + str(self.player.health), True, 'white')
        self.screen.blit(health_display, (20,20))
        heart = AssetManager.UI_images["heart"]
        if self.player.health >= 0:
            for i in range(0,self.player.health):
                self.screen.blit(heart, (40 + 30*i , 40))
        if self.other_player:
            other_health_display = font.render("Enemy: " + str(self.other_player.health), True, 'red')
            self.screen.blit(other_health_display, (20, 80))
                
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
