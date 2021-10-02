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
        db.add_move(move)
        last_move = db.getMove()
        self.assertEqual(last_move.player1, move.player1)
