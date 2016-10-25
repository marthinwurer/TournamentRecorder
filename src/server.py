from flask import Flask, request

app = Flask(__name__)


@app.route('/tr-api/', methods=['POST'])
def recieve():
    json = None
    try:
        json = request.get_json()
    except:
        return '{"outcome":false}' # return false if it failed
    print(json)


    
    return '{"outcome":true}'


@app.route('/')
def hello_world():
    return 'Hello, World!'
