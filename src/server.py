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
        elif function == 'listPlayers':
            return listPlayers()
        elif function == 'createPlayer':
            return createPlayer(json['DCI'], json['name'])
        else:
            print(function + "not found")

            return '{"outcome":false}' # return false if nothing found

    except :
        traceback.print_exc()
        print("         an error occurred")
        return '{"outcome":false}' # return false if it failed
    print(json)

    return result


@app.route('/')
def hello_world():
    return 'Hello, World!'
