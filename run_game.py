import pygame
import sys
import os

GRAVITY = 1
JUMP_VELOCITY = -18
MOVE_SPEED = 5
BASE_GROUND_HEIGHT = 100
BASE_SCREEN_WIDTH = 800
BASE_SCREEN_HEIGHT = 600
MAX_ENEMY_HEALTH = 1
INITIAL_ENEMY_SPEED = 5
MAX_PLAYER_HEALTH = 3
BULLET_SPEED = 30
BULLET_DAMAGE = 5

right_bullet_image_path = os.path.join("src","assets", "images" , "rightpaintball.png")
left_bullet_image_path = os.path.join("src","assets", "images" , "rightpaintball.png")

right_bullet_image = pygame.image.load(right_bullet_image_path)
right_bullet_image = pygame.transform.scale(right_bullet_image, (20, 20))
left_bullet_image = pygame.image.load(left_bullet_image_path)
left_bullet_image = pygame.transform.scale(left_bullet_image, (20, 20))

pygame.font.init()
font = pygame.font.SysFont('Arial',  32, True, False)
heartfont = pygame.font.SysFont('Segoe UI Symbol', 40)
gameoverfont = pygame.font.SysFont('OCR A Extended', 72)

class Platform:
    def __init__(self, x, y, width, height, color=(139, 69, 19), is_solid=True):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.is_solid = is_solid  # Determines if platform is solid for collision
    
    def draw(self, screen, camera_x):
        # Draw platform with camera offset
        draw_rect = pygame.Rect(self.rect.x - camera_x, self.rect.y, 
                               self.rect.width, self.rect.height)
        pygame.draw.rect(screen, self.color, draw_rect)

class Player:
    def __init__(self, game):
        self.game = game
        self.rect = pygame.Rect(100, 300, 50, 80)
        self.velocity_y = 0
        self.on_ground = False
        self.color = (255, 0, 0)  # Player color (red)
        self.health = MAX_PLAYER_HEALTH

    def check_collision(self, platforms):
        # Check vertical collision (falling)
        if self.velocity_y > 0:
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
    
    def check_enemy_collision(self,enemies):
        for enemy in enemies:
            if isinstance(enemy, Enemy):
                if self.rect.colliderect(enemy.rect):
                    #stomp enemy to kill it;  other collisions reduce player's health
                    if(self.velocity_y > 0 and
                        self.rect.bottom > enemy.rect.top and
                        self.rect.top < enemy.rect.top):
                        enemy.health -= 1
                        self.velocity_y = JUMP_VELOCITY * 0.5
                    else :
                        self.health -= 1
                        if self.health > 0:
                            self.rect.y -= 30
                        enemy.is_collided = True
                        return enemy
    
    def update(self, platforms, enemies):
        keys = pygame.key.get_pressed()
        
        # Horizontal movement
        if keys[pygame.K_LEFT]:
            self.rect.x -= MOVE_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += MOVE_SPEED
            
        # Apply gravity
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y
        
        # Check collisions
        self.check_collision(platforms)
        self.check_enemy_collision(enemies)

        # Game over when player dies
        if self.health <= 0:
            game.gameover()
            
        # Jumping (only if on ground)
        if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and self.on_ground:
            self.velocity_y = JUMP_VELOCITY
            self.on_ground = False

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
            if self.check_platform_collision() :
                self.game.Fired_bullets_list.remove(self)
    
        else :

            # Bullet hasn't been fired yet - follow player position 
            self.rect.x = self.player.rect.centerx - 10
            self.rect.y = self.player.rect.centery - 10
    
    def check_enemy_collision (self) :
        if self.is_fired == True :
            for enemy in self.game.enemies :
                if isinstance (enemy, Enemy) :
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
class Enemy(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.rect = pygame.Rect(self.game.screen_width + self.game.camera_x , 450, 50, 50)
        self.velocity_y = 0
        self.on_ground = False
        self.color = (60, 77, 217) 
        self.health = MAX_ENEMY_HEALTH
        self.velocity_x = -1*(INITIAL_ENEMY_SPEED)
        self.is_collided = False
    def update(self):
        self.rect.x += self.velocity_x

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((BASE_SCREEN_WIDTH, BASE_SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Platformer Game")
        self.clock = pygame.time.Clock()
        
        self.update_dimensions()
        
        # Create platforms and ground
        self.platforms = [
            Platform(300, 400, 200, 20),
            Platform(600, 350, 150, 20),
            Platform(900, 300, 100, 20),
            Platform(1200, 400, 200, 20),
            self.ground_rect
        ]
        
        self.player = Player(self)
        self.camera_x = 0
        self.enemies = pygame.sprite.Group()
        enemy = Enemy(self)
        self.enemies.add(enemy)

        self.isGameover = False

    def update_dimensions(self):
        # Update screen and ground dimensions based on current window size
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.ground_rect = pygame.Rect(0, self.screen_height - BASE_GROUND_HEIGHT, self.screen_width * 10, BASE_GROUND_HEIGHT)

    def update_camera(self):
        # Camera follows the player horizontally
        self.camera_x = self.player.rect.centerx - self.screen_width // 2
        max_camera_x = self.ground_rect.width - self.screen_width
        self.camera_x = max(0, min(self.camera_x, max_camera_x))
    
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                # Resize window and update dimensions
                self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                self.update_dimensions()
            # Restart after game over
            elif self.isGameover == True and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.player
                self.player.health = MAX_PLAYER_HEALTH
                self.player.color = (255, 0, 0)
                self.isGameover = False
    
    def update(self):
        if self.isGameover == False:
            self.player.update(self.platforms, self.enemies)
            self.update_camera()
            for enemy in self.enemies:
                enemy.update()
            # Remove dead enemies and spawn new ones
            for enemy in self.enemies:
                if enemy.rect.x <= 0 + self.camera_x or enemy.health <= 0 or self.isGameover == True:
                    enemy.kill()
                    new_enemy = Enemy(self)
                    self.enemies.add(new_enemy)
    
    def draw(self):
        self.screen.fill((135, 206, 235))  # Sky blue background
        
        # Draw platforms and ground
        for platform in self.platforms:
            if isinstance(platform, Platform):
                platform.draw(self.screen, self.camera_x)
            else:
                pygame.draw.rect(self.screen, (34, 139, 34), 
                               pygame.Rect(platform.x - self.camera_x, 
                                          platform.y, 
                                          platform.width, 
                                          platform.height))
        
        # Draw player
        pygame.draw.rect(self.screen, self.player.color, 
                        pygame.Rect(self.player.rect.x - self.camera_x, 
                                   self.player.rect.y, 
                                   self.player.rect.width, 
                                   self.player.rect.height))
        
        # Draw enemies
        for enemy in self.enemies:
            pygame.draw.rect(self.screen, enemy.color,
                             pygame.Rect(enemy.rect.x - self.camera_x, 
                                        enemy.rect.y, 
                                        enemy.rect.width, 
                                        enemy.rect.height))
            
        # Show health
        health_display = font.render("Health: " + str(self.player.health), True, 'white')
        self.screen.blit(health_display, (20,20))
        heart = heartfont.render("♥", True, "red")
        if self.player.health >= 0:
            for i in range(0,self.player.health):
                self.screen.blit(heart, (40 + 30*i , 40))
        # Show game over
        if self.isGameover == True:
            gameover_message = gameoverfont.render("GAME OVER!", True, 'black')
            text_rect = gameover_message.get_rect()
            text_rect.center = (self.screen_width //2, self.screen_height//2)
            self.screen.blit(gameover_message, text_rect)

    def gameover(self):
        self.isGameover = True
        self.player.color = (0, 0, 0)
        self.player.rect.x = 100

if __name__ == "__main__":
    game = Game()
    game.run()
