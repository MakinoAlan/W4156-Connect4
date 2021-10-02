import unittest
import db
from Gameboard import Gameboard


class test_db(unittest.TestCase):

    def test_init_defaultBehavior_tableCreated(self):
        db.init_db()
        test = db.getMove()
        self.assertEqual(None, test)

    def test_addMove_validMove_tupleInserted(self):
        move = Gameboard()
        move.player1 = 'red'
        move.player2 = 'yellow'
        move.remaining_moves = 1
        db.add_move(move)
        last_move = db.getMove()
        self.assertEqual(last_move.player1, move.player1)
        self.assertEqual(last_move.player2, move.player2)
        self.assertEqual(last_move.board, move.board)
        self.assertEqual(last_move.game_result, move.game_result)
        self.assertEqual(last_move.current_turn, move.current_turn)
        self.assertEqual(last_move.remaining_moves, move.remaining_moves)
