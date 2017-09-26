from itertools import product 
import pickle

with open('./src/t3_winner.p', 'rb') as f:
    t3_winner = pickle.load(f)
    
class U3T_board:
    def __init__(self):
        self.symbol = ['1', '2']
        self.empty = '0'
        self.valid = '-1'
        self.field = None
        self.macroboard = None
        self.finish = False   
        
        self.valid_move = set()
        self.winner = None
        self.current_player = None
        self.current_move = None
        #self.valid_macroboard = None
        
    def init_game(self):
        self.field = [[self.empty] * 9 for i in range(9)]
        self.macroboard = [self.empty] * 9
        self.valid_move = set([(x, y) for x in range(9) for y in range(9)])
        self.current_player = 0
        self.finish = False
        #self.valid_macroboard = [-1] * 9
        
    def set_game(self, field, current_move, current_player):
        self.init_game()
        self.field = field
        self.current_player = current_player
        self.current_move = current_move
        
        for i, f in enumerate(field):
            wi = self.get_winner(f)
            if wi != -1:
                self.macroboard[i] = self.symbol[wi]

        self.update_game()
        
    def place_move(self, move):
        ## (x, y)
        if self.finish:
            return
        

        self.current_move = move            
        self.update_game()

    def update_game(self):
        x, y = self.current_move
        px, py = (x // 3), (y // 3) # (px, py)-th macro_board
        mx, my = x % 3, y % 3 # (x, y)-th grid on (px, py)-th macro_board
        mi = 3 * my + mx
        pi = 3 * py + px
        
        
        self.field[pi][mi] = self.symbol[self.current_player]
        
        if self.macroboard[pi] == self.empty and self.check_victory(self.field[pi]):
            self.macroboard[pi] = self.symbol[self.current_player]
            if self.check_victory(self.macroboard):
                self.call_game()        
        
        
        self.valid_move = set()
        #self.valid_macroboard = [self.macroboard[i] for i in range(9)]
        if self.macroboard[mi] == self.empty:
            #self.valid_macroboard[3*my+mx] = self.valid
            for i in range(9):
                if self.field[mi][i] == self.empty:
                    self.valid_move.add((3 * mx + i%3, 3 * my + i/3))
        else:
            for i in range(9):
                if self.macroboard[i] == self.empty:
                    for j in range(9):
                        if self.field[i][j] == self.empty:
                            px, py, mx, my = i%3, i/3, j%3, j/3
                            self.valid_move.add((3 * px + mx, 3 * py + my))
                    
        if not self.valid_move:
            self.call_game()  
        else:
            self.current_player = 1 - self.current_player 
        
    def check_victory(self, board):        
        wi = self.get_winner(board)
        
        return wi != -1  

    def get_winner(self, board):
        return t3_winner[tuple(board)]
        
    
    def call_game(self):
        self.finish = True

        self.winner = self.get_winner(self.macroboard)
        
        
import time
from random import choice
from copy import deepcopy

def get_microboards(field):
    microboards = [[] for i in range(9)]
    for i in range(9):
        tmp = []
        for j in range(9):
            px, py, mx, my = i%3, i/3, j%3, j/3
            tmp.append(field[3 * px + mx, 3 * py + my])
        microboards[i] = tmp
    return microboards

def parse_field(fstr):
    flist = fstr.strip().replace(';', ',').split(',')
    return {(i%9, i/9):f for i, f in enumerate(flist)}
    
def parse_macroboard(mbstr):
    mblist = mbstr.strip().replace(';', ',').split(',')
    
    
    return [f for f in mblist ]

def get_best_moves(scores, moves):
    best_score = max(scores)
    best_moves = [m for s, m in zip(scores, moves) if s == best_score]        
    return best_score, best_moves   

class mc_node:
    def __init__(self):
        self.expand = False
        self.num_move = 0
        self.moveset = {}
        self.movelist = []
        self.stats = [] ## player 0 win, player 1 win, total
        
    def update_stat(self, move, winner):
        self.expand_move(move)
            
        move_id = self.moveset[move]
        if winner != -1:
            self.stats[move_id][winner] += 1
        self.stats[move_id][2] += 1
        #print winner
    def expand_move(self, move):
        if move not in self.moveset:
            self.moveset[move] = self.num_move
            self.movelist.append(move)
            self.stats.append([0, 0, 0])
            self.num_move += 1
        
            
class MC_bot:
    def __init__(self):
        self.empty = '0'
        self.symbol = ['1','2']
        self.valid = '-1'
        self.mygame = U3T_board()
        self.myid = None
        #self.memory = {}
        
    def init_bot(self):
        self.mygame = U3T_board()
        self.myid = None
        
    def run_simulation(self, start_node, start_move):
        game = self.mygame
        #game_history = [(start_key, start_move)]
        
        while not game.finish:
            move = choice([m for m in game.valid_move])
            
            #func_key = self.get_key(game.field, [game.macroboard[i%3, i/3] for i in range(9)]) 
            #game_history.append([func_key, move])
            game.place_move(move)
        
        #for func_key, move in game_history:
        #    if func_key not in self.memory:
        #        self.memory[func_key] = mc_node()
        #    
        #    self.memory[func_key].update_stat(move, game.winner)  
        
        start_node.update_stat(start_move, game.winner)  
        
    def get_key(self, board, macroboard):
        tmp = [board[x, y] for x, y in product(range(9), repeat=2)] 
        tmp += [macroboard[i] for i in range(9)]
        return ''.join(tmp)
    
    def get_move(self, bstr, mbstr):
        macroboard = parse_macroboard(mbstr)
        board = parse_field(bstr)
        microboards = get_microboards(board)
        
        curr_node = mc_node()
        
        if not curr_node.expand:
            poss_macroboard = [i for i, s in enumerate(macroboard) if s == self.valid]

            for p in poss_macroboard:
                px, py = p % 3, p // 3
                for x, y in product(range(3), repeat = 2):
                    pos = (3 * px + x, 3 * py + y)
                    if board[pos] == self.empty:
                        curr_node.expand_move(pos)
                        
            curr_node.expand = True
            
        tic = time.clock()
        c = 0
        tspan = 0.48
        
        n_move = curr_node.num_move
        valid_move = curr_node.movelist
        
        while time.clock() - tic < tspan:
            c = c % n_move
            p = valid_move[c]
            self.mygame.set_game(deepcopy(microboards), p, self.myid)
            self.run_simulation(curr_node, p)
            c += 1
        
        #print curr_node.stats
        scores = map(lambda x: self.child_score(x), curr_node.stats)
        _, moves = get_best_moves(scores, valid_move)
        return choice(moves)
        
    def child_score(self, stat):
        w = stat[self.myid] - stat[1 - self.myid];
        n = stat[2]
        #c = 1.41421356237
        #t = parent.total_tries;
        return float(w) / float(n)
    