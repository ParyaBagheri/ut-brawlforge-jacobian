import pygame
import sys

class AssetManager :
    
    player_assets = {}
    enemy_assets = {}

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

        knight_idle_sheet = pygame.image.load ("src/assets/images/player/knight/idle.png")
        knight_idle_frames = AssetManager.load_frames(knight_idle_sheet, 16,19,5,4)
        knight_idle_frames = AssetManager.scale_frames(knight_idle_frames, 50, 80)

        knight_run_sheet = pygame.image.load("src/assets/images/player/knight/run.png")
        knight_run_frames = AssetManager.load_frames(knight_run_sheet, 16,21,3,4)
        knight_run_frames = AssetManager.scale_frames(knight_run_frames, 50, 80)

        knight_jumping_sheet = pygame.image.load("src/assets/images/player/knight/jumping.png")
        knight_jumping_frames = AssetManager.load_frames(knight_jumping_sheet, 16,21,2,4)
        knight_jumping_frames = AssetManager.scale_frames(knight_jumping_frames, 50, 80)

        knight_falling_sheet = pygame.image.load("src/assets/images/player/knight/falling.png")
        knight_falling_frames = AssetManager.load_frames(knight_falling_sheet, 16,20,2,4)
        knight_falling_frames = AssetManager.scale_frames(knight_falling_frames, 50, 80)

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
        wizard_falling_frames = AssetManager.load_frames(wizard_falling_sheet, 16, 22 , 0 ,1)
        wizard_falling_frames = AssetManager.scale_frames(wizard_falling_frames, 50 , 80)


        AssetManager.player_assets["knight"] = {
            "idle" : knight_idle_frames ,
            "run" : knight_run_frames ,
            "jumping" : knight_jumping_frames,
            "falling" : knight_falling_frames
        }
        AssetManager.player_assets["girl"] = {
            "idle" : girl_idle_frames ,
            "run" : girl_run_frames ,
            "jumping" : girl_jumping_frames ,
            "falling" : girl_falling_frames
        }
        AssetManager.player_assets["wizard"] = {
            "idle" : wizard_idle_frames ,
            "run" : wizard_run_frames ,
            "jumping" : wizard_jumping_frames ,
            "falling" : wizard_falling_frames
        }

        
    def load_assets():
        AssetManager.load_player_assets()
