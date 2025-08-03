class Protocol :
    class Request : # things the server requests from the client
        NICKNAME = "request.nickname"
        MATCHMAKING = "request.matchmaking" 
        CHAR_TYPE = 'request.character_type'
        LOCAL_GAME = "request.local_game"
        INVITE_GAME = "request.invite_game"
        SEND_INVITE = 'request.send_invite'
        ACCEPT_INVITE = 'request.accept_invite'
        DISCONNECTED = 'request.disconnected'
        MOVE = "request.move"
        SHOOT = "request.shoot"
        HIT = "request.hit"
        POWERUP = "request.powerup"
        KILL_POWERUP = "request.kill_powerup"
        LEAVE = "request.leave"
    class Response :
        SETUP = "response.setup"
        GAME_STYLE = "response.game_style"
        ID = "response.id"
        SEND_INVITE = "response.send_invite"
        INVITE_ACCEPTED = "response.invite_accepted"
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




