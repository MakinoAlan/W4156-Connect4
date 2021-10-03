import sqlite3
from sqlite3 import Error, Connection
from Gameboard import Gameboard

'''
Initializes the Table GAME
Do not modify
'''


def init_db():
    # creates Table
    conn = None
    try:
        conn = sqlite3.connect('sqlite_db')
        conn.execute('CREATE TABLE GAME(current_turn TEXT, board TEXT,' +
                     'winner TEXT, player1 TEXT, player2 TEXT' +
                     ', remaining_moves INT)')
        print('Database Online, table created')
    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()


'''
move is a tuple (current_turn, board, winner, player1, player2,
remaining_moves)
Insert Tuple into table
'''


def add_move(move):  # will take in a tuple
    conn = None
    try:
        conn = sqlite3.connect('sqlite_db')
        cur = conn.cursor()

        for i in range(len(move.board)):
            for j in range(len(move.board[i])):
                if move.board[i][j] == 'red':
                    move.board[i][j] = 1
                if move.board[i][j] == 'yellow':
                    move.board[i][j] = 2

        cur.execute(f"INSERT INTO GAME VALUES('{move.current_turn}', '{move.board}'," +
                    f"'{move.game_result}', '{move.player1}', '{move.player2}', {move.remaining_moves})")
        conn.commit()
    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()


'''
Get the last move played
return (current_turn, board, winner, player1, player2, remaining_moves)
'''


def getMove():
    conn = None
    try:
        conn = sqlite3.connect('sqlite_db')
        cur = conn.cursor()
        cur.execute("select * from GAME")

        rows = cur.fetchall()

        if len(rows) == 0:
            return None

        last_row = list(rows[-1])
        last_row[1] = eval(last_row[1])

        for i in range(len(last_row[1])):
            for j in range(len(last_row[1][i])):
                if last_row[1][i][j] == 1:
                    last_row[1][i][j] = 'red'
                if last_row[1][i][j] == 2:
                    last_row[1][i][j] = 'yellow'

        return last_row
    except Error as e:
        print(e)
        return None
    finally:
        if conn:
            conn.close()


'''
Clears the Table GAME
Do not modify
'''


def clear():
    conn = None
    try:
        conn = sqlite3.connect('sqlite_db')
        conn.execute("DROP TABLE GAME")
        print('Database Cleared')
    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()
