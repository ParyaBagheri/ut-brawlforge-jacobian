import pygame
import config
from src.engine.enemy import Enemy
from src.engine.bullet import Bullet
from src.engine.platform import Platform
from src.engine.assetmanager import AssetManager


class Player:
    def __init__(self, game,character_type, start_x=100, id = None, nickname = None):
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
        #sounds
        self.sound_effects = AssetManager.player_sounds
        self.mute = False
        self.damage_sound = False
        self.attack_sound = False
        self.bounce_sound = False
        self.collect_sound = False
        # images
        self.character_type = character_type
        self.state = "idle" 
        self.assets = AssetManager.player_images[character_type]
        self.current_frame = 0
        self.image = self.assets[self.state][self.current_frame]
        self.rect = self.image.get_rect(topleft=(start_x, 0))
        # type of weapon
        self.weapon = config.WEAPONS[self.character_type]
        # attack 
        self.is_shooting = False
        self.attack_animation = False
        # type of bullet 
        if self.weapon == "bow" :
            self.bullet_type = "arrow"
        elif self.weapon == "wand" :
            self.bullet_type = "fireball"
        # die animation 
        self.is_dead = False

        self.held_bullet = Bullet(self, self.bullet_type) # Create a bullet that follows the player (not fired yet)
        self.held_bullet.owner = self

        self.max_jumps = 1
        self.jump_count = 0
        self.jumped = False
        self.shield_activated = False

        # MULTIPLAYER
        self.id = id
        self.nickname = nickname

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

                        # playing damage sound when the player is damaged
                        self.damage_sound = True

                        enemy.is_collided = True
                        self.is_invincible = True
                        return enemy
    def check_powerup_collision(self, powerups):
        for powerup in powerups:
            if self.rect.colliderect(powerup.rect):
                self.collect_sound = True
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
                if powerup.type == "health" :
                    self.health += 1
                    powerup.visible = False
                powerup.kill()
                

    def update(self, platforms, powerups, enemies=None):
        keys = pygame.key.get_pressed()
        if not self.is_dead:
            self.update_animation(keys)
        if self.state != "die" :
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
                    # bounce sound effect
                    self.bounce_sound = True
                elif collided_platform.type == 'slowing':
                    if self.velocity_x >= 3:
                        collided_platform.slowing_platform()
                elif collided_platform.type == 'spikey' and self.is_invincible == False :
                    self.damage_sound = True
                    self.health -= 1
                    self.is_invincible = True

            self.check_horizontal_collision(platforms)
            if enemies : self.check_enemy_collision(enemies)
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
                elif self.shield_activated == False and self.invincibility_timer >= 50 :
                    self.is_invincible = False
            else :
                self.visible = True
                self.invincibility_timer = 0

            if self.is_slowed :
                self.slowing_timer += 1
                if self.slowing_timer >= 15 :
                    self.is_slowed = False
                    self.slowing_timer = 0

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
                self.attack_sound = True
                self.shoot()


            # Update held bullet (follows player if not fired)
            self.held_bullet.update()
        elif self.is_dead == True :
            # Game over when player dies
            self.game.gameover()

    def update_animation (self, keys) :
        prev_state = self.state
        if (self.health <= 0 or self.rect.y >= 600 ) :
            if self.state != "die" :
                self.current_frame = 0
                self.state = "die"
            elif self.state == "die" and self.current_frame >= len(self.assets [self.state]) - (3 * config.PLAYER_FRAMES_SPEED) :
                self.is_dead = True

        elif self.attack_animation == True :
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
        self.sound_manager(prev_state)

    def sound_manager(self, prev_state) :
        if not self.mute :
            if self.collect_sound :
                self.sound_effects["collect"].play()
                self.collect_sound = False
            if self.bounce_sound == True :
                self.sound_effects["bounce"].play()
                self.bounce_sound = False
            if self.state == "jumping" and prev_state != "jumping" :
                self.sound_effects["jump"].play()

            if self.state == "run" and prev_state != "run" :
                self.sound_effects ["running"].play(loops=-1)

            if (self.state != "run" and prev_state == "run"):
                self.sound_effects["running"].stop()
                

            if self.damage_sound :
                self.sound_effects["damage"].play()
                self.damage_sound = False

            if self.attack_sound :
                self.sound_effects["attack"].play()
                self.attack_sound = False
            if self.is_dead and self.state == "die" :
                self.sound_effects["game over"].play()

    def reset (self) :
        self.rect.x = 100
        self.rect.top = 0
        self.invincibility_timer = 0
        self.is_invincible = False
        self.max_jumps = 1
        self.health = config.MAX_PLAYER_HEALTH
        self.state = "idle"
        self.is_dead = False
        self.current_frame = 0 
        self.color = (255, 0, 0)
        
        self.sound_effects["running"].stop()
         
                    

    def shoot (self) :

        # Trigger the held bullet to be fired
        self.held_bullet.fire()

        # Create a new bullet that will follow the player (for next shot)
        self.held_bullet = Bullet(self, self.held_bullet.type)
        self.held_bullet.owner = self

    def sync_remote_players (self, updated_status) :
        prev_state = self.state
        if self.state != "die":
            self.x =  updated_status["x"]
            self.y =  updated_status["y"]
            self.state = updated_status["state"]
            self.health = updated_status["health"]
            self.direction = updated_status["direction"]
            #self.check_powerup_collision(self.game.level.powerups)
            # Shoot
            if (self.current_frame >= config.SHOOT_FRAME[self.weapon]  and 
            self.current_frame < config.SHOOT_FRAME[self.weapon] + config.PLAYER_FRAMES_SPEED and 
            self.state == "attack") :
                self.attack_sound = True
                self.shoot()
        if not self.is_dead :
            self.remote_players_animation_update(prev_state)
    def remote_players_animation_update (self, prev_state) :
        if self.state !=  prev_state :
            self.current_frame = 0 
        if self.state == "die" and self.current_frame >= len(self.assets [self.state]) - (3 * config.PLAYER_FRAMES_SPEED) :
            self.is_dead = True
        self.image = self.assets[self.state][int(self.current_frame)]

        self.current_frame += config.PLAYER_FRAMES_SPEED
        if(self.current_frame >= len(self.assets[self.state])) :
            self.current_frame = 0
        self.remote_players_sound_manager(prev_state)
    def remote_players_sound_manager(self,prev_state) :
        if self.attack_sound :
            self.sound_effects["attack"].play()
            self.attack_sound = False
            