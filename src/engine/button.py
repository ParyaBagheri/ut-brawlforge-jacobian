import pygame
import sys

class Button :
    def __init__(self, game, image, pos, text_input, font, color, hovercolor):
        self.game = game
        self.image = image
        self.x = pos[0]
        self.y = pos[1]
        self.text_input = text_input
        self.color = color
        self.hovercolor = hovercolor
        self.text = text_input.render(text_input, True, color)
        if self.image is None :
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x,self.y))
        self.text_rect = self.text.get_rect(center=(self.x,self.y))

    #def draw(self):
        #if self.image is not None:
            #screen.blit()