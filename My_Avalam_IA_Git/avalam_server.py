
from easyAI import AI_Player, Negamax
from easyAI import TwoPlayersGame
from easyAI.Player import Human_Player
from avalam_ai import AvalamAI
import cherrypy
import sys
import json

#Fonction qui permet de determiner quels sont les pions de l'ia.
#Renvoie 0 ou 1
def check_player(players, you):
    if players[0] == you: return 0
    else: return 1

#Fonction qui compte le nombre de moves possibles en fonction de l'état du jeu.
#Retourne un entier >= 0
def count_moves(game):
    count_moves = 0
    for i in range(0,9):
        for j in range(0,9):                
            if game[i][j]:
                for k in range(-1,2):
                    for l in range(-1,2):
                        if not(k==0 and l==0)and i+k>=0 and i+k<=8 and j+l>=0 and j+l<=8 and(len(game[i][j])+len(game[i+k][j+l])<=5)and(game[i+k][j+l]):
                            count_moves += 1
    return count_moves

#Fonction qui détermine la profondeur de l'arbre de recherche en fonction du nombres de moves possibles.
#Retourne un entier compris entre 2 et 6
def depth(count_moves):
    if count_moves < 8:
        return 6
    elif count_moves < 15:
        return 5
    elif count_moves < 30:
        return 4       
    elif count_moves < 50:
        return 3
    else:
        return 2

class Server:
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    #Route move
    def move(self):
        # Deal with CORS
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        cherrypy.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        cherrypy.response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        if cherrypy.request.method == "OPTIONS":
            return ''
        
        #Récupération des données du jeu
        body = cherrypy.request.json
        game = body['game']
        players = body['players']
        you = body ['you']
        pion = check_player(players, you)

        #Démarage de l'algorithme de recherche du meilleur move
        ai_algo = Negamax(depth(count_moves(game)))
        a = AvalamAI( [AI_Player(ai_algo),Human_Player()],game,pion)
        move = a.player.ask_move(a)
        json_move = {
	        "move": {
		        "from": move[0],
		        "to": move[1]
	        },
	        "message": "What do you say about that?!"
        }
        return json_move

    @cherrypy.expose
    #Route ping
    def ping(self):
        return "pong"


if __name__ == "__main__":
    if len(sys.argv) > 1:
        port=int(sys.argv[1])
    else:
        port=8081

    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': port})
    cherrypy.quickstart(Server())

