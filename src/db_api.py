"""
This file contains all of the code that will actually talk to the database. 
The flask server will do all of the checking and then it will call the 
funcitons in this file, and then return the results to the caller. 
"""
import MySQLdb
import json

db = MySQLdb.connect("localhost", "root", "root", "TournamentRecorder")


def addPlayer(p_id, t_id):
    curs = db.cursor()
    curs.execute("""INSERT INTO tournament_player
                        (t_id, p_id) VALUES
                        (%s  , %s  ); """, [p_id, t_id])
    db.commit()
    return '{"outcome":true}'


def createPlayer(DCI, name):
    curs = db.cursor()
    curs.execute("""INSERT INTO player
                        (id, name) VALUES
                        (%s  , %s  ); """, [DCI, name])
    db.commit()
    return '{"outcome":true}'

def createTournament(name, max_rounds):
    pass

def finishRound(r_id):
    pass

def generatePairings(t_id):
    pass

def getPlayer(p_id):
    pass

def listPlayers():
    curs = db.cursor()
    curs.execute("""SELECT id, name FROM player; """, [])
    db.commit()
    
    output = []

    for row in curs.fetchall():
        output.append({'id': row[0], 'name': row[1]})
    return json.dumps(output)
    

def listTournaments(sort_on, filter_types):
    pass

def listTournamentPlayers(t_id):
    pass

def matchList(r_id):
    pass

def removePlayer(p_id, t_id):
    pass

def roundList(t_id):
    pass

def searchPlayers(partial_name):
    pass

def setMatchResults(m_id, p1_wins, p2_wins, draws):
    pass

def startTournament(t_id):
    pass

