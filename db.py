import sqlite3
from sqlite3 import Error, Connection
from json import dumps

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

        test = cur.fetchall()[-1]
        test1 = cur.fetchone()

        return cur.fetchall()[-1]
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
