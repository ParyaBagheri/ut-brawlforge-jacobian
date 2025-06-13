import pygame

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