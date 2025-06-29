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

        AssetManager.player_assets["knight"] = {
            "idle" : knight_idle_frames ,
            "run" : knight_run_frames ,
            "jumping" : knight_jumping_frames,
            "falling" : knight_falling_frames
            }
        
        


        
    def load_assets():
        AssetManager.load_player_assets()
