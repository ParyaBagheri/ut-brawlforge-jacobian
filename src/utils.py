import pygame
''', pytmx
from pytmx.util_pygame import load_pygame'''

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x,y))

class Tiledmap:
    def __init__(self, filename):
        self.tmx_data = load_pygame(filename)
    def render(self, surface, offset) :
        start_x = offset // self.tmx_data.tilewidth
        end_x = offset + surface.get_width()
        start_y = 0
        end_y = surface.get_height()
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for y in range(start_y, end_y):
                    for x in range(start_x, end_x):
                        if 0 <= x < self.tmx_data.width and 0 <= y < self.tmx_data.height:
                            tile_id = layer.data[y][x]
                            if tile_id:
                                tile_image = self.tmx_data.get_tile_image_by_gid(tile_id)
                                if tile_image:
                                    surface.blit(tile_image, (x * self.tmx_data.tilewidth - offset, y * self.tmx_data.tileheight))
                    
