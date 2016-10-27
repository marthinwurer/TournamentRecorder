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
    curs = db.cursor()
    curs.execute("""INSERT INTO tournament
                        (name, max_rounds) VALUES
                        (%s  , %s  ); """, [name, max_rounds])
    db.commit()
    return '{"outcome":true}'

def finishRound(r_id):
    curs = db.cursor()
    curs.execute("""UPDATE round
                        SET end_date=NOW()
                        WHERE id=%s; """, [r_id])
    db.commit()
    return '{"outcome":true}'

def generatePairings(t_id):
    pass

def getPlayer(p_id):
    curs = db.cursor()
    curs.execute("""SELECT id, name FROM player
                        WHERE id=%s; """, [p_id])
    db.commit()
    
    result = curs.fetchone()
    output = {'id': result[0], 'name': result[1]}
    return output

def listPlayers():
    curs = db.cursor()
    curs.execute("""SELECT id, name FROM player; """, [])
    db.commit()
    
    output = []

    for row in curs.fetchall():
        output.append({'id': row[0], 'name': row[1]})
    return json.dumps(output)
    

def listTournaments(sort_on, filter_types):
    curs = db.cursor()
    curs.execute("""SELECT t.id, t.name, (
                        SELECT COUNT(*) 
                        FROM tournament_player as p
                        WHERE p.t_id=t.id)
                            as num_players
                        FROM tournament as t; """, [])
    db.commit()
    
    output = []

    for row in curs.fetchall():
        output.append({'id': row[0], 'name': row[1], 'num_players': row[2]})
    return json.dumps(output)

def listTournamentPlayers(t_id):
    curs = db.cursor()
    curs.execute("""SELECT tp.id, tp.p_id, (
                            SELECT name FROM player AS p WHERE p.id=tp.p_id
                            ) AS name
                        FROM tournament_player AS tp
                        WHERE pt.t_id=%s; """, [t_id])
    db.commit()
    
    result = curs.fetchone()
    output = {'id': result[0], 'p_id': result[1], 'name': result[2]}
    return output

def matchList(r_id):
    curs = db.cursor()
    # TODO
    curs.execute("""SELECT id, p1 FROM player; """, [])
    db.commit()
    
    output = []

    for row in curs.fetchall():
        output.append({'id': row[0], 'name': row[1]})
    return json.dumps(output)

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

