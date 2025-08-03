class Protocol :
    class Request : # things the server requests from the client
        NICKNAME = "request.nickname"
        MATCHMAKING = "request.matchmaking" 
        CHAR_TYPE = 'request.character_type'
        DISCONNECTED = 'request.disconnected'
        MOVE = "request.move"
        SHOOT = "request.shoot"
        HIT = "request.hit"
        POWERUP = "request.powerup"
        KILL_POWERUP = "request.kill_powerup"
        LEAVE = "request.leave"
    class Response :
        SETUP = "response.setup"
        ID = "response.id"
        OPPONENT = "response.opponent"
        PLAYER_LIST = "response.player_list"
        TEAM = "response.team"
        START = "response.start"
        UPDATE = "response.update"
        POWERUP_SPAWNED = "response.powerup_spawned"
        POWERUP_PICKED = "response.powerup_picked"
        OPPONENT_LEFT = "response.opponent_left"
        WINNER = "response.winner"
        LOSER = "response.loser"




