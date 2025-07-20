import pygame, pytmx
from pytmx.util_pygame import load_pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x,y))

class Tiledmap:
    def __init__(self, filename):
        self.tmx_data = load_pygame(filename)
    def render(self, surface, offset) :
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile :
                        surface.blit(tile, ((x * self.tmx_data.tilewidth) - offset, y * self.tmx_data.tileheight))


