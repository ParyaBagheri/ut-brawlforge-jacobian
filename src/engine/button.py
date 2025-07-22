import pygame
import sys
import config
from src.engine.assetmanager import AssetManager
class Button :
    def __init__(self, game, frames, pos, text_input, font, fontsize, color, hovercolor):
        self.game = game
        self.frames = frames
        self.current_frame = 0
        self.font = pygame.font.Font("src/assets/fonts/" + font + ".ttf", fontsize)
        self.x = pos[0]
        self.y = pos[1]
        self.text_input = text_input
        self.color = color
        self.hovercolor = hovercolor
        self.state = "default"
        self.text = self.font.render(text_input, True, color)
        if self.frames is None :
            self.image = self.text
            self.text_rect = self.text.get_rect(center=(self.x,self.y)) 
            self.image_rect = self.text_rect  
        else :
            self.image = self.frames[0]
            self.not_hovered_image = self.frames[0]
            self.image_rect = self.image.get_rect(center=(self.x,self.y))
            self.text_rect = self.text.get_rect(center=(self.x,self.image_rect.bottom + fontsize/2 ))
        self.rect = self.image_rect.union(self.text_rect)

    def draw(self, mouse_pos):
        is_hovered = self.rect.collidepoint(mouse_pos[0], mouse_pos[1])
        if is_hovered :
            self.sound_manager("hovered")
        else :
            self.sound_manager("default")
        text_color = self.hovercolor if is_hovered else self.color
        self.text = self.font.render(self.text_input, True, text_color)
        if self.frames is not None:
            if is_hovered :
                self.image = self.frames[int(self.current_frame)]
                self.current_frame += config.BUTTON_FRAMES_SPEED 
                if self.current_frame < len(self.frames) :
                    self.current_frame = len(self.frames)-1                   
            else :
                self.current_frame = 0
                self.image = self.not_hovered_image
            self.game.screen.blit(self.image, self.image_rect)
            
        self.game.screen.blit(self.text, self.text_rect)
    
    def is_pressed(self, mouse_pos):
        if mouse_pos[0] in range(self.rect.left, self.rect.right) and mouse_pos[1] in range(self.rect.top, self.rect.bottom):
            self.sound_manager("pressed")
            return True
        self.sound_manager("default")
        return False    
    def sound_manager(self, newstate) :
        if newstate != self.state :
            if newstate == "pressed" :
                AssetManager.UI_sounds["click"].play()
                self.state = "pressed"
            elif newstate == "hovered" :
                AssetManager.UI_sounds["hover"].play()
                self.state = "hovered"
            elif newstate == "default" :
                self.state= "default"