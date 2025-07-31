import socket, threading, json, time, random
from .room import Room
from .protocols import Protocol
from .platform import Platform
from threading import Lock

HOST = '192.168.1.38'
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
        self.id_lock = Lock()

        self.waiting_clients = []
        self.rooms = {}
        self.teams = {}

    def start(self):
        print("server started.")
        self.start_powerup_spawner()
        try :
            while True :
                client, address = self.server.accept()
                print(f"connected with {address}")
                thread = threading.Thread(target=self.handle, args=(client,))
                thread.start()
        except KeyboardInterrupt:
            print("Shutting down server")
            self.server.close()
    
    def handle(self, client):
        self.handle_connect(client)
        self.wait_for_room(client)

        while True :
            try :
                data = client.recv(1024).decode("utf-8")
                if not data :
                    break
                message = json.loads(data)
                self.handle_recieve(message, client)
            except :
                break
        
        self.broadcast(Protocol.Response.OPPONENT_LEFT, None, client)
        self.disconnect(client)

    def handle_connect(self, client):
        while client not in self.client_names:
            self.send(Protocol.Response.SETUP, "Enter your nickname", client )
            try :
                message = json.loads(client.recv(1024).decode("utf-8"))
                if message.get("type") == Protocol.Request.NICKNAME:
                    nickname = message.get("data")
                    self.client_names[client] = nickname
            except :
                continue
        print("nickname")
        while client not in self.client_characters :
            self.send(Protocol.Response.SETUP, "Choose character type", client)
            try :
                message = json.loads(client.recv(1024).decode("utf-8"))
                if message.get("type") == Protocol.Request.CHAR_TYPE :
                    char_type = message.get("data")
                    self.client_characters[client] = char_type
            except :
                continue
                    
        print("character")
        while client not in self.client_ids:
            id = self.id_generator(client)
            self.send(Protocol.Response.ID, id, client)
        print("id")
        while client not in self.client_modes:
            self.send(Protocol.Response.SETUP, "Choose game mode", client)
            try :
                message = json.loads(client.recv(1024).decode("utf-8"))
                if message.get("type") == Protocol.Request.MATCHMAKING :
                    mode = message.get("data")
                    self.client_modes[client] = mode
                    self.waiting_clients.append((client, mode))
                    self.match_players()
            except:
                continue
        print("user defined")
    
    def id_generator(self, client):
        with self.id_lock : # Guarantees unique IDs
            while True :
                id = random.randint(10000, 99999)
                if id not in self.client_ids.values():
                    self.client_ids [ client ] = id
                    return id

    def start_powerup_spawner(self):
        def spawner_loop():
            while True : 
                time.sleep(1)
                for room in set(self.rooms.values()):
                    powerup_data = room.spawn_random_powerup()
                    if powerup_data :
                        room.pending_powerups.append(powerup_data)
                        self.broadcast(Protocol.Response.POWERUP_SPAWNED, powerup_data, sender=None)
        thread = threading.Thread(target= spawner_loop, daemon=True)
        thread.start()

    def match_players(self):
        modes = {"1v1" : [], "2v2" : []}
        for client, mode in self.waiting_clients:
            modes[mode].append(client)
        for mode, queue in modes.items():
            if mode == "1v1" and len(queue) >= 2 :
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
        team_ids = [1,2] * (len(clients)//2)
        teams = dict(zip(clients, team_ids))
        room = Room(clients, teams)
        for client in clients :
            self.rooms[client] = room
            self.teams[client] = teams[client]
            #opponents = [self.client_names[c] for c in clients if c != client]
            opponents = []
            for c in clients :
                if c != client :
                    opponent_info = {
                        "id" : self.client_ids[c],
                        "nickname" : self.client_names[c],
                        "character_type" : self.client_characters[c]
                    }
                opponents.append(opponent_info)
            self.send(Protocol.Response.OPPONENT, opponents, client)
            self.send(Protocol.Response.START, None, client)
        print("room created")

    def wait_for_room(self, client):
        while client not in self.rooms :
            time.sleep(3)

    def handle_recieve(self, message, client):
        r_type = message.get("type")
        data = message.get("data")
        room = self.rooms.get(client)
        if room :
            if r_type == Protocol.Request.MOVE:
                room.update_player_states(client, data)
                self.broadcast(Protocol.Response.UPDATE, {"client" : self.client_names[client], "data": data}, client)
            elif r_type == Protocol.Request.POWERUP :
                if data in room.pending_powerups:
                    room.register_powerup(data)
                    room.pending_powerups.remove(data)
                    self.broadcast(Protocol.Response.POWERUP_PICKED, data, client)

            if room.is_finished():
                loser = room.losing_team
                winner = [t for t in room.team_health if t != loser][0]

                for c in room.clients :
                    if self.teams[c] == winner :
                        self.send(Protocol.Response.WINNER, None, c)
                    else :
                        self.send(Protocol.Response.LOSER, None, c)

    def send(self, r_type, data, client):
        try :
            messege = {"type" : r_type, "data" : data}
            client.send((json.dumps(messege) + "\n").encode("utf-8"))
        except :
            pass

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
        try :
            client.close()
        except : 
            pass
        

if __name__ == "__main__":
    Server().start()