import pygame, time, random
import sys
import os

import config


background_path = os.path.join("src", "assets", "images", "background.jpg")

# Fonts 
pygame.font.init()
font = pygame.font.SysFont('Arial',  32, True, False)
font2 = pygame.font.Font("src/assets/fonts/MinimalPixelFont.ttf",50)
font3 = pygame.font.Font("src/assets/fonts/MinimalPixelFont.ttf", 30)
heartfont = pygame.font.SysFont('Segoe UI Symbol', 40)
gameoverfont = pygame.font.SysFont('OCR A Extended', 72)
loadingscreen_font = pygame.font.SysFont('OCR A Extended', 36)

from src.engine.bullet import Bullet
from src.engine.player import Player
from src.engine.platform import Platform
from src.engine.enemy import Enemy, Freezerenemy
from src.engine.enemy import Bomber
from src.engine.button import Button
from src.engine.level import Level
from src.engine import data_loader
from src.engine.assetmanager import AssetManager
from src.engine.collectible import Powerup
from src.engine.client import Client

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
        self.enemies = None
        #self.player = Player(self)
        self.camera_x = 0
        
        self.isGameover = False

        self.level = None
        self.state = "main_menu"
        self.mode = "single_player"
        self.player = None
        self.client = None
        self.other_players = []
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
                        self.mode = "single_player"
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
        for player in self.other_players :
            if isinstance(player,Player) and not player.is_dead :
                if player.team != self.player.team :
                    return False
        self.state = "won"
        return True  
    def mp_lose(self):
        if self.player :
            if self.player.is_dead :
                return True
        return False
    def how_to_play(self) :
        background = pygame.image.load(background_path)
        background = pygame.transform.scale(background, (800,600))
        self.screen.blit(background, (0,0))
        BACK = Button(self, None, [60, 550], "BACK", "OCRAEXT", 40, 'white', (0, 146, 155)) 
        HOW_TO_PLAY_MOUSE_POS = pygame.mouse.get_pos
        demo_state = "idle"
        demo_direction ="right"
        demo_frames = AssetManager.player_images["knight"]
        demo_image = demo_frames["idle"][0]
        demo_rect = demo_image.get_rect(topleft=(500, 250))
        demo_current_frame = 0
        demo_can_jump = True
        demo_attack_animation = False
        font = pygame.font.Font("src/assets/fonts/MinimalPixelFont.ttf",50)
        text1 =font.render ('Move right', True,'black' )
        text1_rect =text1.get_rect()
        text1_rect.center = (80 , 100 )
        text2 = font.render ('Move left', True,'black' )
        text2_rect =text2.get_rect()
        text2_rect.center = (75 , 220 )
        text3 = font.render ('Jump', True,'black' )
        text3_rect =text3.get_rect()
        text3_rect.center = (50 , 340 )
        text4 = font.render ('Shoot', True,'black' )
        text4_rect = text4.get_rect()
        text4_rect.center = (50 , 460 )
        text5 = font.render ('or left mouse button',True,'black')
        text5_rect =text5.get_rect()
        text5_rect.center = (480 , 460 )
        # keys' animations 
        A_key_is_pressed = False
        A_key_frames = AssetManager.UI_images["A_key"]
        A_key_image = A_key_frames[0]
        A_current_frame = 0
        A_rect = A_key_image.get_rect(topleft=( 185, 80))
        D_key_is_pressed = False
        D_key_frames = AssetManager.UI_images["D_key"]
        D_key_image = D_key_frames[0]
        D_current_frame = 0
        D_rect = D_key_image.get_rect(topleft=( 180, 200))
        SPACE_key_is_pressed = False
        SPACE_key_frames = AssetManager.UI_images["SPACE_key"]
        SPACE_key_image = SPACE_key_frames[0]
        SPACE_current_frame = 0
        SPACE_rect = SPACE_key_image.get_rect(topleft=( 140, 320))
        SHIFT_key_is_pressed = False
        SHIFT_key_frames = AssetManager.UI_images["SHIFT_key"]
        SHIFT_key_image = SHIFT_key_frames[0]
        SHIFT_current_frame = 0 
        SHIFT_rect = SHIFT_key_image.get_rect(topleft=( 140, 440))
        def how_to_play_render():
            self.screen.blit(background, (0,0))        
            BACK.draw(HOW_TO_PLAY_MOUSE_POS())
            self.screen.blit (pygame.transform.scale(demo_image, (75,120)),demo_rect)
            self.screen.blit (A_key_image,A_rect)
            self.screen.blit (D_key_image,D_rect)
            self.screen.blit (SPACE_key_image,SPACE_rect)
            self.screen.blit (SHIFT_key_image,SHIFT_rect)
            self.screen.blit(text1, text1_rect)
            self.screen.blit(text2, text2_rect)
            self.screen.blit(text3, text3_rect)
            self.screen.blit(text4, text4_rect)
            self.screen.blit(text5, text5_rect)
        def how_to_play_event_handler():
            nonlocal demo_current_frame
            nonlocal demo_state
            nonlocal demo_attack_animation
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN :
                    if event.button == 1 : #left mouse button
                        if demo_state != "attack" :
                            demo_current_frame = 0
                        demo_state = "attack"
                        demo_attack_animation = True
                    if BACK.is_pressed(HOW_TO_PLAY_MOUSE_POS()):
                        self.state = "main_menu"
            
        def how_to_play_update() :
            nonlocal demo_state 
            nonlocal demo_direction 
            nonlocal demo_frames 
            nonlocal demo_image 
            nonlocal demo_current_frame 
            nonlocal demo_can_jump 
            nonlocal demo_attack_animation 
            # demo animation update
            if demo_direction == "right" :
                demo_image = demo_frames[demo_state][int(demo_current_frame)]
            else :
                demo_image = pygame.transform.flip(demo_frames[demo_state][int(demo_current_frame)], True, False)
            demo_current_frame += config.PLAYER_FRAMES_SPEED
            if(demo_current_frame >= len(demo_frames[demo_state])) :
                demo_current_frame = 0
                if demo_attack_animation :
                    demo_attack_animation = False
                    demo_state = "idle"
                
            keys = pygame.key.get_pressed() 
            if not demo_attack_animation :
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
                elif keys[pygame.K_SPACE] :
                    if demo_state != "jumping" :
                        demo_current_frame = 0
                    demo_state = "jumping"
                    
                elif (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] ):
                    demo_current_frame = 0
                    demo_state = "attack" 
                    demo_attack_animation = True
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

        char_menu_font = pygame.font.Font("src/assets/fonts/MinimalPixelFont.ttf",80)
        char_menu_text = char_menu_font.render("Choose a character!", True, 'indigo')
        char_menu_text_rect = char_menu_text.get_rect(center= (self.screen_width // 2, self.screen_height//6))
        self.screen.blit(char_menu_text, char_menu_text_rect)

        self.screen.blit(char_menu_text, char_menu_text_rect)
        CHAR_1 = Button(self, AssetManager.player_images["knight"]["idle"], [self.screen_width//4,self.screen_height//2], "knight",'OCRAEXT', 40, (0, 38, 21), (0, 89, 21))
        CHAR_2 = Button(self, AssetManager.player_images["girl"]["idle"], [3 *self.screen_width//4, self.screen_height//2], "girl", 'OCRAEXT', 40, (117, 96,0), (42, 32, 0))
        CHAR_3 = Button(self, AssetManager.player_images["wizard"]["idle"], [self.screen_width//4, 5 * self.screen_height//6], "wizard","OCRAEXT", 40, (255, 181, 118), (81, 1, 109))
        CHAR_4 = Button(self, AssetManager.player_images["TV"]["idle"], [3 *self.screen_width//4, 5 * self.screen_height//6], "TV","OCRAEXT", 40, (0, 13, 72), (229, 134, 169))
        CHAR_MENU_MOUSE_POS = pygame.mouse.get_pos

        character_type = None
        def char_menu_render():
            CHAR_1.draw(CHAR_MENU_MOUSE_POS())
            CHAR_2.draw(CHAR_MENU_MOUSE_POS())
            CHAR_3.draw(CHAR_MENU_MOUSE_POS())
            CHAR_4.draw(CHAR_MENU_MOUSE_POS())

        def char_menu_events():
            nonlocal character_type
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if CHAR_1.is_pressed(CHAR_MENU_MOUSE_POS()):
                        
                        if self.mode == "single_player" :
                            self.state = "map_menu"
                            self.player = Player(self, character_type='knight')
                            
                        elif self.mode == "multiplayer" :
                            character_type = "knight"
                            self.level = Level("multiplayer", self, 3200)
                            self.state = "game_request_menu"
                            
                    elif CHAR_2.is_pressed(CHAR_MENU_MOUSE_POS()):
                        
                        if self.mode == "single_player" :
                            self.state = "map_menu"
                            self.player = Player(self, character_type='girl')
                            
                        elif self.mode == "multiplayer" :
                            character_type = "girl"
                            self.level = Level("multiplayer", self, 3200)
                            self.state = "game_request_menu"
                                               
                    elif CHAR_3.is_pressed(CHAR_MENU_MOUSE_POS()):
                        
                        if self.mode == "single_player" :
                            self.player = Player(self, character_type='wizard')
                            self.state = "map_menu"
                            
                        elif self.mode == "multiplayer" :
                            character_type = "wizard"
                            self.level = Level("multiplayer", self, 3200)
                            self.state = "game_request_menu"
                    
                    elif CHAR_4.is_pressed(CHAR_MENU_MOUSE_POS()):
                        
                        if self.mode == "single_player" :
                            self.player = Player(self, character_type='TV')
                            self.state = "map_menu"
                            
                        elif self.mode == "multiplayer" :
                            character_type = "TV"
                            self.level = Level("multiplayer", self, 3200)
                            self.state = "game_request_menu"
                            

        while self.state == "char_menu":
            char_menu_render()
            char_menu_events()
            pygame.display.flip()
            self.clock.tick(config.FPS)
        if self.state == "game_request_menu" :
            self.game_request_menu(character_type)

    def game_request_menu (self, character_type) :
        background = pygame.image.load(background_path)
        background = pygame.transform.scale(background, (800,600))
        self.screen.blit(background, (0,0))
        request_type = None
        ONEVONE = Button(self,None, [self.screen_width//4,self.screen_height//2], "1v1",'OCRAEXT', 40, (0, 38, 21), (0, 89, 21))
        TWOVTWO = Button(self,None, [3 *self.screen_width//4, self.screen_height//2], "2v2", 'OCRAEXT', 40, (117, 96,0), (42, 32, 0))
        GAME_REQUEST_MOUSE_POS = pygame.mouse.get_pos
        
        def game_request_render():
            ONEVONE.draw(GAME_REQUEST_MOUSE_POS())
            TWOVTWO.draw(GAME_REQUEST_MOUSE_POS())
        def game_request_events():
            for event in pygame.event.get():
                nonlocal request_type
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if ONEVONE.is_pressed(GAME_REQUEST_MOUSE_POS()):
                        request_type = "1v1"
                        self.state = "nickname_menu" 
                              
                    elif TWOVTWO.is_pressed(GAME_REQUEST_MOUSE_POS()):
                        request_type = "2v2"
                        self.state = "nickname_menu" 
                        
                    
        while self.state == "game_request_menu":
            game_request_render()       
            game_request_events()
            pygame.display.flip()
            self.clock.tick(config.FPS)
        if self.state == "nickname_menu" :
            self.nickname_menu(character_type, request_type)                   
    def nickname_menu(self,character_type, request_type):
        
        nickname = ""
        while self.state == "nickname_menu" :
            background = pygame.image.load(background_path)
            background = pygame.transform.scale(background, (800,600))
            self.screen.blit(background, (0,0))
            
            nickname_menu_font = pygame.font.Font("src/assets/fonts/MinimalPixelFont.ttf",80)
            nickname_menu_text = nickname_menu_font.render("Enter your nickname!", True, 'indigo')
            nickname_menu_text_rect = nickname_menu_text.get_rect(center= (self.screen_width // 2, self.screen_height//6))
            self.screen.blit(nickname_menu_text, nickname_menu_text_rect)

            text_font = pygame.font.Font("src/assets/fonts/OCRAEXT.ttf",50)
            nickname_text = text_font.render(nickname, True, 'black')
            text_rect = nickname_text.get_rect(center=(400,300)) 
            self.screen.blit(nickname_text,text_rect) 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN :
                        self.state = "mp_menu" 
                        try :
                            if self.client == None :
                                self.client =  Client(self, nickname, character_type,request_type)
                                self.client.start()
                            else :
                                self.client.new_look(nickname,character_type,request_type)
                        except Exception as e:
                            import traceback
                            print("error", e)
                            traceback.print_exc()
                        break
                    elif event.key == pygame.K_BACKSPACE :
                        nickname = nickname[:-1]
                    else: 
                        nickname += event.unicode
            
            pygame.display.flip()
            self.clock.tick(config.FPS)

        if self.state == "mp_menu" :
            self.multiplayer_menu()

    def waiting_room (self):
        background = pygame.image.load(background_path)
        background = pygame.transform.scale(background, (800,600))
        self.screen.blit(background, (0,0))
        waiting_font = pygame.font.Font("src/assets/fonts/MinimalPixelFont.ttf",80)
        waiting_text = waiting_font.render("waiting", True, 'indigo')
        waiting_text_rect = waiting_text.get_rect(center= (self.screen_width // 2, self.screen_height//2))
        self.screen.blit(waiting_text, waiting_text_rect)
        while self.state == "waiting" :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
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
        background = pygame.image.load(background_path)
        background = pygame.transform.scale(background, (800,600))
        self.screen.blit(background, (0,0))

        map_menu_font = pygame.font.Font("src/assets/fonts/MinimalPixelFont.ttf",80)
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
                    pygame.quit()
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
    def multiplayer_menu(self):
        background = pygame.image.load(background_path)
        background = pygame.transform.scale(background, (800,600))
        self.screen.blit(background, (0,0))
        B1 = Button(self, None, [400, 100], "Match with local players", 'OCRAEXT', 40, 'indigo', 'pink')
        B2 = Button(self, None, [400, 200], "Check invites", 'OCRAEXT', 40, 'indigo', 'pink')
        B3 = Button(self, None, [400, 300], "invite a friend", 'OCRAEXT', 40, 'indigo', 'pink')
        B4 = Button(self, None, [400, 500], "main menu", 'OCRAEXT', 40, 'indigo', 'pink')
        B5 = Button(self, None, [400, 400], "my id", 'OCRAEXT', 40, 'indigo', 'pink')
        MP_MENU_MOUSE_POS = pygame.mouse.get_pos
        def mp_menu_render():
            B1.draw(MP_MENU_MOUSE_POS())
            B2.draw(MP_MENU_MOUSE_POS())
            B3.draw(MP_MENU_MOUSE_POS())
            B4.draw(MP_MENU_MOUSE_POS())
            B5.draw(MP_MENU_MOUSE_POS())
        def mp_menu_event_handler():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if B1.is_pressed(MP_MENU_MOUSE_POS()):
                        self.state = "waiting"  
                    if B2.is_pressed(MP_MENU_MOUSE_POS()):
                        self.state = "invite_screen"
                    if B3.is_pressed(MP_MENU_MOUSE_POS()):
                        self.state = "search_id"
                    if B4.is_pressed(MP_MENU_MOUSE_POS()):
                        self.state = "main_menu"
                    if B5.is_pressed(MP_MENU_MOUSE_POS()):
                        self.state = "id_check"
                    break
        while self.state == "mp_menu":
            mp_menu_render()
            mp_menu_event_handler()
            pygame.display.flip()
            self.clock.tick(config.FPS)
        if self.state == "waiting"  :
            self.client.game_style = "local_game"
            self.waiting_room()  
        elif self.state == "search_id" :
            self.client.game_style = "invite_game"
            self.search_id_screen()
        elif self.state == "invite_screen" :
            self.client.game_style = "invite_game"
            self.invites_screen()
        elif self.state == "id_check":
            self.id_menu()

    def id_menu(self):
        background = pygame.image.load(background_path)
        background = pygame.transform.scale(background, (800,600))
        self.screen.blit(background, (0,0))
        id_menu_font = pygame.font.Font("src/assets/fonts/MinimalPixelFont.ttf",80)
        id_menu_text = id_menu_font.render("Your ID is : ", True, 'indigo')
        id_menu_text_rect = id_menu_text.get_rect(center= (self.screen_width // 2, self.screen_height//6))
        self.screen.blit(id_menu_text, id_menu_text_rect)
        id_font = pygame.font.Font("src/assets/fonts/OCRAEXT.ttf", 80)
        id_text = id_font.render(str(self.player.id), True, 'indigo')
        id_text_rect = id_text.get_rect(center=(400, 300))
        self.screen.blit(id_text, id_text_rect)
        
        ID_MENU_MOUSE_POS = pygame.mouse.get_pos
        BACK_BUTTON = Button(self, None, [100, 500], "back", 'OCRAEXT', 40, 'indigo', 'pink')
        def id_menu_event_handler():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN :
                    if BACK_BUTTON.is_pressed(ID_MENU_MOUSE_POS()):
                        self.state = "mp_menu"
                
        while self.state == "id_check":
            BACK_BUTTON.draw(ID_MENU_MOUSE_POS())
            id_menu_event_handler()
            pygame.display.flip()
            self.clock.tick(60)
            if self.state == "mp_menu":
                self.multiplayer_menu()


    def invites_screen(self):
        background = pygame.image.load(background_path)
        background = pygame.transform.scale(background, (800,600))
        self.screen.blit(background, (0,0))
        buttons = {}
        count = 0
        INVITES_SCREEN_MOUSE_POS = pygame.mouse.get_pos
        def update_invitations () :
            nonlocal count
            for invitation in self.client.invitations :
                if invitation["sender_id"] not in buttons :
                    buttons[invitation["sender_id"]] = Button(self, None, [400, 100 + (count* 200)], str(invitation["sender_id"]) + " " + invitation["nickname"], 'OCRAEXT', 30, 'indigo', 'pink')
                    count +=1

        def invite_screen_render():
            for invitation in self.client.invitations :
                if isinstance(buttons[invitation["sender_id"]], Button) :
                    buttons[invitation["sender_id"]].draw(INVITES_SCREEN_MOUSE_POS())

        def invite_screen_event_handler():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for invitation in self.client.invitations :
                        if isinstance(buttons[invitation["sender_id"]], Button) :
                            if buttons[invitation["sender_id"]].is_pressed(INVITES_SCREEN_MOUSE_POS()) :
                                self.client.accept_invite(invitation)
                                self.state = "waiting"
                                return
        while self.state == "invite_screen" :
            try:
                update_invitations()
                invite_screen_render()
                invite_screen_event_handler()
                pygame.display.flip()
                self.clock.tick(config.FPS)
            except Exception as e:
                print (e)
                import traceback
                traceback.print_exc()
    def search_id_screen (self):
        id = ""
        while self.state == "search_id" :
            background = pygame.image.load(background_path)
            background = pygame.transform.scale(background, (800,600))
            self.screen.blit(background, (0,0))
            
            id_menu_font = pygame.font.Font("src/assets/fonts/MinimalPixelFont.ttf",80)
            id_menu_text = id_menu_font.render("Enter an id", True, 'indigo')
            id_menu_text_rect = id_menu_text.get_rect(center= (self.screen_width // 2, self.screen_height//6))
            self.screen.blit(id_menu_text, id_menu_text_rect)

            text_font = pygame.font.Font("src/assets/fonts/OCRAEXT.ttf",50)
            id_text = text_font.render(id, True, 'black')
            text_rect = id_text.get_rect(center=(400,300)) 
            self.screen.blit(id_text,text_rect) 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN :
                         
                        try :
                            if self.client.send_invite(id)  :
                                print("id found")
                                self.state = "waiting"
                            else :
                                print("wrong id")
                                error_text = text_font.render("error", True, 'black')
                                error_text_rect = error_text.get_rect(center=(400, 400))
                                self.screen.blit(error_text,error_text_rect)
                                id = ""
                                time.sleep(4)
                                self.state = "mp_menu"
                                
                        except Exception as e:
                            import traceback
                            print("error", e)
                            traceback.print_exc()
                        break
                    elif event.key == pygame.K_BACKSPACE :
                        id = id[:-1]
                    else: 
                        id += event.unicode
            
            pygame.display.flip()
            self.clock.tick(config.FPS)

        if self.state == "waiting" :
            self.waiting_room()
        elif self.state == "mp_menu" :
            self.multiplayer_menu
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
                    pygame.quit()
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
        self.player.reset()
        for player in self.other_players :
            if isinstance(player, Player) and not player.is_dead :
                player.reset()
        self.other_players = []
        self.screen.fill((0, 0, 0))
        lose_font = pygame.font.Font("src/assets/fonts/OCRAEXT.ttf", 72)
        lose_msg = lose_font.render("YOU LOST !", True, 'yellow')
        text_rect = lose_msg.get_rect()
        text_rect.center = (self.screen_width//2, 200)
        self.screen.blit(lose_msg, text_rect)

        LS_MOUSE_POS = pygame.mouse.get_pos
        MENU_BUTTON = Button(self, None, [400, 500], 'main menu', 'OCRAEXT', 40, 'yellow', 'white')
        def ls_event_handler():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN :
                    if MENU_BUTTON.is_pressed(LS_MOUSE_POS()):
                        self.state = "main_menu"

        while self.state == "gameover" :
            MENU_BUTTON.draw(LS_MOUSE_POS())
            ls_event_handler()
            pygame.display.flip()
            self.clock.tick(60)

    def win_screen(self):
        try :
            self.player.reset()
            for player in self.other_players :
                if isinstance(player,Player) and not player.is_dead:
                    player.reset()
            self.other_players = []
            self.screen.fill((0, 0, 0))
            win_font = pygame.font.Font("src/assets/fonts/OCRAEXT.ttf", 72)
            win_msg = win_font.render("YOU WIN!", True, 'yellow')
            text_rect = win_msg.get_rect()
            text_rect.center = (self.screen_width//2, 200)
            self.screen.blit(win_msg, text_rect)

            WS_MOUSE_POS = pygame.mouse.get_pos
            MENU_BUTTON = Button(self, None, [400, 500], 'main menu', 'OCRAEXT', 40, 'yellow', 'white')
            def ws_event_handler():
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN :
                        if MENU_BUTTON.is_pressed(WS_MOUSE_POS()):
                            self.state = "main_menu"

            while self.state == "won" :
                MENU_BUTTON.draw(WS_MOUSE_POS())
                ws_event_handler()
                pygame.display.flip()
                self.clock.tick(60)
        except Exception as e :
            print(e)
            import traceback
            traceback.print_exc


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
    '''def spawn_random_powerup(self):
        powerup_types = ['shield', 'doublejump', 'damageboost', 'health']
        p_type = random.choice(powerup_types)

        valid_platforms = [p for p in self.level.platforms if isinstance(p, Platform) and p.visible]
        if not valid_platforms:
            return

        platform = random.choice(valid_platforms)
        x = platform.rect.centerx
        y = platform.rect.top - 50

        new_powerup = Powerup(self, x, y, p_type)
        self.level.powerup_group.add(new_powerup)'''
    def powerup_spawner(self, data):
        new_powerup = Powerup(self, data["x"], data["y"], data["type"])
        self.level.powerup_group.add(new_powerup)
        self.level.powerups.append(new_powerup)
    def powerup_killer(self, data):
        for powerup in self.level.powerup_group:
            if powerup.x == data["x"] and powerup.y == data["y"] and powerup.type == data["type"]:
                powerup.kill()
                self.level.powerups.remove(powerup)


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
            try :
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
                        if self.mode == "single_player" :
                            self.finish_menu()              
            except KeyboardInterrupt :
                if self.client != None :
                    self.client.is_connected = False
                break
            except :
                import traceback
                traceback.print_exc()
                if self.client != None :
                    self.client.is_connected = False
                break


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
                if self.state == "multiplayer" and self.client != None:
                    self.client.is_connected = False
                pygame.quit()
                sys.exit()    
            elif ((event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or 
                  (event.type == pygame.MOUSEBUTTONDOWN and self.PAUSE_BUTTON.is_pressed(GAME_MOUSE_POS()))) and \
                    self.state != "gameover" and self.mode == "single_player":
                # Press esc or pause button to pause
                self.state = "paused"

            elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) or \
                (event.type == pygame.KEYDOWN and (event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT)) :                
                self.player.is_shooting = True

            elif ((event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 ) or 
                  (event.type == pygame.KEYDOWN and (event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT))) and \
                    self.state != "paused" and self.state != "gameover" :
                #if event.button == 1 : #left mouse button
                    self.player.shoot()
            elif (event.type == pygame.KEYDOWN or (event.type == pygame.MOUSEBUTTONDOWN and self.PAUSE_BUTTON.is_pressed(GAME_MOUSE_POS()))) and self.state == "paused": # press space to resume
                if event.key == pygame.K_SPACE:
                    self.state = "playing"
            # Restart after game over
            elif self.state == "gameover" and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.restart()

    def update(self):
        
        if self.state == "playing" and self.level != None:
            if self.mode != "multiplayer" and self.level.won() :
                self.state = "won"
            if self.mode == "multiplayer" and self.mp_win():
                self.state == "won"
          
            if self.mode == "single_player" :
                self.player.update(self.level.platforms, self.level.powerup_group, self.level.enemies)
            elif self.mode == "multiplayer" :
                self.player.update(self.level.platforms, self.level.powerup_group)
                self.client.update_status()
                for player in self.other_players :
                    if isinstance(player,Player):
                        if player.is_dead :
                            self.other_players.remove(player)
                            self.client.other_players.remove(player)
                        else :
                            player.update_remote_player()
            self.update_camera()

            for platform in self.level.platforms :
                if isinstance(platform, Platform):
                    platform.update()
            if self.mode == "single_player" :
                for enemy in self.level.enemies:
                    enemy.update()

            # Update all fired bullets
            for bullet in self.Fired_bullets_list :
                if isinstance(bullet, Bullet) :
                    bullet.update()

            # spawning random powerups :
            if self.mode == "multiplayer":
                for powerup in self.level.powerup_group :
                    powerup.update()

            for powerup in self.level.powerup_group :
                powerup.update()


    def draw(self):
        self.screen.fill((135, 206, 235))  # Sky blue background
    
        self.screen.blit(self.level.background_layers,(0 - int(self.camera_x/10), 0))
        # Draw platforms and ground
        for platform in self.level.platforms:
            if isinstance(platform, Platform) and platform.visible == True:
                platform.draw(self.screen, self.camera_x)
            
        # Draw map
        if self.level.map != None:
            self.screen.blit(self.level.map,( 0 - self.camera_x , 0))
            

        # Draw player
        if(self.player.visible == True) :
            if self.player.direction == "left" :
                self.screen.blit( pygame.transform.flip(self.player.image,True,False), (self.player.rect.x - self.camera_x, self.player.rect.y))
            else :
                self.screen.blit( self.player.image, (self.player.rect.x - self.camera_x, self.player.rect.y))
        if self.other_players :
            self.display_nicknames()
            for player in self.other_players :
                if isinstance(player, Player) :
                    if player.direction == "left" :
                        self.screen.blit(pygame.transform.flip(player.image,True,False), (player.rect.x - self.camera_x, player.rect.y))
                    else :
                        self.screen.blit(player.image, (player.rect.x - self.camera_x, player.rect.y))
        # Draw all fired bullets with camera offset
        for bullet in self.Fired_bullets_list :
            if isinstance(bullet, Bullet) :
                self.screen.blit(bullet.image, (bullet.rect.x - self.camera_x, bullet.rect.y))

        # Draw enemies
        if self.mode == "single_player":
            self.draw_enemies()
        # Draw powerups 
        for powerup in self.level.powerups :
            powerup.draw()
        if self.mode == "multiplayer" :
            for powerup in self.level.powerup_group :
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
            if self.mode == "single_player" :
                self.gameover_render()
            else :
                self.lose_screen()
        if self.state == "won" :
            if self.mode == "multiplayer" :
                self.win_screen()
       

    def draw_enemies(self):
        if self.level.enemies:
            for enemy in self.level.enemies:
                if isinstance(enemy, Bomber) or isinstance(enemy, Freezerenemy):
                    if enemy.direction == "right" :
                        self.screen.blit(enemy.image,(enemy.rect.x - self.camera_x, enemy.rect.y))
                    else :
                        self.screen.blit(pygame.transform.flip(enemy.image,True,False),(enemy.rect.x - self.camera_x, enemy.rect.y))  
                else :    
                    pygame.draw.rect(self.screen, enemy.color,
                                    pygame.Rect(enemy.rect.x - self.camera_x, 
                                                enemy.rect.y, 
                                                enemy.rect.width, 
                                                enemy.rect.height))
    def show_health(self):
        health_display = font2.render("Your Health: " + str(self.player.health), True, 'black')
        self.screen.blit(health_display, (20,20))
        heart = AssetManager.UI_images["heart"]
        if self.player.health >= 0:
            for i in range(0,self.player.health):
                self.screen.blit(heart, (40 + 30*i , 60))
        if self.other_players :
            i = 0
            for player in self.other_players:
                
                if isinstance(player, Player):
                    if player.team == self.player.team :
                        teammate_health_display = font2.render(player.nickname + " : " + str(player.health), True, 'purple')
                        self.screen.blit(teammate_health_display, (20, 80))
                    else :
                        other_health_display = font2.render(player.nickname + " : " + str(player.health), True, 'red')
                        other_health_display_rect = other_health_display.get_rect(topright=(780, 20 + 40 *i))
                        self.screen.blit(other_health_display, other_health_display_rect)
                        i += 1
    
    def display_nicknames(self):
        nick_display = font3.render(self.player.nickname, True, 'grey')
        self.screen.blit(nick_display, (self.player.rect.x + 15 - self.camera_x, self.player.rect.y - 20))
        for player in self.other_players :
            others_nick_display = font3.render(player.nickname, True, 'grey')
            self.screen.blit(others_nick_display, (player.rect.x + 15 - self.camera_x, player.rect.y - 20))

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
        self.level.load()
        for platform in self.level.platforms :
            if isinstance(platform, Platform):
                platform.activated = False
                platform.visible = True
        for powerup in self.level.powerups :
            powerup.visible = True
            powerup.timer = 0
            powerup.is_inview = False
            self.level.powerup_group.add(powerup)
        
        self.state = "playing"

    def pause_render(self):
        pause_msg_font =  pygame.font.Font("src/assets/fonts/OCRAEXT.ttf", 50)
        pause_msg_text = pause_msg_font.render("Press space to resume!", True, 'indigo')
        pause_msg_rect = pause_msg_text.get_rect(center=(self.screen_width//2, self.screen_height//2))
        self.screen.blit(pause_msg_text, pause_msg_rect)

if __name__ == "__main__":
    game = Game()
    game.main_menu()
