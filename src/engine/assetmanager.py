import pygame
import sys
import config

class AssetManager :
    
    player_images = {}
    enemy_assets = {}
    bullet_assets = {}
    player_sounds = {}

    def load_frames(sheet,frame_width,frame_hight ,startpoint, numframes):
        frames = []
        for i in range (numframes) :
            rect = pygame.Rect( i * frame_width,startpoint , frame_width, frame_hight )
            frame = sheet.subsurface(rect)
            frames.append(frame)

        return frames
    def scale_frames(frames,width, height) :
        newframes = []
        for i in range (len(frames)):
            frame = pygame.transform.scale(frames[i], (width, height))
            newframes.append(frame)
        return newframes
    
    def load_player_assets () :
        # player's sound effects
        AssetManager.load_player_sounds ()

        # knight character images
        knight_idle_sheet = pygame.image.load ("src/assets/images/player/knight/idle.png")
        knight_idle_frames = AssetManager.load_frames(knight_idle_sheet, 16,19,5,4)
        knight_idle_frames = AssetManager.scale_frames(knight_idle_frames, 50, 80)

        knight_run_sheet = pygame.image.load("src/assets/images/player/knight/run.png")
        knight_run_frames = AssetManager.load_frames(knight_run_sheet, 16,21,3,4)
        knight_run_frames = AssetManager.scale_frames(knight_run_frames, 50, 80)

        knight_jumping_sheet = pygame.image.load("src/assets/images/player/knight/jumping.png")
        knight_jumping_frames = AssetManager.load_frames(knight_jumping_sheet, 16,20,3,4)
        knight_jumping_frames = AssetManager.scale_frames(knight_jumping_frames, 50, 80)

        knight_falling_sheet = pygame.image.load("src/assets/images/player/knight/falling.png")
        knight_falling_frames = AssetManager.load_frames(knight_falling_sheet, 16,19,3,1)
        knight_falling_frames = AssetManager.scale_frames(knight_falling_frames, 50, 80)

        knight_attack_sheet = pygame.image.load("src/assets/images/player/knight/attack.png")
        knight_attack_frames = AssetManager.load_frames(knight_attack_sheet, 16,20,4, 6)
        knight_attack_frames = AssetManager.scale_frames(knight_attack_frames, 50 , 80)

        knight_die_sheet = pygame.image.load("src/assets/images/player/knight/die.png")
        knight_die_frames = AssetManager.load_frames(knight_die_sheet, 16, 24, 0, 4)
        knight_die_frames = AssetManager.scale_frames(knight_die_frames, 50, 80 )

        # girl character images
        girl_idle_sheet = pygame.image.load("src/assets/images/player/girl/idle.png")
        girl_idle_frames = AssetManager.load_frames(girl_idle_sheet,16,20,4,4)
        girl_idle_frames = AssetManager.scale_frames(girl_idle_frames, 50, 80)

        girl_run_sheet = pygame.image.load("src/assets/images/player/girl/run.png")
        girl_run_frames = AssetManager.load_frames(girl_run_sheet,16,22,2,4)
        girl_run_frames = AssetManager.scale_frames(girl_run_frames, 50, 80)

        girl_jumping_sheet = pygame.image.load("src/assets/images/player/girl/jumping.png")
        girl_jumping_frames = AssetManager.load_frames(girl_jumping_sheet,16,21,2,4)
        girl_jumping_frames = AssetManager.scale_frames(girl_jumping_frames, 50, 80)

        girl_falling_sheet = pygame.image.load("src/assets/images/player/girl/falling.png")
        girl_falling_frames = AssetManager.load_frames(girl_falling_sheet,16,20,2,1)
        girl_falling_frames = AssetManager.scale_frames(girl_falling_frames, 50, 80)

        girl_attack_sheet = pygame.image.load("src/assets/images/player/girl/attack.png")
        girl_attack_frames = AssetManager.load_frames (girl_attack_sheet, 16, 21, 3 ,5)
        girl_attack_frames = AssetManager.scale_frames(girl_attack_frames, 50, 80)

        girl_die_sheet = pygame.image.load("src/assets/images/player/girl/die.png")
        girl_die_frames = AssetManager.load_frames(girl_die_sheet, 16, 24, 0, 4)
        girl_die_frames = AssetManager.scale_frames(girl_die_frames, 50, 80 )

        # wizard character images
        wizard_idle_sheet = pygame.image.load("src/assets/images/player/wizard/idle.png")
        wizard_idle_frames = AssetManager.load_frames(wizard_idle_sheet, 16, 22 , 2 ,4)
        wizard_idle_frames = AssetManager.scale_frames(wizard_idle_frames, 50 , 80)

        wizard_run_sheet = pygame.image.load("src/assets/images/player/wizard/run.png")
        wizard_run_frames = AssetManager.load_frames(wizard_run_sheet, 16, 24 , 0 ,4)
        wizard_run_frames = AssetManager.scale_frames(wizard_run_frames, 50 , 80)

        wizard_jumping_sheet = pygame.image.load("src/assets/images/player/wizard/jumping.png")
        wizard_jumping_frames = AssetManager.load_frames(wizard_jumping_sheet, 16, 23, 0 ,4)
        wizard_jumping_frames = AssetManager.scale_frames(wizard_jumping_frames, 50 , 80)

        wizard_falling_sheet = pygame.image.load("src/assets/images/player/wizard/falling.png")
        wizard_falling_frames = AssetManager.load_frames(wizard_falling_sheet, 16, 23 , 0 ,1)
        wizard_falling_frames = AssetManager.scale_frames(wizard_falling_frames, 50 , 80)

        wizard_attack_sheet = pygame.image.load("src/assets/images/player/wizard/attack.png")
        wizard_attack_frames = AssetManager.load_frames(wizard_attack_sheet, 16, 23, 1,6)
        wizard_attack_frames = AssetManager.scale_frames(wizard_attack_frames, 50, 80)

        wizard_die_sheet = pygame.image.load("src/assets/images/player/wizard/die.png")
        wizard_die_frames = AssetManager.load_frames(wizard_die_sheet, 16, 24, 0, 4)
        wizard_die_frames = AssetManager.scale_frames(wizard_die_frames, 50, 80 )

        AssetManager.player_images["knight"] = {
            "idle" : knight_idle_frames ,
            "run" : knight_run_frames ,
            "jumping" : knight_jumping_frames,
            "falling" : knight_falling_frames ,
            "attack" : knight_attack_frames ,
            "die" : knight_die_frames
        }
        AssetManager.player_images["girl"] = {
            "idle" : girl_idle_frames ,
            "run" : girl_run_frames ,
            "jumping" : girl_jumping_frames ,
            "falling" : girl_falling_frames ,
            "attack" : girl_attack_frames ,
            "die" : girl_die_frames
        }
        AssetManager.player_images["wizard"] = {
            "idle" : wizard_idle_frames ,
            "run" : wizard_run_frames ,
            "jumping" : wizard_jumping_frames ,
            "falling" : wizard_falling_frames ,
            "attack" : wizard_attack_frames ,
            "die" : wizard_die_frames
        }

    def load_player_sounds ():
        
        # running sound
        running_sound = pygame.mixer.Sound("src/assets/sounds/player/running.wav")
        running_sound.set_volume(1)
        # jump sound
        jump_sound = pygame.mixer.Sound("src/assets/sounds/player/jump.wav")
        jump_sound.set_volume(0.2)
        # attack sound
        attack_sound = pygame.mixer.Sound("src/assets/sounds/player/attack.wav")
        # damege sound
        damage_sound = pygame.mixer.Sound("src/assets/sounds/player/damage.wav")
        damage_sound.set_volume(0.6)

        AssetManager.player_sounds = {
            "running" : running_sound ,
            "jump" : jump_sound ,
            "attack" : attack_sound ,
            "damage" : damage_sound
        }
        
  

    def load_bullet_assets (): 

        arrow_image = pygame.image.load("src/assets/images/bullet/arrow.png")  
        arrow_image = pygame.transform.rotate(arrow_image, 270)
        arrow_image = AssetManager.load_frames(arrow_image,21, 7, 0 , 1)
        arrow_image = AssetManager.scale_frames(arrow_image, config.BULLET_SIZE ["arrow"][0], config.BULLET_SIZE["arrow"][1] )

        fireball_sheet  = pygame.image.load("src/assets/images/bullet/fireball.png")
        fireball_frames = AssetManager.load_frames(fireball_sheet,13, 9, 0 ,7)
        fireball_frames = AssetManager.scale_frames(fireball_frames, config.BULLET_SIZE ["fireball"][0],config.BULLET_SIZE["fireball"][1] )
        
        AssetManager.bullet_assets = {
            "arrow" : arrow_image ,
            "fireball" : fireball_frames
        }
        
    def load_assets():
        AssetManager.load_player_assets()
        AssetManager.load_bullet_assets()
