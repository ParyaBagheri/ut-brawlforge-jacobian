import pygame
import os

FPS = 60
GRAVITY = 1200
FRICTION = - 120
JUMP_VELOCITY = -800
MOVE_SPEED = 500
BASE_GROUND_HEIGHT = 100
BASE_SCREEN_WIDTH = 800
BASE_SCREEN_HEIGHT = 600
MAX_ENEMY_HEALTH = 1
INITIAL_ENEMY_SPEED = 4.8
MAX_PLAYER_HEALTH = 3
PLAYER_FRAMES_SPEED = 0.15

BULLET_SPEED = {
    "arrow" : 20 ,
    "fireball" : 25 ,
}
BULLET_DAMAGE = 1
BULLET_SIZE ={
    "arrow" : (44, 15) ,
    "fireball" : (30, 21)
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