from textual.app import App, ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import Button, Header, Footer, Static
from textual.screen import Screen
from textual.geometry import Size

#import sys
#sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=32, cols=50))


board = [["E", "E", "E"], ["E", "E", "E"], ["E", "E", "E"]]
t = 1
x_score = 0
o_score = 0

def highlight_win_location(*loc):
    global x_score, o_score
    highlight = ""
    all_location = ["row1", "row2", "row3","ver1", "ver2", "ver3", "diag1", "diag2"]
    all_positions = ["#b11", "#b12", "#b13","#b21", "#b22", "#b23", "#b31", "#b32", "#b33"]
    actual_positions = []
    win = False
    positions = []
    n = 0
    for i in loc:
        n += 1
        if i == "XXX":
            highlight = all_location[n-1]
            win = True
            x_score += 1
        elif i == "OOO":
            highlight = all_location[n-1]
            win = True
            o_score += 1
        
    match highlight:
        case "row1":
            positions = ["#b11", "#b12", "#b13"]
        case "row2":
            positions = ["#b21", "#b22", "#b23"]
        case "row3":
            positions = ["#b31", "#b32", "#b33"]
        case "ver1":
            positions = ["#b11", "#b21", "#b31"]
        case "ver2":
            positions = ["#b12", "#b22", "#b32"]            
        case "ver3":
            positions = ["#b13", "#b23", "#b33"]
        case "diag1":
            positions = ["#b11", "#b22", "#b33"]
        case "diag2":
            positions = ["#b13", "#b22", "#b31"]           
    update_score()
    
    if win:
        actual_positions = [x for x in all_positions if x not in positions]   
        for p in actual_positions:
            app.query_one(p).disabled = True

def reset_board():
    global board
    board = [["E", "E", "E"], ["E", "E", "E"], ["E", "E", "E"]]
    b_id = ""
    for i in range(1,4):
        row = i
        for x in range(1, 4):
            column = x
            b_id = f"b{row}{column}"
            app.query_one(f"#{b_id}").disabled = False
            app.query_one(f"#{b_id}").label = "[]"
    app.query_one("#display").label = "NO WINNER YET"
    update_score()
def check_win():
    global board
    row1 = board[0][0] + board[0][1] + board[0][2] 
    row2 = board[1][0] + board[1][1] + board[1][2]
    row3 = board[2][0] + board[2][1] + board[2][2]

    ver1 = board[0][0] + board[1][0] + board [2][0]
    ver2 = board[0][1] + board[1][1] + board [2][1]
    ver3 = board[0][2] + board[1][2] + board [2][2]

    diag1 = board[0][0] + board[1][1] + board[2][2]
    diag2 = board[0][2] + board[1][1] + board[2][0]
    empty = False
    highlight_win_location(row1, row2, row3, ver1, ver2, ver3, diag1, diag2)
    
    for i in range(3):
        for j in board[i]:
            if j == "E":
                empty = True
    if row1 == "XXX" or row2 == "XXX" or row3 == "XXX":
        update_score()
        return "X WINS"
    if row1 == "OOO" or row2 == "OOO" or row3 == "OOO":
        return "O WINS"
    if ver1 == "XXX" or ver2 == "XXX" or ver3 == "XXX":
        return "X WINS"
    if ver1 == "OOO" or ver2 == "OOO" or ver3 == "OOO":
        return "O WINS"
    if diag1 == "OOO" or diag2 == "OOO":
        return "O WINS"
    if diag1 == "XXX" or diag2 == "XXX":
        return "X WINS"
    if not empty:
        for p in ["#b11", "#b12", "#b13","#b21", "#b22", "#b23", "#b31", "#b32", "#b33"]:
            app.query_one(p).disabled = True
        return "TIE"
    else:
        return "NO WINNER YET"
   
def update():
    app.query_one("#display").label = check_win()

def update_score():
    app.query_one("#scoreboard_X").label = f"X: {x_score}"
    app.query_one("#scoreboard_O").label = f"O: {o_score}"

class Display(Static):
    "Display"
    test_var = "NULL"
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "reset":
            global t, board
            reset_board()
    def compose(self) -> ComposeResult:
        
        yield Button("NO WINNER YET", id = "display", classes = "normal")
        yield Button("NEW GAME", id = "reset", classes = "normal")

class ttt_board(Static):
    "Tic Tac Toe widget"
    ACTIVE_EFFECT_DURATION = 100
    def on_button_pressed(self, event: Button.Pressed) -> None:
        global t, board, x_score, o_score
        if event.button.id == "restart":
            x_score = 0
            o_score = 0
            t = 1
            reset_board()
        if event.button.name == "blank" and t == 1 and board[int(event.button.id[1])-1][int(event.button.id[2])-1] == "E":
            event.button.label = "X"
            board[int(event.button.id[1])-1][int(event.button.id[2])-1] = "X"
            
            t = 2
        elif event.button.name == "blank" and t == 2 and board[int(event.button.id[1])-1][int(event.button.id[2])-1] == "E":
            event.button.label = "O"
            board[int(event.button.id[1])-1][int(event.button.id[2])-1] = "O"

            t = 1
        update()

    def compose(self) -> ComposeResult:
        yield Container(
            Display(),
            Button("[]", id = "b11", name="blank", classes  = "normal"),
            Button("[]", id = "b12", name="blank", classes = "normal"),
            Button("[]", id = "b13", name="blank", classes = "normal"),
            Button("[]", id = "b21", name="blank", classes = "normal"),
            Button("[]", id = "b22", name="blank", classes = "normal"),
            Button("[]", id = "b23", name="blank", classes = "normal"),
            Button("[]", id = "b31", name="blank", classes = "normal"),
            Button("[]", id = "b32", name="blank", classes = "normal"),
            Button("[]", id = "b33", name="blank", classes = "normal"),
            Button(f"X: {x_score}", id = "scoreboard_O", classes = "normal"),
            Button(f"O: {o_score}", id = "scoreboard_X", classes = "normal"),
            Button("RESTART", id = "restart", classes = "normal"),
            id = "board"
        )

class ttt_app(App):
    "Tic Tac Toe game"
    CSS_PATH = "ttt.css"
    BINDINGS = [    
        ("d", "toggle_dark", "Toggle dark mode"),
        ("D", "toggle_dark", "Toggle dark mode")
    ]
    def action_toggle_dark(self) -> None:
        self.dark = not self.dark
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Container(ttt_board())  
        
            


if __name__ == "__main__":
    app = ttt_app()
    app.run()        