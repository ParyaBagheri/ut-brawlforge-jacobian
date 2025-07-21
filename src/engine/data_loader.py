import pygame , random
from src.engine.platform import Platform
from src.engine.collectible import Powerup
from src.engine.assetmanager import AssetManager
import config


def get_level_data(name, game):
    if name == "forest":
        forest_image = AssetManager.platform_images["forest"]
        return{
            "map" : AssetManager.map_image["forest"] ,
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
                Platform(game, 304, 384, 160, 24, 'solid' ),
                Platform(game, 600, 304, 192, 40, 'solid'),
                Platform(game, 750, 304, 250, 20, 'timed', image = AssetManager.platform_images["timed"]), #Fragile platform
                Platform(game, 1048, 200, 112, 16, 'solid'), # Bonus on this platform
                Platform(game, 1140, 560 - config.BASE_GROUND_HEIGHT, 50, 40, 'bouncy'), #Bouncy platform
                Platform(game, 1248, 296, 304, 24, 'solid'),
                Platform(game, 1416, 600 - config.BASE_GROUND_HEIGHT, 350, 20, 'slowing' ), #Muddy platform
                Platform(game, 1630, 200, 100, 20, 'timed', image = AssetManager.platform_images["timed"]),
                Platform(game, 1696, 296, 112, 48, 'solid'),
                Platform(game, 1808, 296, 248, 48, 'slowing'),
                Platform(game, 2250, 200, 100, 20, 'timed', image = AssetManager.platform_images["timed"]),
                Platform(game, 2400, 296, 304, 24, 'solid'),
                Platform(game, 2800, 200, 100, 20, 'timed', image = AssetManager.platform_images["timed"]),
                Platform(game, 3000, 100, 100, 20, 'timed', image = AssetManager.platform_images["timed"]),
                Platform(game, 3112, 248, 88, 72, 'solid'), #Finish platform
                #Platform(self, 3050, 560 - config.BASE_GROUND_HEIGHT, 50, 40, 'bouncy')
                game.ground_rect
            ],
            "enemies" : [],
            "powerups" : [
                Powerup(game, 1100, 50, 'shield'),
                Powerup(game, 2100, 550 - config.BASE_GROUND_HEIGHT, 'doublejump')
            ]
        }
    elif name == "desert":
        return{
            "map" : AssetManager.map_image["desert"] ,
            "background_layers" : [
                (pygame.image.load("src/assets/images/forest/backgrounds/L7.png").convert(), 0),
            ],
            "platforms" : [
                Platform(game, 0, 96, 400, 496),
                Platform(game, 504, 0, 4848, 96),
                Platform(game, 408, 400, 296, 296), 
                Platform(game, 712, 496, 280, 100),
                Platform(game, 1000, 504, 400, 24, 'spikey'),
                Platform(game, 1096, 448, 200, 24),
                Platform(game, 1408, 304, 592, 288),
                Platform(game, 2008, 504, 488, 32, 'spikey'),
                Platform(game, 2048, 448, 112, 24),
                Platform(game, 2200, 450, 200, 20, 'timed',image = AssetManager.platform_images["timed"]),
                Platform(game, 2504, 448, 196, 144),
                Platform(game, 2704, 504, 696, 32, 'spikey'),
                Platform(game, 2800, 350, 100, 20, 'timed', image = AssetManager.platform_images["timed"]),
                Platform(game, 3000, 400, 112, 24),
                Platform(game, 3200, 304, 144, 24),
                Platform(game, 3408, 400, 192, 192),
                Platform(game, 3608, 504, 288, 24, 'spikey'),
                Platform(game, 3696, 352, 112, 24),
                Platform(game, 3904, 400, 48, 192),
                Platform(game, 3952, 448, 56, 144),
                Platform(game, 4008, 480, 96, 112),
                Platform(game, 4025, 440, 50, 40, 'bouncy'),
                Platform(game, 4104, 496, 736, 24, 'spikey'),
                Platform(game, 4176, 296, 208, 32),
                Platform(game, 4496, 400, 152, 24),
                Platform(game, 4696, 296, 152, 24),
                Platform(game, 4848, 400, 544, 192),
                Platform(game, 5400, 296, 240, 296),
                Platform(game, 5648, 200, 344, 392) 
                #Finish Line at 6000
            ],
            "enemies" : [],
            "powerups" : [
                Powerup(game, 1200, 350, 'shield'),
                Powerup(game, 2300, 400, 'damageboost'),
                Powerup(game, 3950, 400, 'doublejump'),
                Powerup(game, 4580, 350, 'shield'),
                Powerup(game, 5300, 350, 'damageboost')
            ]
        }
    elif name == "lost_city":
        return{
            "map" : None ,
            "platforms" : [
                Platform(game, 0, 300, 500, 300, image = AssetManager.platform_images["lostcity"]),
                Platform(game, 600, 400, 150, 200, image = AssetManager.platform_images["lostcity"]),
                Platform(game, 850, 300, 100, 300, image = AssetManager.platform_images["lostcity"]),
                Platform(game, 1050, 250, 250, 350, image = AssetManager.platform_images["lostcity"]),
                Platform(game, 1350, 150, 150, 20, image = AssetManager.platform_images["lostcity"]),
                Platform(game, 1350, 350, 200, 250, image = AssetManager.platform_images["lostcity"]),
                Platform(game, 1600, 250, 300, 30, image = AssetManager.platform_images["lostcity"]),
                Platform(game, 2000, 350, 400, 250, image = AssetManager.platform_images["lostcity"]),
                Platform(game, 2500, 250, 100, 350, image = AssetManager.platform_images["lostcity"]),
                Platform(game, 2650, 200, 100, 30, image = AssetManager.platform_images["lostcity"]),
                Platform(game, 2800, 100, 100, 30, image = AssetManager.platform_images["lostcity"]),
                Platform(game, 2900, 220, 150, 30, 'timed', image = AssetManager.platform_images["timed"]),
                Platform(game, 3100, 300, 150, 300, image = AssetManager.platform_images["lostcity"]),
                Platform(game, 3350, 250, 150, 350, image = AssetManager.platform_images["lostcity"]),
                Platform(game, 3600, 350, 400, 250, image = AssetManager.platform_images["lostcity"]),
                Platform(game, 3600, 350, 200, 20, image = AssetManager.platform_images["lostcity"]),
                Platform(game, 4100, 300, 100, 30, image = AssetManager.platform_images["lostcity"]),
                Platform(game, 4250, 200, 100, 30, 'timed', image = AssetManager.platform_images["timed"]),
                Platform(game, 4400, 300, 100, 30, image = AssetManager.platform_images["lostcity"]),
                Platform(game, 4600, 400, 100, 30, image = AssetManager.platform_images["lostcity"]),
                Platform(game, 4800, 500, 100, 30, 'slowing', image = AssetManager.platform_images["slowing"]),
                Platform(game, 5000, 400, 150, 30, 'timed', image = AssetManager.platform_images["timed"]),
                Platform(game, 5250, 350, 100, 250, image = AssetManager.platform_images["lostcity"]),
                Platform(game, 5400, 400, 100, 30, image = AssetManager.platform_images["lostcity"]),
                Platform(game, 5600, 400, 100, 30, image = AssetManager.platform_images["lostcity"]),
                Platform(game, 5800, 400, 100, 30, image = AssetManager.platform_images["lostcity"]),
                Platform(game, 5950, 390, 250, 210, image = AssetManager.platform_images["lostcity"]),
                Platform(game, 6300, 300, 100, 30, 'timed' , image = AssetManager.platform_images["timed"]), 
                Platform(game, 6500, 350, 100, 250, image = AssetManager.platform_images["lostcity"]),
                Platform(game, 6700, 300, 100, 30, image = AssetManager.platform_images["lostcity"]),
                Platform(game, 6900, 200, 100, 30, image = AssetManager.platform_images["lostcity"]),
                Platform(game, 7100, 100, 900, 20, image = AssetManager.platform_images["lostcity"]) #Finish line at 7700
                
            ],
            "powerups" : [
                Powerup(game, 1150, 200, 'shield'),
                Powerup(game, 2850, 50, 'health'),
                Powerup(game, 4150, 250, 'doublejump'),
                Powerup(game, 5300, 300, 'shield'),
                Powerup(game, 6750, 250, 'damageboost')
            ]
        }
    elif name == "underwater":
        return{
            "map" : None ,
            "platforms" : [
                Platform(game, 0, 300, 300, 100),
                Platform(game, 450, 400, 300, 100),
                Platform(game, 750, 350, 250, 150),
                Platform(game, 1100, 330, 300, 50),
                Platform(game, 1500, 300, 150, 50),
                Platform(game, 1750, 200, 250, 50),
                Platform(game, 1660, 400, 420, 20, 'spikey'),
                Platform(game, 2100, 300, 300, 50),
                Platform(game, 2500, 400, 300, 50),
                Platform(game, 2900, 300, 300, 40),
                Platform(game, 2900, 500, 1000, 40),
                Platform(game, 3300, 200, 400, 40),
                Platform(game, 3800, 350, 300, 50),
                Platform(game, 4100, 420, 300, 20, 'spikey'), 
                Platform(game, 4250, 250, 450, 50),
                Platform(game, 4800, 200, 400, 50),
                Platform(game, 5300, 300, 400, 50), 
                Platform(game, 5800, 200, 100, 50), 
                Platform(game, 5700, 350, 100, 20, 'spikey'),
                Platform(game, 6000, 300, 100, 50),
                Platform(game, 6200, 400, 100, 50),
                Platform(game, 6400, 300, 400, 50),
                Platform(game, 6950, 300, 100, 50),
                Platform(game, 7200, 300, 150, 50),
                Platform(game, 7500, 300, 200, 50),
                Platform(game, 7800, 200, 400, 50),
                Platform(game, 8300, 300, 200, 50), 
                Platform(game, 8450, 360, 200, 20, 'spikey'),
                Platform(game, 8600, 300, 400, 50),
                Platform(game, 9100, 400, 150, 50), 
                Platform(game, 9350, 300, 150, 50),
                Platform(game, 9600, 200, 100, 50),
                Platform(game, 9800, 300, 200, 50),
                Platform(game, 10050, 450, 200, 50, 'slowing'),
                Platform(game, 10250, 450, 150, 50),
                Platform(game, 10500, 300, 100, 50),
                Platform(game, 10550, 370, 400, 20, 'spikey'),
                Platform(game, 10700, 200, 100, 50),
                Platform(game, 10900, 300, 100, 50),
                Platform(game, 11100, 400, 300, 50),
                Platform(game, 11400, 400, 300, 50, 'slowing'),
                Platform(game, 11800, 300, 100, 50),
                Platform(game, 12000, 300, 300, 50),
                Platform(game, 12400, 200, 100, 50), 
                Platform(game, 12600, 300, 100, 50),
                Platform(game, 12800, 400, 100, 50),
                Platform(game, 13000, 300, 150, 50),
                Platform(game, 13250, 400, 150, 50),
                Platform(game, 13500, 300, 100, 50),
                Platform(game, 13700, 400, 300, 50),
                Platform(game, 14100, 300, 1900, 50) # Finish platform

            ],
            "powerups" : [
                Powerup(game, 900, 300, 'damageboost'),
                Powerup(game, 1600, 250, 'shield'),
                Powerup(game, 3000, 450, 'doublejump'),
                Powerup(game, 3400, 150, 'damageboost'),
                Powerup(game, 4000, 300, 'shield'),
                Powerup(game, 6500, 250, 'shield'),
                Powerup(game, 7600, 250, 'damageboost'),
                Powerup(game, 9420, 250, 'shield'),
                Powerup(game, 10200, 400, 'damageboost'),
                Powerup(game, 10550, 250, 'shield'),
                Powerup(game, 13050, 250, 'damageboost'),
                Powerup(game, 14200, 250, 'damageboost')
            ],
        }
    elif name == "multiplayer" : 
        powerups = ['shield', 'damageboost', 'doublejump', 'health']
        p_idx = random.randint(0, 3)
        p_x = random.randint(100, 3300)
        p_y = random.randint(200, 450)

        return{
            "platforms" : [
                Platform(game, 300, 400, 150, 20, 'solid', image = AssetManager.platform_images["forest"]),
                Platform(game, 600, 300, 150, 20, 'solid', image = AssetManager.platform_images["forest"]),
                Platform(game, 750, 300, 250, 20, 'solid'), #Fragile platform
                Platform(game, 1050, 200, 100, 20, 'solid', image = AssetManager.platform_images["forest"]), # Bonus on this platform
                Platform(game, 1140, 560 - config.BASE_GROUND_HEIGHT, 50, 40, 'bouncy'), #Bouncy platform
                Platform(game, 1250, 300, 300, 20, 'solid', image = AssetManager.platform_images["forest"]),
                Platform(game, 1400, 600 - config.BASE_GROUND_HEIGHT, 350, 20, 'slowing', image = AssetManager.platform_images["slowing"] ), #Muddy platform
                Platform(game, 1630, 200, 100, 20, 'timed', image = AssetManager.platform_images["timed"]),
                Platform(game, 1700, 300, 100, 20, 'solid', image = AssetManager.platform_images["forest"]),
                Platform(game, 1800, 300, 250, 20, 'slowing',image = AssetManager.platform_images["slowing"]),
                Platform(game, 2250, 200, 100, 20, 'timed'),
                Platform(game, 2400, 300, 300, 20, 'solid', image = AssetManager.platform_images["forest"]),
                Platform(game, 2800, 200, 100, 20, 'timed', image = AssetManager.platform_images["timed"]),
                Platform(game, 3000, 100, 100, 20, 'timed', image = AssetManager.platform_images["timed"]),
                Platform(game, 3150, 250, 200, 100, 'solid', image = AssetManager.platform_images["forest"]), #Finish platform
                #Platform(self, 3050, 560 - config.BASE_GROUND_HEIGHT, 50, 40, 'bouncy')
                game.ground_rect
            ],
            "powerups" : []
            
        }

    else:
        raise ValueError(f"Unknown level : {name}")
