import socket
import threading
import json

from src.engine.player import Player

class Client :
    def __init__(self, host, port, id, nickname,character_type,request_type,player, team = None):
        self.host = host
        self.port = port
        self.status = {
            # Data sent periodically to update this player's state and position
            "id" : id,
            "x" : None,
            "y" : None,
            "state" : "idle",
            "health": None,
            "direction" : None
        }
        self.info = {
            # Information required to create a new player
            "id" : id,
            "nickname" : nickname,
            "character_type" : character_type
        }
        self.request_type = request_type
        self.players_count = 0
        self.team = team
        self.player = player
        self.all_players = {}
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def start (self):
        self.socket.connect((self.host,self.port))
        receive_thread = threading.Thread(target=self.recieve)
        update_thread = threading.Thread(target=self.update_status)
        receive_thread.start()
        update_thread.start()

    def recieve(self):
        buffer = ""
        while True :
            buffer = ""
            try : 
                chunck = self.socket.recv(1024).decode('utf-8')
                if not chunck :
                    #disconnected
                    self.socket.close()
                    break
                buffer += chunck
                while '\n' in buffer :
                    line,buffer = buffer.split('\n', 1)
                    if line == "NICK":
                        self.socket.send(self.status["nickname"].encode['utf-8'])
                    else :
                        new_data = json.loads(line) 
                        self.handle_new_data (new_data)
            except:
                self.socket.close()
                break
    def handle_new_data (self, new_data):
        if new_data["type"] == "player_list":
            # Add new players to the client's player_list 
            new_players_count = len(new_data["player_list"])
            for i in range(self.players_count, new_players_count):
                if new_data["player_list"][i] ["id"]== self.info["id"] :
                    self.all_players[i] = self.player
                else :
                    new_player_info = new_data["player_list"][i]
                    #self.all_players[i] = Player(self.game, start_x, new_player_info["id"], new_player_info["nickname"], new_player_info["character_type"])
            self.players_count = new_players_count -1
        elif new_data["type"] == "players_update" :
            # Update position and state of the player with the same id
            for player in self.all_players :
                if isinstance(player, Player) :
                    if player.id == new_data["updated_status"]["id"] :
                        player.sync_remote_player(new_data["updated_status"])

    def update_status (self) :
        updated_status = {
            "id" : self.info["id"],
            "x" : self.player.x,
            "y" : self.player.y,
            "state" : self.player.state,
            "health" : self.player.health,
            "direction" : self.player.direction
        }
        
        self.status = updated_status
        self.send_status()
    def send_status (self):
        data = {
            "type" : "players_update",
            "updated_status" : self.status
        }
        message = json.dumps(data) + "\n"
        self.socket.sendall(message.encode('utf-8'))

    