from easyAI import TwoPlayersGame
from easyAI.Player import Human_Player


class AvalamAI( TwoPlayersGame ):

    def __init__(self, players, game, pion):
        self.players = players
        self.board = game
        self.nplayer = 1
        self.pion = pion
    
    def possible_moves(self):
        moves = []
        for i in range(0,9):
            for j in range(0,9):
                if self.board[i][j]:
                    for k in range(-1,2):
                        for l in range(-1,2):
                            if not(k==0 and l==0)and i+k>=0 and i+k<=8 and j+l>=0 and j+l<=8 and(len(self.board[i][j])+len(self.board[i+k][j+l])<=5)and(self.board[i+k][j+l]):
                                moves.append([[i,j],[i+k,j+l]])
        return moves
    
    def make_move(self, move):
        for i in range (0,len(self.board[move[0][0]][move[0][1]])):
            self.board[move[1][0]][move[1][1]].append(self.board[move[0][0]][move[0][1]][i])
        self.board[move[0][0]][move[0][1]]=[]

    def count_tour(self):
        tour_top_zero = 0
        tour_top_un = 0
        for i in range(0,9):
            for j in range(0,9):
                if self.board[i][j]:
                    if self.board[i][j][-1]==0:
                        tour_top_zero += 1   
                    else:
                        tour_top_un += 1 
        return (tour_top_zero, tour_top_un)
    
    def count_tour_full(self):
        tour_full_zero = 0
        tour_full_un = 0
        for i in range(0,9):
            for j in range(0,9):
                if self.board[i][j]:
                    if (self.board[i][j][-1]==0) and len(self.board[i][j])==5:
                        tour_full_zero += 1   
                    else:
                        tour_full_un += 1 
        return (tour_full_zero, tour_full_un)

    def count_tour_lonely(self):
        tour_lonely_zero = 0
        tour_lonely_un = 0
        for i in range(0,9):
            for j in range(0,9):
                if self.board[i][j]:
                    surrounding_zero = 0
                    surrounding_un = 0
                    for k in range(-1,2):
                        for l in range(-1,2):
                            if not(k==0 and l==0)and i+k>=0 and i+k<=8 and j+l>=0 and j+l<=8 and(self.board[i+k][j+l]):
                                if (self.board[i+k][j+l][-1]==0):
                                    surrounding_zero += 1   
                                else:
                                    surrounding_un += 1 
                    if self.board[i][j][-1]==0 and surrounding_un == 0: tour_lonely_zero += 1
                    if self.board[i][j][-1]==1 and surrounding_zero == 0: tour_lonely_un += 1
        return (tour_lonely_zero, tour_lonely_un)

    def lose(self, tour_top_zero, tour_top_un):
        if self.pion == 0:
            return tour_top_un > tour_top_zero
        else:
            return tour_top_zero > tour_top_un

    def win(self, tour_top_zero, tour_top_un):
        if self.pion == 0:
            return tour_top_un < tour_top_zero
        else:
            return tour_top_zero < tour_top_un

    def score_tour(self, tour_top_zero, tour_top_un):
        if self.pion == 0:
            return tour_top_zero - tour_top_un
        else:
            return tour_top_un - tour_top_zero 

    def score_tour_full(self, tour_full_zero, tour_full_un):
        if self.pion == 0:
            return tour_full_zero
        else:
            return tour_full_un

    def score_tour_lonely(self, tour_lonely_zero, tour_lonely_un):
        if self.pion == 0:
            return tour_lonely_un
        else:
            return tour_lonely_zero

    def is_over(self):
        for i in range(0,9):
            for j in range(0,9):
                if self.board[i][j]:
                    for k in range(-1,2):
                        for l in range(-1,2):
                            if not(k==0 and l==0)and i+k>=0 and i+k<=8 and j+l>=0 and j+l<=8 and(self.board[i+k][j+l]):
                                if (len(self.board[i][j])+len(self.board[i+k][j+l])<=5):
                                    return False
        return True
        
    def show(self):
        s = "[" 
        for i in range(0,9):
            s+= "["
            for j in range(0,9):
                s+= "["
                for k in range(0,len(game[i][j])):
                    s += str(game[i][j][k])
                s+= "]"
            s+= "] \n"
        s += "]"
        print(s)
                 
    def scoring(self):
        (tour_top_zero, tour_top_un) = self.count_tour()
        (tour_full_zero, tour_full_un) = self.count_tour_full()
        (tour_lonely_zero, tour_lonely_un) = self.count_tour_lonely()
        if self.is_over():
            if self.lose(tour_top_zero, tour_top_un): return -300
            elif self.win(tour_top_zero, tour_top_un): return 300
            else: return 0 #EGALITE
        else: return 10*(self.score_tour(tour_top_zero, tour_top_un)) -5*(self.score_tour_lonely(tour_lonely_zero, tour_lonely_un))+ 1*(self.score_tour_full(tour_full_zero, tour_full_un))
    

if __name__ == "__main__":
    
    from easyAI import AI_Player, Negamax

    game= [[[], [], [], [], [], [], [], [], []], 
        [[], [], [], [], [0, 0], [], [], [], []], 
        [[], [], [], [], [1], [], [], [], []], 
        [[], [], [], [1], [0], [1], [], [], []], 
        [[], [], [], [], [0,1,0,1], [1], [], [], []], 
        [[], [], [], [], [], [], [], [], []], 
        [[], [], [], [], [], [], [], [], []], 
        [[], [], [], [], [], [], [], [], []], 
        [[], [], [], [], [], [], [], [], []]]

    pion = 1

    ai_algo = Negamax(6)
    t = AvalamAI( [AI_Player(ai_algo),Human_Player()],game,1)
    move = t.player.ask_move(t)
    print(move)