import pygame
import sys

GRAVITY = 1
JUMP_VELOCITY = -18
MOVE_SPEED = 5
BASE_GROUND_HEIGHT = 100
BASE_SCREEN_WIDTH = 800
BASE_SCREEN_HEIGHT = 600
MAX_ENEMY_HEALTH = 1
INITIAL_ENEMY_SPEED = 5
MAX_PLAYER_HEALTH = 3

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
    
    def update(self, platforms):
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
            
        # Jumping (only if on ground)
        if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and self.on_ground:
            self.velocity_y = JUMP_VELOCITY
            self.on_ground = False

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
    
    def update(self):
        self.player.update(self.platforms)
        self.update_camera()
    
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

if __name__ == "__main__":
    game = Game()
    game.run()
