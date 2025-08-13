import pygame
import sys
import config

class AssetManager :
    
    player_images = {}
    enemy_assets = {}
    bullet_assets = {}
    player_sounds = {}
    platform_images = {}
    map_image = {}
    backgrounds = {}
    UI_images = {}
    UI_sounds = {}
    powerups_images ={}

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
        # bounce sound
        bounce_sound = pygame.mixer.Sound("src/assets/sounds/player/bounce.mp3")
        bounce_sound.set_volume(0.4)
        # game over sound
        gameover_sound = pygame.mixer.Sound("src/assets/sounds/player/gameover.mp3")
        gameover_sound.set_volume(0.4)
        # Collect sound
        collect_sound = pygame.mixer.Sound("src/assets/sounds/player/collect.mp3")
        collect_sound.set_volume(0.05)
        AssetManager.player_sounds = {
            "running" : running_sound ,
            "jump" : jump_sound ,
            "attack" : attack_sound ,
            "damage" : damage_sound ,
            "bounce" : bounce_sound ,
            "game over" : gameover_sound,
            "collect" : collect_sound
        }
        
  

    def load_bullet_assets (): 

        arrow_image = pygame.image.load("src/assets/images/bullet/arrow.png")  
        arrow_image = pygame.transform.rotate(arrow_image, 270)
        arrow_image = AssetManager.load_frames(arrow_image,21, 7, 0 , 1)
        arrow_image = AssetManager.scale_frames(arrow_image, config.BULLET_SIZE ["arrow"][0], config.BULLET_SIZE["arrow"][1] )

        fireball_sheet  = pygame.image.load("src/assets/images/bullet/fireball.png")
        fireball_frames = AssetManager.load_frames(fireball_sheet,13, 9, 0 ,7)
        fireball_frames = AssetManager.scale_frames(fireball_frames, config.BULLET_SIZE ["fireball"][0],config.BULLET_SIZE["fireball"][1] )
        
        freeze_bullet_sheet = pygame.image.load("src/assets/images/bullet/freeze.png")
        freeze_bullet_frames = AssetManager.load_frames(freeze_bullet_sheet,15, 5, 0 ,4)
        freeze_bullet_frames = AssetManager.scale_frames(freeze_bullet_frames, config.BULLET_SIZE ["fireball"][0],config.BULLET_SIZE["fireball"][1] )
        AssetManager.bullet_assets = {
            "arrow" : arrow_image ,
            "fireball" : fireball_frames,
            "freeze" : freeze_bullet_frames
        }
    def load_platform_images () :
        
        lostcity_platform = pygame.image.load("src/assets/images/platforms/lostcity.png")
        slowing_platform = pygame.image.load("src/assets/images/platforms/slowing.png")
        timed_platform = pygame.image.load("src/assets/images/platforms/timed.png")
        spikey_platform = pygame.image.load("src/assets/images/platforms/spikey.png")
        bouncy_frames = pygame.image.load("src/assets/images/platforms/bouncy.png")
        bouncy_frames = AssetManager.load_frames(bouncy_frames, 16,16,0,6)
        bouncy_frames = AssetManager.scale_frames(bouncy_frames, 50, 40)
        AssetManager.platform_images = {
            "lostcity" : lostcity_platform ,
            "slowing" : slowing_platform ,
            "timed" : timed_platform ,
            "spikey" : spikey_platform ,
            "bouncy" : bouncy_frames
        }
    def load_map ( ) :
        forest_map =   pygame.image.load("src/assets/tiles and maps/forest.png")
        desert_map = pygame.image.load("src/assets/tiles and maps/desert.png")
        lost_city_map = pygame.image.load("src/assets/tiles and maps/lostcity.png")
        underwater_map = pygame.image.load("src/assets/tiles and maps/underwater.png")
        
        AssetManager.map_image = {
            "forest" : forest_map ,
            "desert" : desert_map ,
            "underwater" : underwater_map,
            "lost_city" : lost_city_map
        }
        forest_background = pygame.image.load("src/assets/images/backgrounds/forest.jpeg")
        forest_background = pygame.transform.scale(forest_background,(forest_background.get_width() ,config.BASE_SCREEN_HEIGHT ))
        desert_background = pygame.image.load("src/assets/images/backgrounds/desert.jpeg")
        desert_background = pygame.transform.scale(desert_background,(desert_background.get_width()*1.1  ,config.BASE_SCREEN_HEIGHT ))
        lost_city_background = pygame.image.load("src/assets/images/backgrounds/lost_city.jpeg")
        lost_city_background = pygame.transform.scale(lost_city_background,(lost_city_background.get_width()*1.3,config.BASE_SCREEN_HEIGHT ))
        underwater_background = pygame.image.load("src/assets/images/backgrounds/underwater.jpg")
        underwater_background = pygame.transform.scale(underwater_background,(underwater_background.get_width() *1.6,config.BASE_SCREEN_HEIGHT ))
        AssetManager.backgrounds = {
            "forest" : forest_background ,
            "desert" : desert_background ,
            "lost_city" : lost_city_background ,
            "underwater" : underwater_background
        }
    def load_UI_assets ():
        AssetManager.load_UI_sounds()
        heart_image = pygame.image.load("src/assets/images/UI/heart.png")
        #heart_image = pygame.transform.scale(heart_image, (7, 6))

        A_key_sheet = pygame.image.load("src/assets/images/UI/keys/A.png")
        A_key_frames = AssetManager.load_frames(A_key_sheet, 19,21,0,3)
        A_key_frames = AssetManager.scale_frames(A_key_frames,57,63)
        D_key_sheet =  pygame.image.load("src/assets/images/UI/keys/D.png")
        D_key_frames = AssetManager.load_frames(D_key_sheet, 19,21,0,3)
        D_key_frames = AssetManager.scale_frames(D_key_frames,57,63)
        SPACE_key_sheet = pygame.image.load("src/assets/images/UI/keys/space.png")
        SPACE_key_frames = AssetManager.load_frames(SPACE_key_sheet, 98,21,0,3)
        SPACE_key_frames = AssetManager.scale_frames(SPACE_key_frames,294,63)
        SHIFT_key_sheet = pygame.image.load("src/assets/images/UI/keys/shift.png")
        SHIFT_key_frames = AssetManager.load_frames(SHIFT_key_sheet, 61,21,0,3)
        SHIFT_key_frames = AssetManager.scale_frames(SHIFT_key_frames,183,63)
        
        AssetManager.UI_images = {
            "heart" : heart_image,
            "A_key" : A_key_frames,
            "D_key" : D_key_frames,
            "SPACE_key" : SPACE_key_frames,
            "SHIFT_key" : SHIFT_key_frames,
        }
    def load_UI_sounds ():
        hover_sound = pygame.mixer.Sound("src/assets/sounds/UI/hover.wav")
        hover_sound.set_volume(0.2)
        click_sound = pygame.mixer.Sound("src/assets/sounds/UI/click.wav")
        click_sound.set_volume(0.2)
        win_sound = pygame.mixer.Sound("src/assets/sounds/UI/win.mp3")
        win_sound.set_volume(0.5)
        AssetManager.UI_sounds = {
            "hover" : hover_sound ,
            "click" : click_sound,
            "win": win_sound
        }
    def load_powerups_assets():
        shield_image = pygame.image.load("src/assets/images/powerups/shield.png").convert_alpha()
        shield_image = pygame.transform.scale(shield_image,(40,40))
        doublejump_image = pygame.image.load("src/assets/images/powerups/doublejump.png").convert_alpha()
        boost_image = pygame.image.load("src/assets/images/powerups/boost.png").convert_alpha()
        boost_image = pygame.transform.scale(boost_image,(40,40))
        health_image = pygame.image.load("src/assets/images/powerups/health.png").convert_alpha()
        health_image = pygame.transform.scale(health_image,(50,50))
        AssetManager.powerups_images ={
            "shield" : shield_image,
            "doublejump" : doublejump_image,
            "damageboost" : boost_image,
            "health" : health_image
        }
    def load_enemy_assets () :
        bomber_idle_sheet = pygame.image.load("src/assets/images/enemy/bomber/idle.png")
        bomber_idle_frames = AssetManager.load_frames(bomber_idle_sheet,16 , 16, 0 ,4)
        bomber_idle_frames = AssetManager.scale_frames(bomber_idle_frames, 50, 50)
        bomber_run_sheet = pygame.image.load("src/assets/images/enemy/bomber/run.png")
        bomber_run_frames = AssetManager.load_frames(bomber_run_sheet,16 , 16, 0 ,4)
        bomber_run_frames = AssetManager.scale_frames(bomber_run_frames, 50, 50)
        bomber_death_sheet = pygame.image.load("src/assets/images/enemy/bomber/death.png")
        bomber_death_frames = AssetManager.load_frames(bomber_death_sheet,16 , 16, 0 ,6)
        bomber_death_frames = AssetManager.scale_frames(bomber_death_frames, 50, 50)
        AssetManager.enemy_assets["bomber"] = {
            "idle" : bomber_idle_frames,
            "run" : bomber_run_frames ,
            "death" : bomber_death_frames
        }
        freezer_idle_sheet = pygame.image.load("src/assets/images/enemy/freezer/idle.png")
        freezer_idle_frames = AssetManager.load_frames(freezer_idle_sheet,32 , 16, 8 ,4)
        freezer_idle_frames = AssetManager.scale_frames(freezer_idle_frames, 100, 60)
        freezer_attack_sheet = pygame.image.load("src/assets/images/enemy/freezer/attack.png")
        freezer_attack_frames = AssetManager.load_frames(freezer_attack_sheet,32 , 16, 8 ,6)
        freezer_attack_frames = AssetManager.scale_frames(freezer_attack_frames, 100, 60)
        freezer_death_sheet = pygame.image.load("src/assets/images/enemy/freezer/death.png")
        freezer_death_frames = AssetManager.load_frames(freezer_death_sheet,32 , 16, 0 ,7)
        freezer_death_frames = AssetManager.scale_frames(freezer_death_frames, 100, 60)
        freezer_damage_sheet = pygame.image.load("src/assets/images/enemy/freezer/damage.png")
        freezer_damage_frames = AssetManager.load_frames(freezer_damage_sheet,32 , 16, 8 ,4)
        freezer_damage_frames = AssetManager.scale_frames(freezer_damage_frames, 100, 60)
        AssetManager.enemy_assets["freezer"] = {
            "idle" : freezer_idle_frames,
            "attack" : freezer_attack_frames ,
            "death" : freezer_death_frames ,
            "damage" : freezer_damage_frames
        }
        
    def load_assets():
        AssetManager.load_player_assets()
        AssetManager.load_bullet_assets()
        AssetManager.load_platform_images()
        AssetManager.load_map()
        AssetManager.load_UI_assets ()
        AssetManager.load_powerups_assets()
        AssetManager.load_enemy_assets()
