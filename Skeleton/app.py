from flask import Flask, render_template, request, redirect, jsonify
from json import dump, dumps
from Gameboard import Gameboard
import db


app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

game = Gameboard()

'''
Implement '/' endpoint
Method Type: GET
return: template player1_connect.html and status = "Pick a Color."
Initial Webpage where gameboard is initialized
'''


@app.route('/', methods=['GET'])
def player1_connect():
    global game
    game = Gameboard()
    return render_template('player1_connect.html', status='Pick a Color.')


'''
Helper function that sends to all boards don't modify
'''


@app.route('/autoUpdate', methods=['GET'])
def updateAllBoards():
    try:
        return jsonify(move=game.board, winner=game.game_result,
                       color=game.player1)
    except Exception:
        return jsonify(move="")


'''
Implement '/p1Color' endpoint
Method Type: GET
return: template player1_connect.html and status = <Color picked>
Assign player1 their color
'''


@app.route('/p1Color', methods=['GET'])
def player1_config():
    color = request.args.get('color')
    game.player1 = color
    return render_template('player1_connect.html', status=f'{color} picked')


'''
Implement '/p2Join' endpoint
Method Type: GET
return: template p2Join.html and status = <Color picked> or Error
if P1 didn't pick color first

Assign player2 their color
'''


@app.route('/p2Join', methods=['GET'])
def p2Join():
    color = request.args.get('color')
    if game.player1 == '':
        return render_template('p2Join.html', status='Error')
    p2_color = 'yellow' if game.player1 == 'red' else 'red'
    game.player2 = p2_color
    return render_template('p2Join.html', status=f'{p2_color} picked')


'''
Implement '/move1' endpoint
Method Type: POST
return: jsonify (move=<CurrentBoard>,
invalid=True or False, winner = <currWinner>)
If move is valid --> invalid = False else invalid = True
If invalid == True, also return reason= <Why Move is Invalid>

Process Player 1's move
'''


@app.route('/move1', methods=['POST'])
def p1_move():
    payload = request.get_json()
    y = int(payload['column'][-1]) - 1
    x = get_x_axis_value(y)

    error_reason = check_common_error(x, y, 'p1')
    if error_reason is not None:
        return dumps({'move': game.board, 'invalid': True, 'reason': f'{error_reason}'})

    game.board[x][y] = game.player1
    game.current_turn = 'p2'

    if is_win(x, y, game.player1):
        game.game_result = 'p1'

    return dumps({'move': game.board, 'invalid': False, 'status': f'{game.game_result} win'})


'''
Same as '/move1' but instead proccess Player 2
'''


@app.route('/move2', methods=['POST'])
def p2_move():
    payload = request.get_json()
    y = int(payload['column'][-1]) - 1
    x = get_x_axis_value(y)

    '''
    Completeness check
    Though it is almost impossible, server side should handle all potential case
    '''

    error_reason = check_common_error(x, y, 'p2')
    if error_reason is not None:
        return dumps({'move': game.board, 'invalid': True, 'reason': f'{error_reason}'})

    '''
    Update board if no error found
    '''
    game.board[x][y] = game.player2
    game.current_turn = 'p1'

    if is_win(x, y, game.player2):
        game.game_result = 'p2'

    return dumps({'move': game.board, 'invalid': False, 'status': f'{game.game_result} win'})


def check_common_error(x, y, player):
    if x >= 6 or x < 0 or y >= 7 or y < 0:
        return f'position is unreachable - out of the board. {x}, {y}'

    if game.current_turn != player:
        return 'Invalid turn.'

    if game.board[x][y] != 0:
        return 'Slot already be taken'


def get_x_axis_value(y):
    for i in range(5, -1, -1):
        if game.board[i][y] == 0:
            return i
    return -1


def is_win(x, y, color):
    return is_row_win(x, y, color) or is_column_win(x, y, color) or is_diagonal_win(x, y, color)


def is_row_win(x, y, color):
    counter_row = 0
    for i in range(y, 7, 1):
        if game.board[x][i] == color:
            counter_row += 1
            if counter_row == 4:
                return True
        else:
            break
    counter_row -= 1;
    for i in range(y, -1, -1):
        if game.board[x][i] == color:
            counter_row += 1
            if counter_row == 4:
                return True
        else:
            break
    return False


'''
Base on the game rule, for column we only need to check downside
'''


def is_column_win(x, y, color):
    counter_col = 0
    for i in range(x, 6, 1):
        if i >= 6:
            break
        if game.board[i][y] == color:
            counter_col += 1
            if counter_col == 4:
                return True
        else:
            break
    return False


def is_diagonal_win(x, y, color):
    counter_diagonal = 1
    i = 1
    while x - i >= 0 and y - i >= 0:
        if game.board[x - i][y - i] == color:
            counter_diagonal += 1
            i += 1
            if counter_diagonal == 4:
                return True
        else:
            break

    i = 1
    while x + i < 6 and y + i < 7:
        if game.board[x + i][y + i] == color:
            counter_diagonal += 1
            i += 1
            if counter_diagonal == 4:
                return True
        else:
            break

    counter_diagonal = 1
    i = 1
    while x - i >= 0 and y + i < 7:
        if game.board[x - i][y + i] == color:
            counter_diagonal += 1
            i += 1
            if counter_diagonal == 4:
                return True
        else:
            break

    i = 1
    while x + i < 6 and y - i >= 0:
        if game.board[x + i][y - i] == color:
            counter_diagonal += 1
            i += 1
            if counter_diagonal == 4:
                return True
        else:
            break
    return False


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
