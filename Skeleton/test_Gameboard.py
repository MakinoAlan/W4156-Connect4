import unittest
from Gameboard import Gameboard


class test_Gameboard(unittest.TestCase):

    def test_init_byDefault_dataLoadCorrectly(self):
        game = Gameboard()
        self.assertEqual('', game.player1)
        self.assertEqual('', game.player2)
        self.assertEqual('', game.game_result)
        self.assertEqual('p1', game.current_turn)
        self.assertEqual(42, game.remaining_moves)
        for i in range(6):
            for j in range(7):
                self.assertEqual(0, game.board[i][j])

    def test_move_p1ValidMove_updateBoard(self):
        game = Gameboard()
        game.player1 = 'red'
        game.move(1, 2, 'p1')
        self.assertEqual('red', game.board[1][2])
        self.assertEqual('p2', game.current_turn)
        self.assertEqual(41, game.remaining_moves)
        self.assertEqual('', game.game_result)

    def test_move_p2ValidMove_updateBoard(self):
        game = Gameboard()
        game.player2 = 'yellow'
        game.move(1, 2, 'p2')
        self.assertEqual('yellow', game.board[1][2])
        self.assertEqual('p1', game.current_turn)
        self.assertEqual(41, game.remaining_moves)
        self.assertEqual('', game.game_result)

    def test_isTie_remainingMovesIs0_returnTrue(self):
        game = Gameboard()
        game.remaining_moves = 0
        self.assertEqual(True, game.is_tie())

    def test_isTie_remainingMovesIsNot0_returnFalse(self):
        game = Gameboard()
        game.remaining_moves = 21
        self.assertEqual(False, game.is_tie())

    def test_checkCommonError_invalidPosition_returnErrorMessage(self):
        game = Gameboard()
        self.assertEqual(
            'position is unreachable - out of the board. 100, 100',
            game.check_common_error(100, 100, 'p1'))

    def test_checkCommonError_invalidCurrentTurn_returnErrorMessage(self):
        game = Gameboard()
        game.current_turn = 'p1'
        self.assertEqual('Not your turn.', game.check_common_error(0, 0, 'p2'))

    def test_checkCommonError_moveOnTakenSpot_returnErrorMessage(self):
        game = Gameboard()
        game.board[1][1] = 'red'
        self.assertEqual(
            'Slot already be taken',
            game.check_common_error(1, 1, 'p1'))

    def test_checkCommonError_hasGameResult_returnGameOverMessage(self):
        game = Gameboard()
        game.game_result = 'p1'
        self.assertEqual(
            'Game is over. The winner is p1',
            game.check_common_error(1, 1, 'p1'))

    def test_checkCommonError_remainingMoveIsO_returnErrorMessage(self):
        game = Gameboard()
        game.remaining_moves = 0
        self.assertEqual(
            'Game board is full, tie.',
            game.check_common_error(1, 1, 'p1'))

    def test_getXAxisValue_validXValueExist_returnXValue(self):
        game = Gameboard()
        game.board[5][6] = 'red'
        x = game.get_x_axis_value(6)
        self.assertEqual(4, x)

    def test_getXAxisValue_fullInRow_returnMinusOne(self):
        game = Gameboard()
        for i in range(6):
            game.board[i][0] = 'red'
        x = game.get_x_axis_value(0)
        self.assertEqual(-1, x)

    def test_isWin_isRowWinReturnTrue_returnTrue(self):
        game = Gameboard()
        for i in range(4):
            game.board[1][i] = 'yellow'
        self.assertEqual(True, game.is_win(1, 3, 'yellow'))

    def test_isRowWin_winConditionExistsEast_returnTrue(self):
        game = Gameboard()
        for i in range(4):
            game.board[1][i] = 'yellow'
        self.assertEqual(True, game.is_row_win(1, 3, 'yellow'))

    def test_isRowWin_winConditionExistsWest_returnTrue(self):
        game = Gameboard()
        for i in range(4):
            game.board[1][i] = 'yellow'
        self.assertEqual(True, game.is_row_win(1, 0, 'yellow'))

    def test_isRowWin_winConditionNotExists_returnFalse(self):
        game = Gameboard()
        for i in range(2):
            game.board[1][i] = 'yellow'
        self.assertEqual(False, game.is_row_win(1, 3, 'yellow'))

    def test_isColumnWin_winConditionExists_returnTrue(self):
        game = Gameboard()
        for i in range(4):
            game.board[5 - i][1] = 'red'
        self.assertEqual(True, game.is_column_win(2, 1, 'red'))

    def test_isColumnWin_winConditionNotExists_returnFalse(self):
        game = Gameboard()
        for i in range(2):
            game.board[5 - i][1] = 'red'
        self.assertEqual(False, game.is_column_win(2, 1, 'red'))

    def test_isColumnWin_invalidInput_returnFalse(self):
        game = Gameboard()
        self.assertEqual(False, game.is_column_win(8, 1, 'red'))

    def test_isDiagonalWin_winConditionExistsNorthWest_returnTrue(self):
        game = Gameboard()
        game.board[5][6] = 'red'
        game.board[4][5] = 'red'
        game.board[3][4] = 'red'
        game.board[2][3] = 'red'
        self.assertEqual(True, game.is_diagonal_win(2, 3, 'red'))

    def test_isDiagonalWin_winConditionNotExistsNorthWest_returnFalse(self):
        game = Gameboard()
        game.board[5][6] = 'red'
        game.board[2][3] = 'red'
        self.assertEqual(False, game.is_diagonal_win(1, 4, 'yellow'))

    def test_isDiagonalWin_winConditionExistsSouthEast_returnTrue(self):
        game = Gameboard()
        game.board[5][6] = 'red'
        game.board[4][5] = 'red'
        game.board[3][4] = 'red'
        game.board[2][3] = 'red'
        self.assertEqual(True, game.is_diagonal_win(5, 6, 'red'))

    def test_isDiagonalWin_winConditionNotExistsSouthEast_returnFalse(self):
        game = Gameboard()
        game.board[5][6] = 'red'
        game.board[2][3] = 'red'
        self.assertEqual(False, game.is_diagonal_win(5, 6, 'red'))

    def test_isDiagonalWin_winConditionExistsNorthEast_returnTrue(self):
        game = Gameboard()
        game.board[5][0] = 'red'
        game.board[4][1] = 'red'
        game.board[3][2] = 'red'
        game.board[2][3] = 'red'
        self.assertEqual(True, game.is_diagonal_win(2, 3, 'red'))

    def test_isDiagonalWin_winConditionExistsSouthWest_returnTrue(self):
        game = Gameboard()
        game.board[5][0] = 'red'
        game.board[4][1] = 'red'
        game.board[3][2] = 'red'
        game.board[2][3] = 'red'
        self.assertEqual(True, game.is_diagonal_win(5, 0, 'red'))

    def test_isDiagonalWin_winConditionNotExists_returnFalse(self):
        game = Gameboard()
        game.board[5][0] = 'yellow'
        game.board[4][1] = 'yellow'
        game.board[3][2] = 'yellow'
        self.assertEqual(False, game.is_diagonal_win(3, 2, 'yellow'))


if __name__ == '__main__':
    unittest.main()
