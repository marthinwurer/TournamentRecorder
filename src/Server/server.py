from flask import Flask
import MySQLdb

app = Flask(__name__)

db = MySQLdb.connect("localhost", "root", "root", "TournamentRecorder")

def countDogs():
    curs = db.cursor()
    curs.execute("SELECT COUNT(*) FROM dogs;")
    return curs.fetchone()

def listDogs():
    curs = db.cursor()
    curs.execute('SELECT * FROM dogs;')
    return curs.fetchall()

@app.route('/adddog/<string:name>')
def add_dog(name):
    curs = db.cursor()
    curs.execute('INSERT INTO dogs (name) VALUES (%s);', [name])
    db.commit()
    
    return 'Hello, World!' + str(countDogs());

@app.route('/')
def hello_world():
    return 'Hello, World!' + str(countDogs());

@app.route('/listdogs/')
def list_dogs():
    return str(listDogs())

@app.route('/removedog/<int:id>')
def remove_dog(id):
    curs = db.cursor()
    curs.execute('DELETE FROM dogs WHERE ID = %s;', [id])
    db.commit()
    
    return str(listDogs());

