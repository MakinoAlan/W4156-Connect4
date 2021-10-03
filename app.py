import logging
import db
from flask import Flask, render_template, request, jsonify
from json import dumps
from Gameboard import Gameboard


app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

game = Gameboard()
db.init_db()

'''
Implement '/' endpoint
Method Type: GET
return: template player1_connect.html and status = "Pick a Color."
Initial Webpage where gameboard is initialized
'''


@app.route('/', methods=['GET'])
def player1_connect():
    global game
    last_state = db.getMove()
    if last_state is not None:
        game = Gameboard()
        game.board = last_state[1]
        game.current_turn = last_state[0]
        game.game_result = last_state[2]
        game.player1 = last_state[3]
        game.player2 = last_state[4]
        game.remaining_moves = last_state[5]
        if game.player1 != '':
            return render_template('player1_connect.html', status=f'{game.player1} picked')
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
    db.add_move(game)
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
    if game.player1 != '' and game.player2 != '':
        return render_template('p2Join.html', status=f'{game.player2} picked')
    if game.player1 == '':
        return render_template('p2Join.html', status='Error')
    p2_color = 'yellow' if game.player1 == 'red' else 'red'
    game.player2 = p2_color
    db.add_move(game)
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
    x = game.get_x_axis_value(y)

    error_reason = game.check_common_error(x, y, 'p1')
    if error_reason is not None:
        return dumps({
            'move': game.board,
            'invalid': True,
            'reason': f'{error_reason}',
            'winner': game.game_result})

    game.move(x, y, 'p1')

    if game.is_win(x, y, game.player1):
        game.game_result = 'p1'
        db.clear()
    else:
        db.add_move(game)

    return dumps({
        'move': game.board,
        'invalid': False,
        'status': f'{game.game_result} win',
        'winner': game.game_result})


'''
Same as '/move1' but instead process Player 2
'''


@app.route('/move2', methods=['POST'])
def p2_move():
    payload = request.get_json()
    y = int(payload['column'][-1]) - 1
    x = game.get_x_axis_value(y)

    '''
    Completeness check
    '''

    error_reason = game.check_common_error(x, y, 'p2')
    if error_reason is not None:
        return dumps({
            'move': game.board,
            'invalid': True,
            'reason': f'{error_reason}',
            'winner': game.game_result})

    game.move(x, y, 'p2')

    if game.is_win(x, y, game.player2):
        game.game_result = 'p2'
        db.clear()
    else:
        db.add_move(game)

    return dumps({
        'move': game.board,
        'invalid': False,
        'status': f'{game.game_result} win',
        'winner': game.game_result})


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
