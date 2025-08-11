import pygame
import os
import math
#from src.engine.enemy import Enemy
from src.engine.platform import Platform
from src.engine.assetmanager import AssetManager
import config
from src.engine.assetmanager import AssetManager



class Bullet :

    def __init__(self, owner, type) :
        #arrow or fireball or ...
        self.type = type

        #set the default direction
        self.direction = "none"
        #bullet animation
        self.asset = AssetManager.bullet_assets[self.type] # Default image (right-facing)
        self.current_frame = 0
        self.image = self.asset [self.current_frame]

        self.owner = owner # Reference to the player who shot this bullet
        self.player_collision = False
        self.is_fired = False
        self.game = self.owner.game 
        self.damage = config.BULLET_DAMAGE
        
        
        #bullet's speed
        self.speed = config.BULLET_SPEED[self.type]
        self.changex = 0
        self.changey = 0
        # Create bullet's rectangle at player's center (adjusted for image size)
        self.rect = pygame.Rect(self.owner.rect.centerx, self.owner.rect.centery-3, config.BULLET_SIZE [self.type][0],config.BULLET_SIZE [self.type][1])

    
            

    def fire (self, direction= None) :
        
        # Mark bullet as shot and add it to the game's bullet list
        self.is_fired = True
        self.game.Fired_bullets_list.append(self)

        
        # Set direction and speed based on player's facing direction
        if direction == None:
            if self.owner.direction == "right"  :
                self.changex = self.speed
                self.direction = "right"
                    
            if self.owner.direction == "left" :
                self.changex = -self.speed
                self.direction = "left"
        elif direction :
            theta = (direction[0]) // math.sqrt(((direction[0]*direction[0]) + (direction[1]*direction[1])))
            self.direction = 180 - theta
            self.changex = direction[0] // 40
            self.changey = direction[1] // 30




    def update (self) :

        if self.is_fired == True :
            #fired bullet animation 
            self.update_image ()
            # Bullet is in flight - move it horizontally
            self.rect.x += self.changex 
            self.rect.y += self.changey

            # Check for collisions, remove if hit something
            if self.check_platform_collision() or self.check_enemy_collision() or self.player_collision:
                self.game.Fired_bullets_list.remove(self)
    
        else :

            # Bullet hasn't been fired yet - follow player position 
            self.rect.x = self.owner.rect.centerx
            self.rect.y = self.owner.rect.centery - 3

    def update_image (self) :
        self.current_frame += config.BULLET_FRAMES_SPEED
        if self.current_frame >= len(self.asset) :
            self.current_frame = 0
        if self.direction == "right" :
            self.image = self.asset[int(self.current_frame)] # Right-facing image
        elif self.direction == "left":
            self.image = pygame.transform.flip(self.asset[int(self.current_frame)], True, False ) #left_facing image
        else :
            self.image = pygame.transform.rotate(self.asset[int(self.current_frame)], int(self.direction))
    def check_enemy_collision (self) :
        if self.is_fired == True and self.type != "freeze": 
            if self.game.level.enemies : 
                for enemy in self.game.level.enemies :
                    #if isinstance (enemy, Enemy) :
                    if self.direction == "right" :
                        if (self.rect.right >= enemy.rect.left and 
                        self.rect.right <= enemy.rect.right and 
                        self.rect.y >= enemy.rect.top and 
                        self.rect.y <= enemy.rect.bottom ):
                                enemy.got_shot(self.damage)
                                return True
                    elif self.direction == "left" :
                        if (self.rect.left <= enemy.rect.right and 
                        self.rect.left >= enemy.rect.left and 
                        self.rect.y >= enemy.rect.top and 
                        self.rect.y <= enemy.rect.bottom ):
                            enemy.got_shot(self.damage)
                            return True



        
        
    def check_platform_collision (self) :
        
        # Check if bullet went off-screen (left or right of camera view)
        if self.rect.right < self.game.camera_x  or self.rect.left > self.game.screen_width + self.game.camera_x :
            return True
            
        else :

            # Check collision with platforms
            for platform in self.game.level.platforms:
                if isinstance (platform, Platform) :
                    if (self.rect.x >= platform.rect.left and 
                    self.rect.x <= platform.rect.right and 
                    self.rect.y >= platform.rect.top and 
                    self.rect.y <= platform.rect.bottom ):
                            
                        return True # Bullet hit a platform
                    
        return False  # Bullet didn't hit anything