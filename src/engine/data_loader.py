import pygame , random
from src.engine.platform import Platform
from src.engine.collectible import Powerup
from src.engine.assetmanager import AssetManager
import config


def get_level_data(name, game):
    if name == "forest":
        
        return{
            "map" : AssetManager.map_image["forest"] ,
            "background_layers" : {AssetManager.backgrounds["forest"]},
            "platforms" : [
                Platform(game, 304, 384, 160, 24, 'solid' ),
                Platform(game, 600, 304, 192, 40, 'solid'),
                Platform(game, 750, 304, 250, 20, 'timed', image = AssetManager.platform_images["timed"]), #Fragile platform
                Platform(game, 1048, 200, 112, 16, 'solid'), # Bonus on this platform
                Platform(game, 1140, 560 - config.BASE_GROUND_HEIGHT, 50, 40, 'bouncy',AssetManager.platform_images["bouncy"][0]), #Bouncy platform
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
                Platform(game, 3050, 560 - config.BASE_GROUND_HEIGHT, 50, 40, 'bouncy', AssetManager.platform_images["bouncy"][0])
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
            "background_layers" : {
                AssetManager.backgrounds["desert"]
                },
            
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
                Platform(game, 4025, 440, 50, 40, 'bouncy',AssetManager.platform_images["bouncy"][0]),
                Platform(game, 4104, 496, 736, 24, 'spikey'),
                Platform(game, 4176, 296, 208, 32),
                Platform(game, 4496, 400, 152, 24),
                Platform(game, 4696, 296, 152, 24),
                Platform(game, 4848, 400, 544, 192),
                Platform(game, 5400, 296, 240, 296),
                Platform(game, 5648, 200, 344, 400) 
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
            "map" : AssetManager.map_image["lost_city"] ,
            "background_layers" : {AssetManager.backgrounds["lost_city"]},
            "platforms" : [
                Platform(game, 0, 296, 496, 296),
                Platform(game, 600, 400, 152, 200),
                Platform(game, 848, 296, 96, 296),
                Platform(game, 1048, 248, 248, 352),
                Platform(game, 1352, 152, 152, 24),
                Platform(game, 1352, 352, 200, 248),
                Platform(game, 1600, 248, 296, 32),
                Platform(game, 2000, 352, 400, 248),
                Platform(game, 2496, 248, 96, 352),
                Platform(game, 2648, 200, 96, 32),
                Platform(game, 2800, 96, 96, 32),
                Platform(game, 2900, 220, 152, 32, 'timed', image = AssetManager.platform_images["timed"]),
                Platform(game, 3096, 296, 152, 296),
                Platform(game, 3352, 248, 152, 352),
                Platform(game, 3600, 352, 400, 248),
                #Platform(game, 3600, 352, 200, 24, image = AssetManager.platform_images["lostcity"]),
                Platform(game, 4096, 296, 96, 32),
                Platform(game, 4250, 200, 100, 30, 'timed', image = AssetManager.platform_images["timed"]),
                Platform(game, 4400, 296, 96, 32),
                Platform(game, 4600, 400, 96, 32),
                Platform(game, 4800, 496, 96, 32, 'slowing', image = AssetManager.platform_images["slowing"]),
                Platform(game, 5000, 400, 150, 30, 'timed', image = AssetManager.platform_images["timed"]),
                Platform(game, 5248, 352, 96, 248),
                Platform(game, 5400, 400, 96, 32),
                Platform(game, 5600, 400, 96, 32),
                Platform(game, 5800, 400, 96, 32),
                Platform(game, 5952, 392, 248, 208),
                Platform(game, 6300, 300, 100, 30, 'timed' , image = AssetManager.platform_images["timed"]), 
                Platform(game, 6496, 352, 96, 248),
                Platform(game, 6696, 296, 96, 32),
                Platform(game, 6896, 200, 96, 32),
                Platform(game, 7096, 96, 904, 24) #Finish line at 7700
                
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
            "map" : AssetManager.map_image["underwater"] ,
            "background_layers" : {AssetManager.backgrounds["underwater"]},
            "platforms" : [
                Platform(game, 0, 296, 296, 96),
                Platform(game, 448, 400, 296, 96),
                Platform(game, 760, 352, 248, 152),
                Platform(game, 1096, 328, 296, 48),
                Platform(game, 1496, 296, 152, 48),
                Platform(game, 1752, 200, 248, 48),
                Platform(game, 1656, 400, 424, 24, 'spikey'),
                Platform(game, 2096, 296, 296, 48),
                Platform(game, 2496, 400, 296, 48),
                Platform(game, 2896, 296, 296, 40),
                Platform(game, 2896, 496, 1000, 40),
                Platform(game, 3296, 200, 400, 40),
                Platform(game, 3800, 352, 296, 48),
                Platform(game, 4096, 424, 296, 24, 'spikey'), 
                Platform(game, 4248, 248, 448, 48),
                Platform(game, 4800, 200, 400, 48),
                Platform(game, 5296, 296, 400, 48), 
                Platform(game, 5800, 200, 96, 48), 
                Platform(game, 5696, 360, 96, 24, 'spikey'),
                Platform(game, 6000, 296, 96, 48),
                Platform(game, 6200, 400, 96, 48),
                Platform(game, 6400, 296, 400, 48),
                Platform(game, 6952, 296, 96, 48),
                Platform(game, 7200, 296, 152, 48),
                Platform(game, 7496, 296, 200, 48),
                Platform(game, 7800, 200, 400, 48),
                Platform(game, 8296, 296, 200, 48), 
                Platform(game, 8448, 368, 200, 24, 'spikey'),
                Platform(game, 8600, 296, 400, 48),
                Platform(game, 9104, 400, 152, 48), 
                Platform(game, 9352, 296, 152, 48),
                Platform(game, 9600, 200, 96, 48),
                Platform(game, 9800, 296, 200, 48),
                Platform(game, 10048, 448, 200, 48, 'slowing'),
                Platform(game, 10248, 448, 152, 48),
                Platform(game, 10504, 296, 96, 48),
                Platform(game, 10552, 368, 400, 24, 'spikey'),
                Platform(game, 10704, 200, 96, 48),
                Platform(game, 10904, 296, 96, 48),
                Platform(game, 11104, 400, 296, 48),
                Platform(game, 11400, 400, 296, 48, 'slowing'),
                Platform(game, 11800, 296, 96, 48),
                Platform(game, 12000, 296, 296, 48),
                Platform(game, 12400, 200, 96, 48), 
                Platform(game, 12600, 296, 96, 48),
                Platform(game, 12800, 400, 96, 48),
                Platform(game, 13000, 296, 152, 48),
                Platform(game, 13248, 400, 152, 48),
                Platform(game, 13496, 296, 96, 48),
                Platform(game, 13696, 400, 296, 48),
                Platform(game, 14104, 296, 1900, 48) # Finish platform

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
            "map" : AssetManager.map_image["forest"] ,
            "background_layers" :{ AssetManager.backgrounds["forest"]},
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
            "powerups" : []
            
        }

    else:
        raise ValueError(f"Unknown level : {name}")
