from flask import Flask

app = Flask(__name__)


@app.route('/tt-api/', methods=['POST'])
def recieve():
    try:
        json = request.get_json()
    except:
        return '{"outcome":false}' # return false if it failed


    
    return '{"outcome":true}'


@app.route('/')
def hello_world():
    return 'Hello, World!'
