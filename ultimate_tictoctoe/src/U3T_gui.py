import Tkinter as tk
from tkFont import Font
#helv36 = tkFont.Font(family='Helvetica', size=24, weight=tkFont.BOLD)
#frame = Frame(width=510, height=510, bg="", colormap="new")
class U3T_GUI:
    def __init__(self, game, bot):
        self.bot = bot
        self.bot.init_bot()
        self.bot.myid = 1
        #self.bot_pos = Position()
        self.current_player = 0
        self.app = tk.Tk()
        self.game = game
        self.game.init_game()
        
        self.title = 'Utilmate TicTacToe'
        self.default_font = Font(family="Helvetica", size=24)
        self.button_dict = {}
        self.current_player = 0
        self.valid_button = set()
        
        if self.bot.myid == 0:
            self.bot_move()   
            
    def initial_layout(self):
        self.app.title('Ultimate TicTacToe')
        self.app.resizable(width=False, height=False)        
        self.app.geometry("510x510")
        for i in range(9):
            for j in range(9):
                btn = tk.Button(self.app, text = self.map_output(self.game.field[i,j]), font = self.default_font)
                btn.place(x = 20 + i * 50 + (i / 3) * 10 , y = 20 + j * 50 + (j / 3) * 10 , width=50, height=50)
                btn.bind("<Button-1>", self.pressed)
                self.button_dict[btn] = [(i, j)]
                    
        self.valid_button = self.button_dict.keys()
        self.update_layout()
    
    def pressed(self, event):  
        if not event.widget in self.valid_button:
            return
        
        k = self.button_dict[event.widget][0]
        self.make_move(k)
        
        if not self.game.finish:
            self.bot_move()
        
        #board, macroboard = self.game.get_state()
        #print macroboard
        #for i in range(9):
        #    print board.replace(',', '')[i * 9:(i+1) * 9]
        #print '---'
        
    def bot_move(self):
        self.app.config(cursor="watch")
        
        board, macroboard = self.game.get_state()
        
        move = self.bot.get_move(board, macroboard)
        self.make_move(move)
        self.app.config(cursor="")
        
    def make_move(self, move):
        self.game.place_move(move)
        self.update_valid_button()
        self.update_layout()
        self.current_player = self.game.current_player

    def update_valid_button(self):
        tmp = set()
        #print self.game.valid_move
        for btn, item in self.button_dict.items():
            if item[0] in self.game.valid_move:
                tmp.add(btn)
                
        self.valid_button = tmp
        return
        
    def update_layout(self):
        #print self.board.valid_board
        #for item in self.board.field:
        #    print item
        
        for btn, item in self.button_dict.items():
            i, j = item[0]
            btn['text'] = self.map_output(self.game.field[i,j])
            if self.game.macroboard[i/3, j/3] == self.game.empty:
                btn['disabledforeground'] = 'black'
                btn['foreground'] = 'black'
            elif self.game.macroboard[i/3, j/3] == self.game.symbol[0]:
                btn['disabledforeground'] = 'red'
                btn['foreground'] = 'red'
            else:
                btn['disabledforeground'] = 'blue'
                btn['foreground'] = 'blue'
                
            if btn in self.valid_button:
                btn['state'] = 'normal'
                btn['background'] = '#a1dbcd'
            else:
                btn['state'] = 'disabled'
                btn['background'] = 'AntiqueWhite3'
        return
    
    def map_output(self, s):
        #return s
        if s == '0':
            return ''
        if s == '1':
            return 'o'
        if s == '2':
            return 'x'
        
    def run(self):
        self.initial_layout()
        self.app.mainloop()
    