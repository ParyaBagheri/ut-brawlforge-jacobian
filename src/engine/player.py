import pygame
import config
from src.engine.enemy import Enemy
from src.engine.bullet import Bullet
from src.engine.platform import Platform
from src.engine.assetmanager import AssetManager


class Player:
    def __init__(self, game,character_type):
        self.game = game
        self.color = (255, 0, 0)  # Player color (red)
        '''if image:
            self.image = image
        else:
            self.image = pygame.Surface((50, 80))
            self.image.fill(self.color)'''
        self.velocity_y = 0
        self.on_ground = False
        self.health = config.MAX_PLAYER_HEALTH
        self.is_invincible = False
        self.invincibility_timer = 0
        self.visible = True
        self.velocity_x = config.MOVE_SPEED
        self.is_slowed = False
        self.slowing_timer = 0

        self.direction = "right" # Track facing direction ( default : right- facing )
        self.collision_direction = "none" 
        self.collision_direction = "none"''

        # player's asset managing
        self.character_type = character_type
        self.state = "idle" 
        self.assets = AssetManager.player_assets[character_type]
        self.current_frame = 0
        self.image = self.assets[self.state][self.current_frame]
        self.rect = self.image.get_rect(topleft=(100, 0))

        #tyoe of weapon
        self.weapon = config.WEAPONS[self.character_type]
        #held bullet animation
        self.is_shooting = False
        self.attack_animation = False

        #type of bullet 
        if self.weapon == "bow" :
            self.bullet_type = "arrow"
        elif self.weapon == "wand" :
            self.bullet_type = "fireball"

        self.held_bullet = Bullet(self, self.bullet_type) # Create a bullet that follows the player (not fired yet)

        self.max_jumps = 1
        self.jump_count = 0
        self.jumped = False
        self.shield_activated = False
        

    def check_vertical_collision(self, platforms):
        landed_on = None
        # Check vertical collision (falling)
        if self.velocity_y > 0 :
            for platform in platforms:
                if isinstance(platform, Platform) and platform.visible:
                    if (self.rect.bottom + self.velocity_y > platform.rect.top and
                        self.rect.top < platform.rect.top and
                        self.rect.right > platform.rect.left and 
                        self.rect.left < platform.rect.right):
                        self.rect.bottom = platform.rect.top
                        self.velocity_y = 0
                        self.on_ground = True
                        landed_on = platform
                        self.jump_count = 0
                        #return platform
                        break
                elif not isinstance(platform, Platform):
                    if (self.rect.bottom + self.velocity_y > platform.top and
                        self.rect.top < platform.top and
                        self.rect.right > platform.left and 
                        self.rect.left < platform.right):
                        self.rect.bottom = platform.top
                        self.velocity_y = 0
                        self.on_ground = True
                        self.jump_count = 0
                        break
                        #return platform
        
        # Check vertical collision (jumping)
        for platform in platforms:
            if isinstance(platform, Platform) and platform.is_solid and platform.visible :
                if (self.velocity_y < 0 and
                    self.rect.top < platform.rect.bottom and
                    self.rect.bottom > platform.rect.bottom and
                    self.rect.right > platform.rect.left and 
                    self.rect.left < platform.rect.right):
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0
                    self.jump_count = 0
                    break
                    #return platform
        
        if self.velocity_y == 0:
                for platform in platforms:
                    rect = platform.rect if isinstance(platform, Platform) else platform
                    if self.rect.bottom == rect.top and \
                    self.rect.right > rect.left and self.rect.left < rect.right:
                        landed_on = platform
                        break

        self.on_ground = bool(landed_on)
        return landed_on

    
    def check_horizontal_collision(self,platforms):
        for platform in platforms :
            if isinstance(platform, Platform) and platform.visible:
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
        return None

    def check_enemy_collision(self,enemies):
        for enemy in enemies:
            if isinstance(enemy, Enemy):
                if self.rect.colliderect(enemy.rect):
                    #stomp enemy to kill it;  other collisions reduce player's health
                    if(self.velocity_y > 0 and
                        self.rect.bottom <= enemy.rect.top + 10):
                        enemy.health -= 1
                        self.velocity_y = config.JUMP_VELOCITY * 0.5
                        return 
                    elif(enemy.is_collided == False) :
                        self.health -= 1
                        enemy.is_collided = True
                        self.is_invincible = True
                        return enemy
    def check_powerup_collision(self, powerups):
        for powerup in powerups:
            if self.rect.colliderect(powerup.rect):
                if powerup.type == "doublejump":
                    self.max_jumps = 2
                    powerup.visible = False
                if powerup.type == "shield":
                    self.is_invincible = True 
                    self.shield_activated = True
                    powerup.visible = False
                if powerup.type == "damageboost":
                    self.held_bullet.damage += 1
                    powerup.visible = False

    def update(self, platforms, enemies, powerups):
        keys = pygame.key.get_pressed()
        self.update_image(keys)
        
        # Horizontal movement
        self.velocity_x = config.MOVE_SPEED - 3 if self.is_slowed else config.MOVE_SPEED

        if (keys[pygame.K_a] and self.collision_direction != "left"):
            self.rect.x -= self.velocity_x
            self.direction = "left" # Update facing direction

        if (keys[pygame.K_d] and self.collision_direction != "right"):
            self.rect.x += self.velocity_x
            self.direction = "right" # Update facing direction
        if self.rect.x <= 0 :
            self.rect.x = 0
            
        # Apply gravity
        self.velocity_y += config.GRAVITY
        self.rect.y += self.velocity_y
        
        # Check collisions
        collided_platform = self.check_vertical_collision(platforms)
        #print("collided:", collided_platform.type if collided_platform else None)
        if collided_platform != None and collided_platform != self.game.ground_rect :
            if collided_platform.type == 'timed':
                collided_platform.timed_platform()
            elif collided_platform.type == 'bouncy':
                collided_platform.bouncy_platform()
            elif collided_platform.type == 'slowing':
                if self.velocity_x >= 3:
                    collided_platform.slowing_platform()
            elif collided_platform.type == 'spikey' and self.is_invincible == False :
                self.health -= 1
                self.is_invincible = True
            
        self.check_horizontal_collision(platforms)
        self.check_enemy_collision(enemies)
        self.check_powerup_collision(powerups)


        # Temporary flickering after collision with an enemy
        if self.is_invincible :
            self.invincibility_timer += 1
            if self.invincibility_timer % 15 < 8 :
                self.visible = True
            else :
                self.visible = False
            if self.shield_activated and self.invincibility_timer >= 180:
                self.is_invincible = False
                self.shield_activated = False
            elif self.shield_activated == False and self.invincibility_timer >= 50:
                self.is_invincible = False
        else :
            self.visible = True
            self.invincibility_timer = 0

        if self.is_slowed :
            self.slowing_timer += 1
            if self.slowing_timer >= 15 :
                self.is_slowed = False
                self.slowing_timer = 0



        # Game over when player dies
        if self.health <= 0 or self.rect.y >= 600:
            self.game.gameover()
            
        # Jumping (only if on ground)
        if (keys[pygame.K_UP] or keys[pygame.K_SPACE]):
            if not self.jumped and (self.on_ground or self.jump_count < self.max_jumps) :
                self.jump_count += 1
                self.velocity_y = config.JUMP_VELOCITY
                self.on_ground = False
            self.jumped = True
        else :
            self.jumped = False

        #shoot_animation
        if self.is_shooting == True :
            self.attack_animation = True
            self.is_shooting = False
        #shoot
        if (self.current_frame >= config.SHOOT_FRAME[self.weapon]  and 
        self.current_frame < config.SHOOT_FRAME[self.weapon] + config.PLAYER_FRAMES_SPEED and 
        self.state == "attack") :
            self.shoot()

            
        # Update held bullet (follows player if not fired)
        self.held_bullet.update()

    def update_image (self, keys) :

        if self.attack_animation == True :
            if self.state != "attack" :
                self.current_frame = 0
                self.state = "attack"
            elif self.state == "attack" and self.current_frame >= len(self.assets [self.state]) - (2 * config.PLAYER_FRAMES_SPEED) :
                self.attack_animation = False

        elif (self.on_ground and ( not ( keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_UP] or keys[pygame.K_SPACE] ) ) ):
            if(self.state != "idle"):
                self.current_frame = 0
                self.state = "idle"

        elif ( (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and self.on_ground) :

            self.current_frame = 0
            self.state = "jumping"
            
        elif not self.on_ground :

            if(self.state != "falling" and self.velocity_y > 0) :
                self.current_frame = 0
                self.state = "falling"
        
        elif (keys[pygame.K_a] or keys[pygame.K_d]) and self.on_ground :
            if(self.state != "run" ):
                self.current_frame = 0
                self.state = "run"
    
        self.image = self.assets[self.state][int(self.current_frame)]
        
        self.current_frame += config.PLAYER_FRAMES_SPEED
        if(self.current_frame >= len(self.assets[self.state])) :
            self.current_frame = 0
        

    def shoot (self) :
        
        # Trigger the held bullet to be fired
        self.held_bullet.fire()

        # Create a new bullet that will follow the player (for next shot)
        self.held_bullet = Bullet (self, self.held_bullet.type)