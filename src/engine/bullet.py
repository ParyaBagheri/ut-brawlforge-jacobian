import pygame
import os

right_bullet_image_path = os.path.join("src","assets", "images" , "rightpaintball.png")
left_bullet_image_path = os.path.join("src","assets", "images" , "rightpaintball.png")

right_bullet_image = pygame.image.load(right_bullet_image_path)
right_bullet_image = pygame.transform.scale(right_bullet_image, (20, 20))
left_bullet_image = pygame.image.load(left_bullet_image_path)
left_bullet_image = pygame.transform.scale(left_bullet_image, (20, 20))

BULLET_SPEED = 30
BULLET_DAMAGE = 1


class Bullet :

    def __init__(self, player) :
        #set the default direction
        self.bulletimg = right_bullet_image # Default image (right-facing)
        self.direction = "none"

        self.player = player # Reference to the player who shot this bullet
        
        self.is_fired = False
        self.game = self.player.game 
        
        #bullet's speed
        self.changex = 0

        # Create bullet's rectangle at player's center (adjusted for image size)
        self.rect = pygame.Rect(self.player.rect.centerx-10, self.player.rect.centery-10, 20, 20)

    
            

    def fire (self) :
        
        # Mark bullet as shot and add it to the game's bullet list
        self.is_fired = True
        self.game.Fired_bullets_list.append(self)

        
        # Set direction and speed based on player's facing direction
        if self.player.direction == "right"  :
            self.changex = BULLET_SPEED
            self.direction = "right"
            self.bulletimg = right_bullet_image # Right-facing image
            
        if self.player.direction == "left" :
            self.changex = -BULLET_SPEED
            self.direction = "left"
            self.bulletimg = left_bullet_image # Left-facing image


    def update (self) :

        if self.is_fired == True :

            # Bullet is in flight - move it horizontally
            self.rect.x += self.changex

            # Check for collisions, remove if hit something
            if self.check_platform_collision() or self.check_enemy_collision() :
                self.game.Fired_bullets_list.remove(self)
    
        else :

            # Bullet hasn't been fired yet - follow player position 
            self.rect.x = self.player.rect.centerx - 10
            self.rect.y = self.player.rect.centery - 10
    
    def check_enemy_collision (self) :
        if self.is_fired == True :
            for enemy in self.game.enemies :
                #if isinstance (enemy, Enemy) :
                if self.direction == "right" :
                    if (self.rect.right >= enemy.rect.left and 
                    self.rect.right <= enemy.rect.right and 
                    self.rect.y >= enemy.rect.top and 
                    self.rect.y <= enemy.rect.bottom ):
                            enemy.got_shot()
                            return True
                elif self.direction == "left" :
                    if (self.rect.left <= enemy.rect.right and 
                    self.rect.left >= enemy.rect.left and 
                    self.rect.y >= enemy.rect.top and 
                    self.rect.y <= enemy.rect.bottom ):
                        enemy.got_shot()
                        return True



        
        
    def check_platform_collision (self) :
        
        # Check if bullet went off-screen (left or right of camera view)
        if self.rect.right < self.game.camera_x  or self.rect.left > self.game.screen_width + self.game.camera_x :
            return True
            
        else :

            # Check collision with platforms
            for platform in self.game.platforms:
                    #if isinstance (platform, Platform) :
                    
                if (self.rect.x >= platform.rect.left and 
                self.rect.x <= platform.rect.right and 
                self.rect.y >= platform.rect.top and 
                self.rect.y <= platform.rect.bottom ):
                        
                    return True # Bullet hit a platform
                    
        return False  # Bullet didn't hit anything