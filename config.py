import pygame
import os

FPS = 60
GRAVITY = 1
JUMP_VELOCITY = -18
MOVE_SPEED = 5
BASE_GROUND_HEIGHT = 104
BASE_SCREEN_WIDTH = 800
BASE_SCREEN_HEIGHT = 600
MAX_ENEMY_HEALTH = 1
INITIAL_ENEMY_SPEED = 4.8
MAX_PLAYER_HEALTH = 3
PLAYER_FRAMES_SPEED = 0.15

BULLET_SPEED = {
    "arrow" : 20 ,
    "fireball" : 25 ,
    "freeze" : 25
}
BULLET_DAMAGE = 1
BULLET_SIZE ={
    "arrow" : (44, 15) ,
    "fireball" : (30, 21),
    "freeze" : (30, 21)
}
WEAPONS = {
    "knight" : "bow" ,
    "girl" : "bow" ,
    "wizard" : "wand"
}
SHOOT_FRAME = {
    "bow" : 2 ,
    "wand" : 4
}
BULLET_FRAMES_SPEED = 0.45
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BUTTON_FRAMES_SPEED = 0.15
FINISHING_POINTS = {
    "forest" : 3200 ,
    "desert" : 6000,
    "lost_city" : 7700,
    "underwater" : 16000,
    "multiplayer" : 3200

}
MUSIC_PATHS = {
    "game_music" : "src/assets/sounds/music/game_music.mp3",
    "menu_music" :"src/assets/sounds/music/menu_music.mp3"
}