import socket
import threading
import json

from src.engine.player import Player
from src.engine.protocols import Protocol 
class Client :
    def __init__(self,game, nickname,character_type,request_type):
        self.host = '192.168.1.38'
        self.port = 55555
        self.status = {
            # Data sent periodically to update this player's state and position
            "id" : None,
            "x" : None,
            "y" : None,
            "state" : None,
            "health": None,
            "direction" : None
        }
        self.info = {
            # Information required to create a new player
            "id" : None,
            "nickname" : nickname,
            "character_type" : character_type
        }
        self.request_type = request_type
        #self.players_count = 0
        self.team = None
        self.player = None
        self.game = game
        self.other_players = {}
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
                    line = json.loads(line)
                    
                    if line.get("type") == Protocol.Response.SETUP :
                        if line.get("data") == "Enter your nickname" :
                            self.send(Protocol.Request.NICKNAME,self.info["nickname"].encode['utf-8'])
                        elif line.get("type") == "Choose character type":
                            self.send(Protocol.Request.CHAR_TYPE,self.info["character_type"].encode['utf-8'])
                        elif line.get("data") == "Choose game mode" :
                            self.send(Protocol.Request.MATCHMAKING, self.request_type.encode['utf-8'])
                    elif line.get("type") == Protocol.Response.ID:
                        self.info["id"] = line.get("data")
                        self.status["id"] = line.get("data")
                        self.player = Player(self.game, self.info["character_type"], self.info["id"],self.info["nickname"])
                    elif line.get("type") == Protocol.Response.START :
                        self.game.state = "playing"
                    elif line.get("type") == Protocol.Response.UPDATE :
                        self.update_other_players (line.get("data"))
                    elif line.get("type") == Protocol.Response.OPPONENT :
                        self.other_players = line.get("data")
                    elif line.get("type") == Protocol.Response.POWERUP_SPAWNED :
                        self.game.level.powerups = line.get("data")

            except:
                self.socket.close()
                break

    '''def add_new_player (self, other_players_info):
        
        # Add new players to the client's player_list 
        new_players_count = len(other_players_info)
        for i in range(self.players_count, new_players_count):
            if other_players_info[i] ["id"]== self.info["id"] :
                self.other_players[i] = self.player
            else :
                new_player_info = other_players_info[i]
                self.other_players[i] = Player(self.game, new_player_info["character_type"], new_player_info["id"],new_player_info["nickname"])
        self.players_count = new_players_count -1'''
    
    def update_other_players(self,data) :        
        
        # Update position and state of the player with the same id
        for player in self.other_players :
            if isinstance(player, Player) :
                if player.id == data["id"] :
                    player.sync_remote_player(data)

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
        self.send(Protocol.Request.MOVE, self.status) 
    def send (self, type, data):
        message = {
            "type" : type ,
            "data" : data
        }
        message = json.dumps(message) + "\n"
        self.socket.sendall(message.encode('utf-8'))

    