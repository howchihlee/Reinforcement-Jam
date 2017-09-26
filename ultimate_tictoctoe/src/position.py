
class Position:
    def __init__(self):
        self.board = {}
        self.macroboard = []
        self.valid = '-1'
        self.symbol = ['1', '2']
        self.empty = '0'
        
    def parse_field(self, fstr):
        flist = fstr.replace(';', ',').split(',')
        self.board = {(i%9, i/9):f for i, f in enumerate(flist)}
    
    def parse_macroboard(self, mbstr):
        mblist = mbstr.replace(';', ',').split(',')
        self.macroboard = [f for f in mblist ]
    
    def is_legal(self, x, y):
        mbx, mby = x/3, y/3
        return self.macroboard[3*mby+mbx] == self.valid and self.board[y, x] == self.empty

    def legal_moves(self):
        return [ (x, y) for x in range(9) for y in range(9) if self.is_legal(x, y) ]
        
    def make_move(self, x, y, pid):
        mbx, mby = x/3, y/3
        self.macroboard[3*mby+mbx] = -1
        self.board[y, x] = pid
        
    def get_board(self):
        return ''.join(self.board, ',')

    def get_macroboard(self):
        return ''.join(self.macroboard, ',')