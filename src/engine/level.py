import pygame
from src.engine import data_loader
from src.utils import Tiledmap
class Level:
    def __init__(self,name, game, width, winFunc=None, loseFunc=None):
        self.name = name
        self.game = game
        self.width = width
        self.background_layers = []
        self.platforms = []
        self.enemies = []
        self.powerups = []
        self.map = None
        self.winFunc = winFunc
        self.loseFunc = loseFunc
        self.load()

    def load(self):
        data = data_loader.get_level_data(self.name, self.game)
        self.map = data["map"]
        self.background_layers = list(data["background_layers"])[0]
        self.platforms = data["platforms"]
        self.powerups = data["powerups"]
        self.powerup_group = pygame.sprite.Group(self.powerups)
        self.enemies = data["enemies"]
        self.enemies_group = data["enemies"]
        print(f"[DEBUG] Loaded powerups: {len(self.powerups)}")
        self.enemies = data["enemies"]
    def won(self):
        if self.winFunc is None:
            return False
        return self.winFunc()
    def lost(self):
        if self.loseFunc is None:
            return False
        return self.loseFunc()
    
