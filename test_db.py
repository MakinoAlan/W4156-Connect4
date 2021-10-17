import unittest
import db
from Gameboard import Gameboard


class test_db(unittest.TestCase):
    '''
    I will skip init() and clear() as it is provided by default
    This unit tests will cover the two methods I implemented
    add_move and get_move

    Since this is the integration test: Business layer <-> Database layer
    Tests will just check if two parts can communicate and return data
    The correctness of data is checked in business layer - gameboard.py
    '''

    def test_getMove_dbEmpty_returnNone(self):
        db.clear()
        db.init_db()
        test = db.getMove()
        self.assertEqual(None, test)
        db.clear()

    def test_addAndGetMove_validMoveRed_tupleCanInsertAndReturn(self):
        db.clear()
        db.init_db()
        move = Gameboard()
        move.player1 = 'red'
        move.player2 = 'yellow'
        move.remaining_moves = 1
        move.board[0][0] = 'red'
        db.add_move(move)
        last_move = db.getMove()
        self.assertEqual(last_move[3], move.player1)
        self.assertEqual(last_move[4], move.player2)
        self.assertEqual(last_move[1], move.board)
        self.assertEqual(last_move[2], move.game_result)
        self.assertEqual(last_move[0], move.current_turn)
        self.assertEqual(last_move[5], move.remaining_moves)
        db.clear()

    def test_addAndGetMove_validMoveYellow_tupleCanInsertAndReturn(self):
        db.clear()
        db.init_db()
        move = Gameboard()
        move.player1 = 'red'
        move.player2 = 'yellow'
        move.remaining_moves = 1
        move.board[0][0] = 'yellow'
        db.add_move(move)
        last_move = db.getMove()
        self.assertEqual(last_move[3], move.player1)
        self.assertEqual(last_move[4], move.player2)
        self.assertEqual(last_move[1], move.board)
        self.assertEqual(last_move[2], move.game_result)
        self.assertEqual(last_move[0], move.current_turn)
        self.assertEqual(last_move[5], move.remaining_moves)
        db.clear()

