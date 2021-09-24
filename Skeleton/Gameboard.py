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

    def check_common_error(self, x, y, player):
        if x >= 6 or x < 0 or y >= 7 or y < 0:
            return f'position is unreachable - out of the board. {x}, {y}'

        if self.current_turn != player:
            return 'Not your turn.'

        if self.board[x][y] != 0:
            return 'Slot already be taken'

        if self.game_result != "":
            return f'Game is over. The winner is {self.game_result}'

        if self.remaining_moves == 0:
            return 'There is no slot for new move.'

        if self.is_tie():
            return 'Game board is full, tie.'

    def get_x_axis_value(self, y):
        for i in range(5, -1, -1):
            if self.board[i][y] == 0:
                return i
        return -1

    def is_win(self, x, y, color):
        return self.is_row_win(x, y, color) or self.is_column_win(x, y, color) or self.is_diagonal_win(x, y, color)

    def is_row_win(self, x, y, color):
        counter_row = 0
        for i in range(y, 7, 1):
            if self.board[x][i] == color:
                counter_row += 1
                if counter_row == 4:
                    return True
            else:
                break
        counter_row -= 1;
        for i in range(y, -1, -1):
            if self.board[x][i] == color:
                counter_row += 1
                if counter_row == 4:
                    return True
            else:
                break
        return False

    '''
    Base on the game rule, for column we only need to check downside
    '''

    def is_column_win(self, x, y, color):
        counter_col = 0
        for i in range(x, 6, 1):
            if i >= 6:
                break
            if self.board[i][y] == color:
                counter_col += 1
                if counter_col == 4:
                    return True
            else:
                break
        return False

    def is_diagonal_win(self, x, y, color):
        counter_diagonal = 1
        i = 1
        while x - i >= 0 and y - i >= 0:
            if self.board[x - i][y - i] == color:
                counter_diagonal += 1
                i += 1
                if counter_diagonal == 4:
                    return True
            else:
                break

        i = 1
        while x + i < 6 and y + i < 7:
            if self.board[x + i][y + i] == color:
                counter_diagonal += 1
                i += 1
                if counter_diagonal == 4:
                    return True
            else:
                break

        counter_diagonal = 1
        i = 1
        while x - i >= 0 and y + i < 7:
            if self.board[x - i][y + i] == color:
                counter_diagonal += 1
                i += 1
                if counter_diagonal == 4:
                    return True
            else:
                break

        i = 1
        while x + i < 6 and y - i >= 0:
            if self.board[x + i][y - i] == color:
                counter_diagonal += 1
                i += 1
                if counter_diagonal == 4:
                    return True
            else:
                break
        return False
