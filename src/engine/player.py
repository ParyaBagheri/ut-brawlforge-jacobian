import pygame
import config
from src.engine.enemy import Enemy
from src.engine.bullet import Bullet
from src.engine.platform import Platform
from src.engine.assetmanager import AssetManager


class Player:
    def __init__(self, game):
        self.game = game
        self.rect = pygame.Rect(100, 300, 50, 80)
        self.velocity_y = 0
        self.on_ground = False
        self.color = (255, 0, 0)  # Player color (red)
        self.health = config.MAX_PLAYER_HEALTH
        self.is_invincible = False
        self.invincibility_timer = 0
        self.visible = True

        self.held_bullet = Bullet(self) # Create a bullet that follows the player (not fired yet)

        self.direction = "right" # Track facing direction ( default : right- facing )
        self.collision_direction = "none"

        self.state = "idle" 
        self.assets = AssetManager.player_assets["knight"]

        self.current_frame = 0
        self.image = self.assets[self.state][self.current_frame]



    def check_vertical_collision(self, platforms):
        # Check vertical collision (falling)
        if self.velocity_y > 0 :
            for platform in platforms:
                if isinstance(platform, Platform):
                    if (self.rect.bottom + self.velocity_y > platform.rect.top and
                        self.rect.top < platform.rect.top and
                        self.rect.right > platform.rect.left and 
                        self.rect.left < platform.rect.right):
                        self.rect.bottom = platform.rect.top
                        self.velocity_y = 0
                        self.on_ground = True
                        return platform
                else:
                    if (self.rect.bottom + self.velocity_y > platform.top and
                        self.rect.top < platform.top and
                        self.rect.right > platform.left and 
                        self.rect.left < platform.right):
                        self.rect.bottom = platform.top
                        self.velocity_y = 0
                        self.on_ground = True
                        return platform
        
        # Check vertical collision (jumping)
        for platform in platforms:
            if isinstance(platform, Platform) and platform.is_solid:
                if (self.velocity_y < 0 and
                    self.rect.top < platform.rect.bottom and
                    self.rect.bottom > platform.rect.bottom and
                    self.rect.right > platform.rect.left and 
                    self.rect.left < platform.rect.right):
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0
                    return platform
        
        self.on_ground = False
        return None
    
    def check_horizontal_collision(self,platforms):
        for platform in platforms :
            if isinstance(platform, Platform):
                if(self.rect.top < platform.rect.bottom and
                    self.rect.bottom > platform.rect.top) :
                    if(self.direction == "right" and
                       self.rect.right == platform.rect.left):
                        self.rect.right = platform.rect.left
                        self.collision_direction = "right"
                        return platform
                    elif(self.direction == "left" and
                         self.rect.left == platform.rect.right):
                        self.rect.left = platform.rect.right
                        self.collision_direction = "left"
                        return platform
                    self.collision_direction = "none"

    def check_enemy_collision(self,enemies):
        for enemy in enemies:
            if isinstance(enemy, Enemy):
                if self.rect.colliderect(enemy.rect):
                    #stomp enemy to kill it;  other collisions reduce player's health
                    if(self.velocity_y > 0 and
                        self.rect.bottom > enemy.rect.top and
                        self.rect.top < enemy.rect.top):
                        enemy.health -= 1
                        self.velocity_y = config.JUMP_VELOCITY * 0.5
                    elif(enemy.is_collided == False) :
                        self.health -= 1
                        enemy.is_collided = True
                        self.is_invincible = True
                        return enemy
    
    def update(self, platforms, enemies):
        keys = pygame.key.get_pressed()
        self.update_image(keys)
        
        # Horizontal movement
        if (keys[pygame.K_a] and self.collision_direction != "left"):
            self.rect.x -= config.MOVE_SPEED
            self.direction = "left" # Update facing direction

        if (keys[pygame.K_d] and self.collision_direction != "right"):
            self.rect.x += config.MOVE_SPEED
            self.direction = "right" # Update facing direction
        if self.rect.x <= 0 :
            self.rect.x = 0
            
        # Apply gravity
        self.velocity_y += config.GRAVITY
        self.rect.y += self.velocity_y
        
        # Check collisions
        self.check_vertical_collision(platforms)
        self.check_horizontal_collision(platforms)
        self.check_enemy_collision(enemies)

        # Temporary flickering after collision with an enemy
        if self.is_invincible :
            self.invincibility_timer += 1
            if self.invincibility_timer % 15 < 8 :
                self.visible = True
            else :
                self.visible = False
            if self.invincibility_timer >= 50:
                self.is_invincible = False
        else :
            self.visible = True
            self.invincibility_timer = 0


        # Game over when player dies
        if self.health <= 0:
            self.game.gameover()
            
        # Jumping (only if on ground)
        if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and self.on_ground:
            self.velocity_y = config.JUMP_VELOCITY
            self.on_ground = False
        
        # Update held bullet (follows player if not fired)
        self.held_bullet.update()

    def update_image (self, keys) :

        self.current_frame += 0.1
        if(self.current_frame >= len(self.assets[self.state])) :
            self.current_frame = 0

        if (self.on_ground and ( not ( keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_UP] or keys[pygame.K_SPACE] ) ) ):
            if(self.state != "idle"):
                self.current_frame = 0
                self.state = "idle"

        elif ( (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and self.on_ground) :

            self.current_frame = 0
            self.state = "jumping"
            
        elif not self.on_ground :

            if(self.state != "falling" and self.state != "jumping") :
                self.current_frame = 0
                self.state = "falling"
        
        elif (keys[pygame.K_a] or keys[pygame.K_d]) and self.on_ground :
            if(self.state != "run" ):
                self.current_frame = 0
                self.state = "run"

        self.image = self.assets[self.state][int(self.current_frame)]
        
        

    def shoot (self) :

        # Trigger the held bullet to be fired
        self.held_bullet.fire()

        # Create a new bullet that will follow the player (for next shot)
        self.held_bullet = Bullet (self)