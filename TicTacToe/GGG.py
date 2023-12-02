"""A tic-tac-toe game built with Python and Tkinter."""

import tkinter as tk
from itertools import cycle
from tkinter import font
from typing import NamedTuple
from random import random


cell_to_board_map = {
    (0,0):'7',
    (1,0):'4',
    (2,0):'1',
    (0,1):'8',
    (1,1):'5',
    (2,1):'2',
    (0,2):'9',
    (1,2):'6',
    (2,2):'3',
}

BOARD_TO_CELL = {v:k for k,v in cell_to_board_map.items()}

def get_empty_board():
    return {v:" " for v in cell_to_board_map.values()}


def printBoard(board):
    print(board['7'] + '|' + board['8'] + '|' + board['9'])
    print('-+-+-')
    print(board['4'] + '|' + board['5'] + '|' + board['6'])
    print('-+-+-')
    print(board['1'] + '|' + board['2'] + '|' + board['3'])


scoreMap = {"X": 1, "O": -1}

def checkWinner(theBoard):
    result = None # None not finished 0 draw, 1 X won, -1 O won
    if theBoard['7'] == theBoard['8'] == theBoard['9'] != ' ': # across the top
        return scoreMap[theBoard['7']]
    elif theBoard['4'] == theBoard['5'] == theBoard['6'] != ' ': # across the middle
        return scoreMap[theBoard['4']]
    elif theBoard['1'] == theBoard['2'] == theBoard['3'] != ' ': # across the bottom
        return scoreMap[theBoard['1']]
    elif theBoard['1'] == theBoard['4'] == theBoard['7'] != ' ': # down the left side
        return scoreMap[theBoard['1']]
    elif theBoard['2'] == theBoard['5'] == theBoard['8'] != ' ': # down the middle
        return scoreMap[theBoard['2']]
    elif theBoard['3'] == theBoard['6'] == theBoard['9'] != ' ': # down the right side
        return scoreMap[theBoard['3']]
    elif theBoard['7'] == theBoard['5'] == theBoard['3'] != ' ': # diagonal
        return scoreMap[theBoard['7']]
    elif theBoard['1'] == theBoard['5'] == theBoard['9'] != ' ': # diagonal
        return scoreMap[theBoard['1']]
    
    if all([value!=" " for value in theBoard.values()]):
        return 0
    return result

def current_moves_to_board(current_moves):
    board = get_empty_board()

    for row in current_moves:
        for move in row:
            row_ind, col_ind =  move.row, move.col
            label = move.label
            if label in ("X", "O"):
                board[cell_to_board_map[(row_ind,col_ind)]] = label
    printBoard(board)
    return board 


def get_next_func(turn):
    return min if turn == "X" else max

next_turn = lambda turn : "O" if turn == "X" else "X"

def minimax(board, turn, func=max):
    my_score = None
    best_move = None
    
    table_score = checkWinner(board)
    if table_score is not None:
        return table_score, None
    for x in range(1,10):
        x = str(x)
        if board[x] != " ":
            continue
        board[x] = turn
        opponent = next_turn(turn)
        score, move = minimax(board,opponent,get_next_func(turn))
#         print(board, x, score, move)
        if my_score is None or score == func([my_score,score]):
            my_score= score
            best_move= str(x)
        board[x] = " "
    return my_score, best_move

tictactoe_move_count = lambda board : sum([1 if v!=" " else 0 for v in board.values() ])
tmc = tictactoe_move_count

def minimax_with_length(board, turn, func=max):
        my_score = None
        best_move = None

        table_score = checkWinner(board)
        if table_score is not None:
            table_score = table_score * 10
            move_count = tmc(board)
            if table_score == -10:
                table_score =  table_score + move_count
            elif table_score == 10:
                table_score =  table_score - move_count
            
            return table_score, None
        for x in range(1,10):
            x = str(x)
            if board[x] != " ":
                continue
            board[x] = turn
            opponent = next_turn(turn)
            score, move = minimax_with_length(board,opponent,get_next_func(turn))
    #         print(board, x, score, move)
            if my_score is None or score == func([my_score,score]):
                my_score= score
                best_move= str(x)
            board[x] = " "
        return my_score, best_move


class Player(NamedTuple):
    label: str
    color: str

class Move(NamedTuple):
    row: int
    col: int
    label: str = ""

BOARD_SIZE = 3
DEFAULT_PLAYERS = (
    Player(label="X", color="black"),
    Player(label="O", color="green"),
)

class TicTacToeGame:
    def __init__(self, players=DEFAULT_PLAYERS, board_size=BOARD_SIZE):
        self._players = cycle(players)
        self.board_size = board_size
        self.current_player = next(self._players)
        self.winner_combo = []
        self._current_moves = []
        self._has_winner = False
        self._winning_combos = []
        self._setup_board()

    def _setup_board(self):
        self._current_moves = [
            [Move(row, col) for col in range(self.board_size)]
            for row in range(self.board_size)
        ]
        self._winning_combos = self._get_winning_combos()

    def _get_winning_combos(self):
        rows = [
            [(move.row, move.col) for move in row]
            for row in self._current_moves
        ]
        columns = [list(col) for col in zip(*rows)]
        first_diagonal = [row[i] for i, row in enumerate(rows)]
        second_diagonal = [col[j] for j, col in enumerate(reversed(columns))]
        return rows + columns + [first_diagonal, second_diagonal]

    def toggle_player(self):
        """Return a toggled player."""
        self.current_player = next(self._players)

    def is_valid_move(self, move):
        """Return True if move is valid, and False otherwise."""
        row, col = move.row, move.col
        move_was_not_played = self._current_moves[row][col].label == ""
        no_winner = not self._has_winner
        return no_winner and move_was_not_played

    def process_move(self, move):
        """Process the current move and check if it's a win."""
        row, col = move.row, move.col
        self._current_moves[row][col] = move
        for combo in self._winning_combos:
            results = set(self._current_moves[n][m].label for n, m in combo)
            is_win = (len(results) == 1) and ("" not in results)
            if is_win:
                self._has_winner = True
                self.winner_combo = combo
                break

    def has_winner(self):
        """Return True if the game has a winner, and False otherwise."""
        return self._has_winner

    def is_tied(self):
        """Return True if the game is tied, and False otherwise."""
        no_winner = not self._has_winner
        played_moves = (
            move.label for row in self._current_moves for move in row
        )
        return no_winner and all(played_moves)

    def reset_game(self):
        """Reset the game state to play again."""
        for row, row_content in enumerate(self._current_moves):
            for col, _ in enumerate(row_content):
                row_content[col] = Move(row, col)
        self._has_winner = False
        self.winner_combo = []

class TicTacToeBoard(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.title("Tic-Tac-Toe Game")
        self._cells = {}
        self.cell_to_button = {}
        self._game = game
        self._create_menu()
        self._create_board_display()
        self._create_board_grid()

    def _create_menu(self):
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(master=menu_bar)
        file_menu.add_command(label="Play Again", command=self.reset_board)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

    def _create_board_display(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text="Ready?",
            font=font.Font(size=28, weight="bold"),
        )
        self.display.pack()

    def _create_board_grid(self):
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()
        for row in range(self._game.board_size):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)
            for col in range(self._game.board_size):
                button = tk.Button(
                    master=grid_frame,
                    text="",
                    font=font.Font(size=36, weight="bold"),
                    fg="black",
                    width=3,
                    height=2,
                    highlightbackground="lightblue",
                )
                self._cells[button] = (row, col)
                button.bind("<ButtonPress-1>", self.play)
                button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

                self.cell_to_button[(row,col)] = button

    def random_ai(self):
        """  Random response by AI"""
        while True:
            row, col = int(random()*3),int(random()*3)
            move = Move(row, col, self._game.current_player.label)
            if self._game.is_valid_move(move): 
                return move
    
    def minimax_ai(self):
        """  Minimax response by AI"""
        board = current_moves_to_board(self._game._current_moves)

        turn = self._game.current_player.label
        func = max if turn == "X" else min
        score, move = minimax(board,turn, func)
        row, col = BOARD_TO_CELL[move]
        print(f"Minimax move row: {row} col: {col}", f"AI score: {score}")
        move = Move(row, col, self._game.current_player.label)
        return move
    
    def minimax_with_length_ai(self):
        """  Minimax with length response by AI"""
        board = current_moves_to_board(self._game._current_moves)

        turn = self._game.current_player.label
        func = max if turn == "X" else min
        score, move = minimax_with_length(board,turn, func)
        row, col = BOARD_TO_CELL[move]
        print(f"Minimax with length move row: {row} col: {col}", f"AI score: {score}")
        move = Move(row, col, self._game.current_player.label)
        return move
    
    def play(self, event=None, move = None):
        """Handle a player's move."""

        if move is None:
            clicked_btn = event.widget
            row, col = self._cells[clicked_btn]
            move = Move(row, col, self._game.current_player.label)
        else:
            row, col = move.row, move.col
            print("Row col", row,col)
            clicked_btn = self.cell_to_button[(row,col)]

        if self._game.is_valid_move(move):
            self._update_button(clicked_btn)
            self._game.process_move(move)
            if self._game.is_tied():
                self._update_display(msg="Tied game!", color="red")
            elif self._game.has_winner():
                self._highlight_cells()
                msg = f'Player "{self._game.current_player.label}" won!'
                color = self._game.current_player.color
                self._update_display(msg, color)
            else:
                self._game.toggle_player()
                msg = f"{self._game.current_player.label}'s turn"
                self._update_display(msg)
                if event is not None:
                    self.play(move=self.minimax_with_length_ai())


    def _update_button(self, clicked_btn):
        clicked_btn.config(text=self._game.current_player.label)
        clicked_btn.config(fg=self._game.current_player.color)

    def _update_display(self, msg, color="black"):
        self.display["text"] = msg
        self.display["fg"] = color

    def _highlight_cells(self):
        for button, coordinates in self._cells.items():
            if coordinates in self._game.winner_combo:
                button.config(highlightbackground="red")

    def reset_board(self):
        """Reset the game's board to play again."""
        self._game.reset_game()
        self._update_display(msg="Ready?")
        for button in self._cells.keys():
            button.config(highlightbackground="lightblue")
            button.config(text="")
            button.config(fg="black")

def main():
    """Create the game's board and run its main loop."""
    game = TicTacToeGame()
    board = TicTacToeBoard(game)
    board.mainloop()

if __name__ == "__main__":
    main()