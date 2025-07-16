import pygame
import sys

class Button :
    def __init__(self, game, image, pos, text_input, font, fontsize, color, hovercolor):
        self.game = game
        self.image = image
        self.font = pygame.font.Font("src/assets/fonts/"+ font + ".ttf", fontsize)
        self.x = pos[0]
        self.y = pos[1]
        self.text_input = text_input
        self.color = color
        self.hovercolor = hovercolor
        self.text = self.font.render(text_input, True, color)
        if self.image is None :
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x,self.y))
        self.text_rect = self.text.get_rect(center=(self.x,self.y))

    def draw(self, mouse_pos):
        is_hovered = self.rect.collidepoint(mouse_pos[0], mouse_pos[1])
        text_color = self.hovercolor if is_hovered else self.color
        self.text = self.font.render(self.text_input, True, text_color)
        if self.image is not None:
            self.game.screen.blit(self.image, self.rect)
        self.game.screen.blit(self.text, self.text_rect)
    
    def is_pressed(self, mouse_pos):
        if mouse_pos[0] in range(self.rect.left, self.rect.right) and mouse_pos[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False    

    