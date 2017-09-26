line_up = [[0, 4, 8], [2, 4, 6], [0, 1, 2], [3, 4, 5], 
           [6,7,8], [0,3,6], [1,4,7], [2,5,8]]  

class Game:
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
        self.round = 0
        self.valid_macroboard = None
        
    def init_game(self):
        self.field = {(x,y):self.empty for x in range(9) for y in range(9)}
        self.macroboard = {(x, y):self.empty for x in range(3) for y in range(3)}
        self.valid_move = set([(x, y) for x in range(9) for y in range(9)])
        self.current_player = 0
        self.finish = False
        self.valid_macroboard = [-1] * 9
        self.round = 0
        
    def place_move(self, move):
        ## (x, y)
        if self.finish:
            return
        
        if move not in self.valid_move:
            print self.valid_move
            self.finish = True
            print('invalid move')
            return
        
        self.current_move = move            
        self.update_game()
        
    def get_state(self):
        board = ','.join([self.field[i%9, i/9] for i in range(81)])
        macroboard = ','.join(map(str, self.valid_macroboard))
        return board, macroboard


    def update_game(self):
        self.round += 1
        
        x, y = self.current_move
        px, py = (x / 3), (y / 3) # (px, py)-th macro_board
        mx, my = x % 3, y % 3 # (x, y)-th grid on (px, py)-th macro_board
        
        self.field[x, y] = self.symbol[self.current_player]
        
        if self.macroboard[px, py] == self.empty and self.check_victory(self.field, mx, my, px * 3, py * 3):
            self.macroboard[px, py] = self.symbol[self.current_player]
            if self.check_victory(self.macroboard, px, py, 0, 0):
                self.call_game()        
        
        
        self.valid_move = set()
        self.valid_macroboard = [self.macroboard[i%3, i/3] for i in range(9)]
        if self.macroboard[mx, my] == self.empty:
            self.valid_macroboard[3*my+mx] = self.valid
            
            for x in range(3):
                for y in range(3):
                    if self.field[3 * mx + x, 3 * my + y] == self.empty:
                        self.valid_move.add((3 * mx + x, 3 * my + y))
        else:
            for i in range(9):
                if self.macroboard[i%3, i/3] == self.empty:
                    self.valid_macroboard[i] = self.valid
                    for j in range(9):
                        px, py, mx, my = i%3, i/3, j%3, j/3
                        pos = (3 * px + mx, 3 * py + my)
                        if self.field[pos] == self.empty:
                            
                            self.valid_move.add(pos)
                    
        if not self.valid_move:
            self.call_game()  
        else:
            self.current_player = 1 - self.current_player 
        
    def check_victory(self, board, mx, my, px, py):        
        #check if previous move caused a win on vertical line 
        if board[px + 0, py + my] == board[px + 1, py + my] == board [px + 2, py + my]:
            return True

        #check if previous move caused a win on horizontal line 
        if board[px + mx, py + 0] == board[px + mx, py + 1] == board[px + mx, py + 2]:
            return True

        #check if previous move was on the main diagonal and caused a win
        if mx == my and board[px + 0, py + 0] == board[px + 1, py + 1] == board[px + 2, py + 2]:
            return True

        #check if previous move was on the secondary diagonal and caused a win
        if mx + my == 2 and board[px + 0, py + 2] == board[px + 1, py + 1] == board[px + 2, py + 0]:
            return True

        return False  

    def get_winner(self, field):
        ## return game_finish, winner
        winners = []
        curr = field
        for r0, r1, r2 in line_up:
            r0, r1, r2 = (r0/3, r0%3), (r1/3, r1%3), (r2/3, r2%3)
            if curr[r0] != self.empty and curr[r0] == curr[r1] == curr[r2]:
                winners.append(curr[r0])
                
        winner = None
        if len(set(winners)) == 1:
            winner = self.symbol.index(winners[0])
        return winner
    
    def call_game(self):
        self.finish = True
        self.winner = self.get_winner(self.macroboard)
        print('game finished')
        print('winner: bot ' + str(self.winner))