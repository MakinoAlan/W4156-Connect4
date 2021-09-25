import unittest
from Gameboard import Gameboard


class TestStringMethods(unittest.TestCase):

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

    def test_tie_remainingMovesIs0_returnTrue(self):
        game = Gameboard()
        game.remaining_moves = 0
        self.assertEqual(True, game.is_tie())

    def test_tie_remainingMovesIsNot0_returnFalse(self):
        game = Gameboard()
        game.remaining_moves = 21
        self.assertEqual(False, game.is_tie())


if __name__ == '__main__':
    unittest.main()