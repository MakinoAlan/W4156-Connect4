import db


class Gameboard():
    def __init__(self):
        self.player1 = ""
        self.player2 = ""
        self.board = [[0 for x in range(7)] for y in range(6)]
        self.game_result = ""
        self.current_turn = 'p1'
        self.remaining_moves = 42

    def move(self, x, y, player):
        if player == 'p1':
            self.board[x][y] = self.player1
            self.current_turn = 'p2'
        else:
            self.board[x][y] = self.player2
            self.current_turn = 'p1'
        self.remaining_moves -= 1

    def is_tie(self):
        if self.remaining_moves == 0:
            self.game_result = "tie"
            return True
        return False
