"""
This file is the base flask server. It parses HTTP requests and then calls the
correct DB API function.
Author: TangentTally
"""
from flask import Flask, request
import traceback

from db_api import *

app = Flask(__name__)


@app.route('/tr-api/<string:function>', methods=['POST'])
def recieve(function):
    json = None
    result = '{"outcome":false}'
    try:
        json = request.get_json()
        if function == 'addPlayer':
            return addPlayer(json['p_id'], json['t_id'])
        elif function == 'createPlayer':
            return createPlayer(json['DCI'], json['name'])
        elif function == 'createTournament':
            return createTournament(json['name'], json['max_rounds'])
        elif function == 'finishRound':
            return finishRound(json['r_id'])
        elif function == 'generatePairings':
            return generatePairings(json['t_id'])
        elif function == 'getPlayer':
            return getPlayer(json['p_id'])
        elif function == 'getTournamentPlayer':
            return getTournamentPlayer(json['tp_id'])
        elif function == 'listPlayers':
            return listPlayers()
        elif function == 'listTournaments':
            return listTournaments(json['sort_on'], json['filter_types'])
        elif function == 'listTournamentPlayers':
            return listTournamentPlayers(json['t_id'])
        elif function == 'listActiveTournamentPlayers':
            return listActiveTournamentPlayers(json['t_id'])
        elif function == 'matchList':
            return matchList(json['r_id'])
        elif function == 'removePlayer':
            return removePlayer(json['p_id'], json['t_id'])
        elif function == 'roundList':
            return roundList(json['t_id'])
        elif function == 'searchPlayers':
            return searchPlayers(json['partial_name'])
        elif function == 'setMatchResults':
            return setMatchResults(json['m_id'], json['p1_wins'], json['p2_wins'], json['draws'])
        elif function == 'startTournament':
            return startTournament(json['t_id'])
        else:
            print(function + "not found")

            return '{"outcome":false}' # return false if nothing found

    except :
        traceback.print_exc()
        db.rollback()
        print("         an error occurred")
        return '{"outcome":false}' # return false if it failed
    print(json)

    return result


@app.route('/')
def hello_world():
    return 'Hello, World!'
