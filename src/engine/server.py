import socket, threading, json, time, random,traceback
from .room import Room
from .protocols import Protocol
from .platform import Platform
from threading import Lock

HOST = '0.0.0.0'
PORT = 55555

class Server:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()

        self.client_names = {}
        self.client_modes = {}
        self.client_characters = {}
        #self.client_ids = []
        self.client_ids = {}
        self.ids = {}
        self.id_lock = Lock()
        self.client_gamestyles = {}
        self.client_invites = {}
        self.waiting_clients = []
        self.rooms = {}
        self.teams = {}

    def start(self):
        print("server started.")
        self.start_powerup_spawner()
        try :
            while True :
                buffer = ""
                client, address = self.server.accept()
                client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY,1)
                client.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65536)
                client.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
                print(f"connected with {address}")
                thread = threading.Thread(target=self.handle, args=(client,buffer,))
                thread.start()
        except KeyboardInterrupt:
            print("Shutting down server")
            self.server.close()
    
    def handle(self, client,buffer):
        self.handle_connect(client)
        self.wait_for_room(client)
        connection = True
        while connection :
            try :
                
                data = client.recv(1024).decode("utf-8")
                if not data :
                    break
                buffer += data
                while '\n' in buffer and connection:
                    line,buffer = buffer.split('\n',1)
                    message = json.loads(line)
                    connection = self.handle_recieve(message, client)               
            except Exception as e:
                print("????",e)
                traceback.print_exc()
                break
        
        self.broadcast(Protocol.Response.OPPONENT_LEFT,self.client_ids[client] , client)
        self.disconnect(client)

    def handle_connect(self, client):
        print ("handle_connect")
        while client not in self.client_names:
            self.send(Protocol.Response.SETUP, "Enter your nickname", client )
            try :
                line = client.recv(1024).decode("utf-8")
                line = line.rstrip('\n')
                message = json.loads(line)
                if message.get("type") == Protocol.Request.NICKNAME:
                    nickname = message.get("data")
                    self.client_names[client] = nickname
                    print(message)
            except :
                continue
        print("nickname")
        while client not in self.client_characters :
            self.send(Protocol.Response.SETUP, "Choose character type", client)
            try :
                line = client.recv(1024).decode("utf-8")
                line = line.rstrip('\n')
                message = json.loads(line)
                if message.get("type") == Protocol.Request.CHAR_TYPE :
                    char_type = message.get("data")
                    self.client_characters[client] = char_type
                    print(message)
            except :
                continue
                    
        print("character")
        while client not in self.client_ids:
            id = self.id_generator(client)
            print(id)
            self.send(Protocol.Response.ID, id, client)
        print("id")
        while client not in self.client_modes:
            self.send(Protocol.Response.SETUP, "Choose game mode", client)
            try :
                line = client.recv(1024).decode("utf-8")
                line = line.rstrip('\n')
                message = json.loads(line)
                if message.get("type") == Protocol.Request.MATCHMAKING :
                    mode = message.get("data")
                    self.client_modes[client] = mode
            except:
                continue
        while client not in self.client_gamestyles :
            self.send(Protocol.Response.GAME_STYLE, "Choose game style", client)
            try :
                line = client.recv(1024).decode("utf-8")
                line = line.rstrip('\n')
                message = json.loads(line)
                if message.get("type") == Protocol.Request.LOCAL_GAME :
                    self.client_gamestyles[client] = "local_game"
                    self.waiting_clients.append((client, self.client_modes[client]))
                    self.match_players()
                elif message.get("type") == Protocol.Request.INVITE_GAME :
                    self.client_gamestyles[client] = "invite_game"
                    line = client.recv(1024).decode("utf-8")
                    line = line.rstrip('\n')
                    message = json.loads(line)
                    if message.get("type") == Protocol.Request.SEND_INVITE :
                        invitation = {
                            "sender_id" : self.client_ids[client],
                            "request_type" : self.client_modes[client],
                            "nickname" : self.client_names[client]
                        }
                        reciever_id = message.get("data")
                        self.send(Protocol.Response.SEARCH_RESAULT, self.id_found(reciever_id), client)
                        if self.id_found(reciever_id) :
                            self.client_invites[client] = self.ids[message.get("data")]
                            self.send(Protocol.Response.SEND_INVITE, invitation, self.ids[reciever_id])
                    elif message.get("type") == Protocol.Request.ACCEPT_INVITE :
                        data = message.get("data")
                        mode = data.get("request_type")
                        id = data.get("sender_id")
                        self.client_modes[client] = mode
                        clients = [self.ids[id], client]
                        self.create_room(clients)
            except Exception as e:
                print("error setting the game style",e)
                traceback.print_exc()
        print("user defined")
 
    def id_generator(self, client):
        with self.id_lock : # Guarantees unique IDs
            while True :
                id = random.randint(10000, 99999)
                if id not in self.client_ids.values():
                    self.client_ids [ client ] = id
                    self.ids[id] = client
                    return id

    def id_found(self, reciever_id):
        for client_id in self.ids :
            if client_id == reciever_id:
                return True
        return False
            

    def start_powerup_spawner(self):
        def spawner_loop():
            while True : 
                time.sleep(3)
                for room in set(self.rooms.values()):
                    powerup_data = room.spawn_random_powerup()
                    if powerup_data :
                        room.pending_powerups.append(powerup_data)
                        #self.broadcast(Protocol.Response.POWERUP_SPAWNED, powerup_data, sender=None)
                        for client in room.clients:
                            self.send(Protocol.Response.POWERUP_SPAWNED, powerup_data, client)
        thread = threading.Thread(target= spawner_loop, daemon=True)
        thread.start()

    def match_players(self):
        modes = {"1v1" : [], "2v2" : []}
        for client, mode in self.waiting_clients:
            modes[mode].append(client)
        for mode, queue in modes.items():
            if mode == "1v1" and len(queue) >= 2 :
                print("matched")
                self.create_room(queue[:2])
                remaining_clients = []
                for pair in self.waiting_clients :
                    if pair[0] not in queue[:2] :
                        remaining_clients.append(pair)
                self.waiting_clients = remaining_clients
    
            elif mode == "2v2" and len(queue) >= 4:
                self.create_room(queue[:4])
                remaining_clients = []
                for pair in self.waiting_clients :
                    if pair[0] not in queue[:4] :
                        remaining_clients.append(pair)
                self.waiting_clients = remaining_clients
    
    def create_room(self, clients):
        print("creato room func")
        team_ids = [1,2] * (len(clients)//2)
        teams = dict(zip(clients, team_ids))
        room = Room(clients, teams)
        for client in clients :
            self.rooms[client] = room
            self.teams[client] = teams[client]
        for client in clients :
            self.send(Protocol.Response.TEAM, teams[client], client)
            print(f"sent protocol team {self.teams[client]}")
            #opponents = [self.client_names[c] for c in clients if c != client]
            opponents = []
            for c in clients :
                if c != client :
                    try :
                        opponent_info = {
                            "id" : self.client_ids[c],
                            "nickname" : self.client_names[c],
                            "character_type" : self.client_characters[c],
                            "team" : self.teams[c]
                        }
                        print(f"opponent info {opponent_info}")
                        opponents.append(opponent_info)
                    except Exception as e:
                        print(f"[ERROR getting opponent info]: {e}")
                        traceback.print_exc()
            self.send(Protocol.Response.OPPONENT, opponents, client)
            self.send(Protocol.Response.START, "", client)
        print("room created and start protocol sent")

    def wait_for_room(self, client):
        while client not in self.rooms :
            print("waiting for room")
            time.sleep(1)

    def handle_recieve(self, message, client):
        r_type = message.get("type")
        data = message.get("data")
        room = self.rooms.get(client)
        if room :
            if r_type == Protocol.Request.DISCONNECTED :
                print(self.client_ids[client])
                print( "left")
                return False
                
            elif r_type == Protocol.Request.MOVE:
                room.update_player_state(client, data)
                self.broadcast(Protocol.Response.UPDATE, data, client)
            elif r_type == Protocol.Request.POWERUP :
                if data in room.pending_powerups:
                    room.register_powerup(data)
                    room.pending_powerups.remove(data)
                    self.broadcast(Protocol.Response.POWERUP_PICKED, data, client)

            '''if room.is_finished():
                loser = room.losing_team
                winner = [t for t in room.team_health if t != loser][0]
                #print("[SERVER] Match ended. Sending WINNER/LOSER...")

                for c in room.clients :
                    if self.teams[c] == winner :
                        self.send(Protocol.Response.WINNER, None, c)
                    else :
                        self.send(Protocol.Response.LOSER, None, c)'''
            if r_type == Protocol.Request.NEW_LOOK :
                print("New look")
                self.teams.pop(client, None)
                self.client_names.pop(client, None)
                self.client_modes.pop(client, None)
                self.client_characters.pop(client,None)
                self.client_gamestyles.pop(client,None)
                self.client_invites.pop(client,None)
                self.handle_connect(client) 
        return True

    def send(self, r_type, data, client):
        try :
            messege = {"type" : r_type, "data" : data}
            client.send((json.dumps(messege) + "\n").encode("utf-8"))
        except Exception as e:
            print(f"[SEND ERROR]: {e}")

    def broadcast(self, r_type, data, sender):
        room = self.rooms.get(sender)
        if room :
            for client in room.clients :
                if client != sender:
                    self.send(r_type, data, client)
    
    def disconnect(self, client):
        room = self.rooms.get(client)
        if room :
            room.clients.remove(client)
            del self.rooms[client]
        self.teams.pop(client, None)
        self.client_names.pop(client, None)
        self.client_modes.pop(client, None)
        self.client_ids.pop(client, None)
        self.client_characters.pop(client,None)
        try :
            client.close()
        except : 
            pass
        

if __name__ == "__main__":
    Server().start()