class Room:
    def __init__(self, clients, teams):
        self.clients = clients
        self.teams = teams
        self.clients_states = {client : {} for client in self.clients}
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

        

