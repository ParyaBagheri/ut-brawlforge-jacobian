class Protocol :
    class Request : # things the server requests from the client
        NICKNAME = "request.niskname"
        MATCHMAKING = "request.matchmaking" 
        MOVE = "request.move"
        SHOOT = "request.shoot"
        HIT = "request.hit"
        POWERUP = "request.powerup"
        LEAVE = "request.leave"
    class Response :
        SETUP = "response.setup"
        OPPONENT = "response.opponent"
        START = "response.start"
        UPDATE = "response.update"
        POWERUP_PICKED = "response.powerup_picked"
        OPPONENT_LEFT = "response.opponent_left"
        WINNER = "response.winner"
        LOSER = "response.loser"




