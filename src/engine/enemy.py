import pygame
import config
from src.engine.platform import Platform
from src.engine.bullet import Bullet
from src.engine.assetmanager import AssetManager

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.rect = pygame.Rect(self.game.screen_width + self.game.camera_x , 450, 50, 50)
        self.velocity_y = 0
        self.on_ground = False
        self.color = (60, 77, 217) 
        self.health = config.MAX_ENEMY_HEALTH
        self.velocity_x = -1*(config.INITIAL_ENEMY_SPEED)
        self.is_collided = False
        self.state = "idle"
    def update(self):
        self.rect.x += self.velocity_x

    def got_shot(self, damage):
        self.health -= damage

class Bomber (Enemy,pygame.sprite.Sprite ) :
    # A mobile enemy that chases the player and explodes on contact

    def __init__(self, game,start_x,start_y) :
        super().__init__(game)
        self.rect  = pygame.Rect(start_x,start_y , 50, 50 )
        self.velocity_x = config.INITIAL_ENEMY_SPEED
        self.direction = "right"
        self.game = game
        self.type = "bomber"
        # Animation handling
        self.current_frame = 0
        self.assets = AssetManager.enemy_assets["bomber"]
        self.image = self.assets["idle"][0]
        self.is_inview = False
        self.state = "idle"
        
        self.is_collided = False

    def update (self) :
        # Update bomber position, state, and animations

        prev_state = self.state # Track previous state for animation transitions

        # Check if bomber is visible on screen
        if (self.rect.x >= 0 + self.game.camera_x and self.rect.x - self.game.camera_x <= config.BASE_SCREEN_WIDTH - 50):
            self.is_inview = True
        else :
            self.is_inview = False

        # Only update if visible
        if self.is_inview :

            # Check if bomber should die (no health or collided with player)
            if self.health <= 0 or self.rect.colliderect(self.game.player.rect):
                self.health = 0
                self.state = "death"
            # Chase player if player is not over the bomber
            elif (self.game.player.rect.bottom >= self.rect.bottom) :
                self.state = "run"

            else :
                self.state = "idle"

            # Movement logic when in run state
            if self.state == "run" :

                if self.game.player.rect.x - self.rect.x >= 50:
                    self.direction = "right"
                    self.rect.x += self.velocity_x
                elif self.game.player.rect.x - self.rect.x <= -50:
                    self.direction = "left"
                    self.rect.x -= self.velocity_x

            # Prevent moving off left edge of screen
            if self.rect.x <= 0 :
                self.rect.left = 0
                self.state = "idle"
                self.direction = "right"

            # Apply gravity
            self.velocity_y += config.GRAVITY
            self.check_platform_collision() # Handle platform collisions
            self.rect.y += self.velocity_y # Apply vertical movement
            # Update animation frames
            self.update_animation(prev_state)
            
    def check_platform_collision (self):
        # Check vertical collision (falling)
        if self.velocity_y > 0 :
            for platform in self.game.level.platforms:
                if isinstance(platform, Platform) and platform.visible:
                    if (self.rect.bottom + self.velocity_y > platform.rect.top and
                        self.rect.top < platform.rect.top and
                        self.rect.right > platform.rect.left and 
                        self.rect.left < platform.rect.right):
                        self.rect.bottom = platform.rect.top
                        self.velocity_y = 0
                        break
                elif not isinstance(platform, Platform):
                    if (self.rect.bottom + self.velocity_y > platform.top and
                        self.rect.top < platform.top and
                        self.rect.right > platform.left and 
                        self.rect.left < platform.right):
                        self.rect.bottom = platform.top
                        self.velocity_y = 0
                        break

        # Check horizontal collision
        for platform in self.game.level.platforms :
            if isinstance(platform, Platform) and platform.visible:
                if(self.rect.top < platform.rect.bottom and
                    self.rect.bottom > platform.rect.top) :
                    if(self.direction == "right" and
                       self.rect.right >= platform.rect.left and self.rect.right <= platform.rect.right):
                        self.rect.right = platform.rect.left
                        return platform
                    elif(self.direction == "left" and
                        self.rect.left <=  platform.rect.right and self.rect.left >= platform.rect.left):
                        self.rect.left = platform.rect.right
                        self.collision_direction = "left"
                        return platform
                    
    def update_animation (self, prev_state) :
        # Update animation frames based on current state

        # Reset frame counter if state changed
        if self.state != prev_state :
            self.current_frame = 0

        self.image = self.assets[self.state][int(self.current_frame)]
        self.current_frame += config.PLAYER_FRAMES_SPEED
        if(self.current_frame >= len(self.assets[self.state])) :
            if self.state == "death" :
                self.kill() # Remove sprite when death animation completes
            else :
                self.current_frame = 0 # Loop animation


class Freezerenemy(Enemy) :
    # A stationary enemy that freezes the player from a distance

    def __init__(self, game, start_x, start_y):
        super().__init__(game)
        self.start_x = start_x
        self.start_y = start_y
        self.rect = pygame.Rect(self.start_x, self.start_y, 80, 50)
        self.activated = False
        self.activation_timer = 0
        self.held_bullet = Bullet(self, 'freeze')
        self.direction = 'left'
        # Animation handling
        self.state = "idle"
        self.current_frame = 0
        self.assets = AssetManager.enemy_assets["freezer"]
        self.image = self.assets["idle"][0]
        self.type = "freezer"
    
    def update(self):
        # Update freezer state and behavior
        prev_state = self.state
        # Check if player is within activation range (800 pixels left or right)
        if self.game.player.rect.x - self.rect.x <= 800 and self.game.player.rect.x - self.rect.x >= 0:
            self.activated = True
            self.direction = 'right'
        elif self.game.player.rect.x - self.rect.x <= 0 and self.game.player.rect.x - self.rect.x >= -800 :
            self.activated = True
            self.direction = 'right'
        else :
            self.activated = False
            self.activation_timer = 0

        # Behavior when activated
        if self.activated :
            self.activation_timer += 1
            if self.activation_timer % 200 == 0:
                self.state = "attack"
                self.shoot()
            # Handle death
            if self.health <= 0 :
                self.health = 0
                self.state = "death"

            else :
                self.state = "idle"

            self.update_animation(prev_state)

    
    def shoot(self):
        # Fire a freezing projectile at the player
        self.held_bullet.fire([self.game.player.rect.x + 15 - self.rect.x , self.game.player.rect.y -self.rect.y])
        self.held_bullet = Bullet(self, 'freeze')

    def update_animation(self, prev_state):
        # Update animation frames based on current state

        # Reset frame counter if state changed
        if self.state != prev_state:
            self.current_frame = 0

        self.image = self.assets[self.state][int(self.current_frame)]
        self.current_frame += config.PLAYER_FRAMES_SPEED
        if (self.current_frame >= len(self.assets[self.state])):
            if self.state == "death" :
                self.kill() # Remove sprite when death animation completes
            else :
                self.current_frame = 0 # Loop animation

