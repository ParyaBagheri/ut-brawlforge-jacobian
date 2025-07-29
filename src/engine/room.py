import random
from src.engine.platform import Platform
from src.engine.assetmanager import AssetManager
import config
platforms = [
    Platform(0, 600 - config.BASE_GROUND_HEIGHT, 3200, config.BASE_GROUND_HEIGHT, 'solid')
    Platform(304, 384, 160, 24, 'solid' ),
    Platform(600, 304, 192, 40, 'solid'),
    Platform(750, 304, 250, 20, 'timed'), #Fragile platform
    Platform(1048, 200, 112, 16, 'solid'), # Bonus on this platform
    Platform(1140, 560 - config.BASE_GROUND_HEIGHT, 50, 40, 'bouncy'), #Bouncy platform
    Platform(1248, 296, 304, 24, 'solid'),
    Platform(1416, 600 - config.BASE_GROUND_HEIGHT, 350, 20, 'slowing' ), #Muddy platform
    Platform(1630, 200, 100, 20, 'timed'),
    Platform(1696, 296, 112, 48, 'solid'),
    Platform(1808, 296, 248, 48, 'slowing'),
    Platform(2250, 200, 100, 20, 'timed'),
    Platform(2400, 296, 304, 24, 'solid'),
    Platform(2800, 200, 100, 20, 'timed'),
    Platform(3000, 100, 100, 20, 'timed'),
    Platform(3112, 248, 88, 72, 'solid'), #Finish platform
    Platform(3050, 560 - config.BASE_GROUND_HEIGHT, 50, 40, 'bouncy')
]
class Room:
    def __init__(self, clients, teams):
        self.clients = clients
        self.teams = teams
        self.clients_states = {client : {} for client in self.clients}
        self.pending_powerups = []
        self.collected_powerups = []
        self.finished = False
    def update_player_state(self, client, data): # Have a function in server to send this data to room
        self.clients_states[client] = data

    def get_player_state(self, client):
        return self.clients_states.get(client, {})
    
    def get_opponents(self, client):
        my_team = self.teams[client]
        return [c for c in self.clients if self.teams[c] != my_team]
    
    def get_opponents_states(self, client):
        return [self.clients_states.get(c, {}) for c in self.get_opponents(client)]
    
    def get_teammate(self, client):
        my_team = self.teams[client]
        return [c for c in self.clients if c != client and self.teams[c] == my_team]
    
    def get_teammate_states(self, client):
        return [self.clients_states.get(c, {}) for c in self.get_teammate(client)]
    
    def spawn_random_powerup(self):
        powerup_types = ['shield', 'doublejump', 'damageboost', 'health']
        p_type = random.choice(powerup_types)

        valid_platforms = [p for p in platforms if isinstance(p, Platform) and p.visible]
        if not valid_platforms:
            return

        platform = random.choice(valid_platforms)
        x = platform.rect.centerx
        y = platform.rect.top - 50
        return {
            "type": p_type, 
            "x" : x, 
            "y": y
        }
    
    def register_powerup(self, data):
        if data not in self.collected_powerups :
            self.collected_powerups.append(data)
            return True
        return False

    def is_finished(self):
        self.team_health = {}
        for client, client_state in self.clients_states.items():
            team = self.teams[client]
            health = client_state.get("health", 1)
            if team not in self.team_health:
                self.team_health[team] = 0
            self.team_health[team] += max(0, health)

        for team, health in self.team_health.items():
            if health == 0 :
                self.losing_team = team
                return True
        return False

        

