import pygame
from src.engine.platform import Platform
import config


def get_level_data(name, game):
    if name == "forest":
        platform_img = pygame.image.load("src/assets/images/platform.png").convert_alpha()
        return{
            "background_layers" : [
                (pygame.image.load("src/assets/images/forest/backgrounds/L7.png").convert(), 0.1),
                (pygame.image.load("src/assets/images/forest/backgrounds/L5.png").convert_alpha(), 0.2),
                (pygame.image.load("src/assets/images/forest/backgrounds/L4.png").convert_alpha(), 0.3),
                (pygame.image.load("src/assets/images/forest/backgrounds/L6.png").convert_alpha(), 0.4),
                (pygame.image.load("src/assets/images/forest/backgrounds/L2.png").convert_alpha(), 0.5),
                (pygame.image.load("src/assets/images/forest/backgrounds/L3.png").convert_alpha(), 0.5),
                (pygame.image.load("src/assets/images/forest/backgrounds/L0.png").convert_alpha(), 0.7),
                (pygame.image.load("src/assets/images/forest/backgrounds/L1.png").convert_alpha(), 0.7),
            ],
            "platforms" : [
                Platform(game, 300, 400, 150, 20, 'solid', image=platform_img),
                Platform(game, 600, 300, 150, 20, 'solid', image=platform_img),
                Platform(game, 750, 300, 250, 20, 'solid'), #Fragile platform
                Platform(game, 1050, 200, 100, 20, 'solid'), # Bonus on this platform
                Platform(game, 1140, 560 - config.BASE_GROUND_HEIGHT, 50, 40, 'bouncy'), #Bouncy platform
                Platform(game, 1250, 300, 300, 20, 'solid'),
                Platform(game, 1400, 600 - config.BASE_GROUND_HEIGHT, 350, 20, 'slowing'), #Muddy platform
                Platform(game, 1630, 200, 100, 20, 'timed'),
                Platform(game, 1700, 300, 100, 20, 'solid'),
                Platform(game, 1800, 300, 250, 20, 'slowing'),
                Platform(game, 2250, 200, 100, 20, 'timed'),
                Platform(game, 2400, 300, 300, 20, 'solid'),
                Platform(game, 2800, 200, 100, 20, 'timed'),
                Platform(game, 3000, 100, 100, 20, 'timed'),
                Platform(game, 3150, 250, 200, 100, 'solid'), #Finish platform
                #Platform(self, 3050, 560 - config.BASE_GROUND_HEIGHT, 50, 40, 'bouncy')
                game.ground_rect
            ],
            "enemies" : [],
        }
    elif name == "desert":
        return{
            "background_layers" : [
                (pygame.image.load("src/assets/images/forest/backgrounds/L7.png").convert(), 0),
            ],
            "platforms" : [
                Platform(game, 0, 100, 400, 500),
                Platform(game, 500, 0, 4850, 100),
                Platform(game, 400, 400, 300, 200), 
                Platform(game, 700, 500, 300, 100),
                Platform(game, 1000, 510, 400, 90, 'spikey'),
                Platform(game, 1100, 450, 200, 20),
                Platform(game, 1400, 300, 600, 300),
                Platform(game, 2000, 500, 500, 100, 'spikey'),
                Platform(game, 2050, 450, 100, 20),
                Platform(game, 2200, 450, 200, 20, 'timed'),
                Platform(game, 2500, 450, 200, 150),
                Platform(game, 2700, 500, 700, 100, 'spikey'),
                Platform(game, 2800, 350, 100, 20, 'timed'),
                Platform(game, 3000, 400, 100, 20),
                Platform(game, 3200, 300, 150, 20),
                Platform(game, 3400, 400, 200, 200),
                Platform(game, 3600, 500, 300, 100, 'spikey'),
                Platform(game, 3700, 350, 100, 20),
                Platform(game, 3900, 400, 50, 200),
                Platform(game, 3950, 450, 50, 150),
                Platform(game, 4000, 480, 100, 120),
                Platform(game, 4025, 440, 50, 40, 'bouncy'),
                Platform(game, 4100, 500, 850, 100, 'spikey'),
                Platform(game, 4200, 300, 200, 20),
                Platform(game, 4500, 400, 150, 20),
                Platform(game, 4700, 300, 150, 20),
                Platform(game, 4950, 400, 450, 200),
                Platform(game, 5400, 300, 150, 300),
                Platform(game, 5550, 200, 6600, 400) 
                #Finish Line at 6000
            ],
            "enemies" : []
        }
    
    else:
        raise ValueError(f"Unknown level : {name}")
