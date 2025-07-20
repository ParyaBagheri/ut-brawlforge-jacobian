from src.engine import data_loader
from src.utils import Tiledmap
class Level:
    def __init__(self,name, game, width, winFunc=None, loseFunc=None):
        self.name = name
        self.game = game
        self.width = width
        #self.tilemap = Tiledmap(f"src/assets/tiles and maps/{name}.tmx")
        #self.platforms = platforms
        #self.entities = entities
        self.background_layers = []
        self.platforms = []
        self.enemies = []
        self.powerups = []
        self.winFunc = winFunc
        self.loseFunc = loseFunc
        self.load()

    def load(self):
        data = data_loader.get_level_data(self.name, self.game)

        #self.background_layers = data["background_layers"]
        self.platforms = data["platforms"]
        self.powerups = data["powerups"]
        print(f"[DEBUG] Loaded powerups: {len(self.powerups)}")
        #self.enemies = data["enemies"]
        #self.player = data["player"]
    def won(self):
        if self.winFunc is None:
            return False
        return self.winFunc()
    def lost(self):
        if self.loseFunc is None:
            return False
        return self.loseFunc()
    
