import socket
import threading
import json
import config
import traceback
from src.engine.player import Player
from src.engine.protocols import Protocol 
class Client :
    def __init__(self,game, nickname,character_type,request_type):
        self.host = '192.168.1.175'
        self.port = 7337
        self.status = {
            # Data sent periodically to update this player's state and position
            "id" : None,
            "x" : None,
            "y" : 0,
            "state" : None,
            "health": config.MAX_PLAYER_HEALTH,
            "direction" : None
        }
        self.info = {
            # Information required to create a new player
            "id" : None,
            "nickname" : nickname,
            "character_type" : character_type,
            "team" : None
        }
        self.request_type = request_type
        #self.players_count = 0
        self.team = None
        self.player = None
        self.game = game
        self.other_players = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buffer = ""
        self.is_connected = False
        
    def start (self):
        try:
            self.socket.connect((self.host,self.port))
            self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY,1)
            self.is_connected = True
        except KeyboardInterrupt :
            print ("keyboard interrupt")
            self.send(Protocol.Request.DISCONNECTED,self.info["id"])
            self.socket.close()
        except:
            print("connection error")
            return
        recieve_thread = threading.Thread(target=self.recieve)
        #update_thread = threading.Thread(target=self.update_status)
        recieve_thread.start()
        #update_thread.start()
        if not self.is_connected :
            print ("keyboard interrupt")
            self.send(Protocol.Request.DISCONNECTED,self.info["id"])
            self.socket.close()
   


    def recieve(self):
        while self.is_connected :  
            try : 
                chunck = self.socket.recv(1024).decode('utf-8')
                
                self.buffer += chunck
                while '\n' in self.buffer :
                    line,self.buffer = self.buffer.split('\n', 1)
                    line = json.loads(line)
                    
                    if line.get("type") == Protocol.Response.SETUP :
                        print("recieved1")
                        if line.get("data") == "Enter your nickname" :
                            print("recieved2")
                            self.send(Protocol.Request.NICKNAME,self.info["nickname"])
                        elif line.get("data") == "Choose character type":
                            self.send(Protocol.Request.CHAR_TYPE,self.info["character_type"])
                        elif line.get("data") == "Choose game mode" :
                            self.send(Protocol.Request.MATCHMAKING, self.request_type)
                    elif line.get("type") == Protocol.Response.ID:
                        self.info["id"] = line.get("data")
                        self.status["id"] = line.get("data")
                        self.player = Player(self.game, self.info["character_type"],100, self.info["id"],self.info["nickname"])
                        self.game.player = self.player
                    elif line.get("type") == Protocol.Response.TEAM:
                        self.info["team"] = line.get("data")
                        self.player.team = self.info["team"]
                    elif line.get("type") == Protocol.Response.START :
                        self.game.state = "playing"
                        print ("recieved start")
                    elif line.get("type") == Protocol.Response.UPDATE :
                        self.update_other_players (line.get("data"))
                    elif line.get("type") == Protocol.Response.OPPONENT :
                        self.add_other_players( line.get("data"))
                        print ("other player func")
                    elif line.get("type") == Protocol.Response.POWERUP_SPAWNED :
                        self.game.powerup_spawner(line.get("data"))
                    elif line.get("type") == Protocol.Response.POWERUP_PICKED :
                        self.game.powerup_killer(line.get("data"))
                    elif line.get("type") == Protocol.Response.OPPONENT_LEFT :
                        for player in self.other_players :
                            if isinstance(player, Player) :
                                if player.id == line.get("data") :
                                    print(player.id )
                                    print("left")
                                    self.other_players.remove(player)
                                    self.game.other_players = self.other_players
                                    self.game.state = "won"
            except KeyboardInterrupt :
                print ("keyboard interrupt")
                self.send(Protocol.Request.DISCONNECTED,self.info["id"])
                self.socket.close()
                break
            except Exception as e:
                print("closed",e)
                traceback.print_exc()
                self.is_connected = False
                self.send(Protocol.Request.DISCONNECTED,self.info["id"])
                self.socket.close()
                return
        if not self.is_connected :
            print ("keyboard interrupt")
            self.send(Protocol.Request.DISCONNECTED,self.info["id"])
            self.socket.close()

    def add_other_players (self, other_players_info):
        try:
            # Add new players to the client's player_list 
            for player_info in other_players_info:
                self.other_players.append(Player(self.game, player_info["character_type"],100, player_info["id"],player_info["nickname"], player_info["team"]))
            self.game.other_players = self.other_players
        except Exception as e:
            print("error2", e)
            traceback.print_exc()
    
    def update_other_players(self,data) :        
        
        # Update position and state of the player with the same id
        for player in self.other_players :
            if isinstance(player, Player) :
                if player.id == data["id"]:
                    player.sync_remote_player(data)

    def update_status (self) :
        if self.is_connected :
            try:
                if self.game.state == "playing" and self.player != None :
                    updated_status = {
                        "id" : self.info["id"],
                        "x" : self.player.rect.x,
                        "y" : self.player.rect.y,
                        "state" : self.player.state,
                        "health" : self.player.health,
                        "direction" : self.player.direction
                    }
                    
                    self.status = updated_status
                    self.send(Protocol.Request.MOVE, self.status)
            except KeyboardInterrupt :
                print ("keyboard interrupt")
                self.send(Protocol.Request.DISCONNECTED,self.info["id"])
                self.socket.close()
            except Exception as e:
                print("error3",e) 
                traceback.print_exc()
                self.is_connected =False
                self.socket.close()
        else:
            print ("keyboard interrupt")
            self.send(Protocol.Request.DISCONNECTED,self.info["id"])
            self.socket.close()
    def send (self, type, data):
        message = {
            "type" : type ,
            "data" : data
        }
        message = json.dumps(message) + "\n"
        self.socket.sendall(message.encode('utf-8'))

    