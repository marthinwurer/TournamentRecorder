"""
This file contains all of the code that will actually talk to the database. 
The flask server will do all of the checking and then it will call the 
funcitons in this file, and then return the results to the caller. 
"""
import MySQLdb
import MySQLdb.cursors
import json

db = MySQLdb.connect("localhost", "root", "root", "TournamentRecorder",
                        cursorclass=MySQLdb.cursors.DictCursor)


def addPlayer(p_id, t_id):
    curs = db.cursor()
    curs.execute("""INSERT INTO tournament_player
                        (p_id, t_id) VALUES
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
    """
        This is the real complex business logic. For now, just generate a list of players
        and pair them in order
    """
    # get a list of players
    playerList = listTournamentPlayersHelper(t_id)
    print( playerList)

    # create a round
    curs = db.cursor()
    #get the previous round's number
    curs.execute("""SELECT MAX(number) AS max FROM round
                        WHERE t_id = %s; """, [t_id])
    previous = curs.fetchone()['max']

    if previous == None:
        previous = 0

    num = previous + 1


    #insert it
    curs.execute("""INSERT INTO round
                        (t_id, number) VALUES
                        (%s  , %s  ); """, [t_id, num])

    # get its id
    curs.execute("""SELECT id FROM round
                        WHERE t_id = %s AND number = %s; """, [t_id, num])
    r_id = curs.fetchone()['id']

    
    for ii in range(0, len(playerList), 2):
        first = playerList[ii]['id']
        if ii + 1 < len(playerList):
            second = playerList[ii + 1]['id']
        else:
            second = 'NULL'

        table_num = ii // 2 + 1

        curs.execute("""INSERT INTO t_match
                            (r_id, p1_id, p2_id, table_number) VALUES
                            (%s  , %s , %s , %s ); """, [r_id, first, second, table_num])

    # only commit once everything is done
    db.commit()

    result = {}
    result['outcome'] = True
    return json.dumps(result)
    


def getPlayer(p_id):
    curs = db.cursor()
    curs.execute("""SELECT id, name FROM player
                        WHERE id=%s; """, [p_id])
    db.commit()
    
    result = curs.fetchone()
    result['outcome'] = True
    return json.dumps(result)

def listPlayers():
    curs = db.cursor()
    curs.execute("""SELECT id, name FROM player; """, [])
    db.commit()
    
    result = curs.fetchall()
    
    #add the outcome variable
    output = {'outcome': True, 'rows': result}
    
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
    
    result = curs.fetchall()
    
    #add the outcome variable
    output = {'outcome': True, 'rows': result}
    
    return json.dumps(output)

def listTournamentPlayersHelper(t_id):
    curs = db.cursor()
    curs.execute("""SELECT tp.id, tp.p_id, (
                            SELECT name FROM player AS p WHERE p.id=tp.p_id
                            ) AS name
                        FROM tournament_player AS tp
                        WHERE tp.t_id=%s; """, [t_id])
    db.commit()
    
    result = curs.fetchall()
    
    return result


def listTournamentPlayers(t_id):
    # call the helper function
    output = {'outcome': True, 'rows': listTournamentPlayersHelper(t_id)}
    
    return json.dumps(output)

def matchList(r_id):
    curs = db.cursor()
    curs.execute("""SELECT table_number, p1_id, p2_id, p1_wins, p2_wins, draws
                        FROM t_match
                        WHERE r_id = %s; """, [r_id])
    db.commit()
    
    result = curs.fetchall()
    
    #add the outcome variable
    output = {'outcome': True, 'rows': result}
    
    return json.dumps(output)

def removePlayer(p_id, t_id):
    """
        Only do this if the player has no outstanding match results

    """
    curs = db.cursor()
    
    # get the player's tp_id
    curs.execute("""SELECT id FROM tournament_player 
                        WHERE p_id = %s AND t_id = %s;""", [p_id, t_id])
    tp_id = curs.fetchone()['id']

    # check the number of ongoing matches the player is in.
    curs.execute("""SELECT COUNT(*) AS count FROM t_matches 
                        WHERE p1_id = %s OR p2_id = %s AND draws IS NULL;""" [tp_id, tp_id])
    count = curs.fetchone()['count']

    # if there are no ongoing matches, then remove the plyer. otherwise, report failure
    if count == 0:
        curs.execute("""UPDATE tournament_player
                            SET dropped = 1
                            WHERE id = %s; """, [tp_id])
        db.commit()
        return '{"outcome":true}'
    else:
        return '{"outcome":false}'


def roundList(t_id):
    curs = db.cursor()
    curs.execute("""SELECT id, number, start_date, end_date
                        FROM round
                        WHERE t_id = %s; """, [t_id])
    db.commit()
    
    result = curs.fetchall()
    
    #add the outcome variable
    output = {'outcome': True, 'rows': result}
    
    return json.dumps(output)

def searchPlayers(partial_name):
    curs = db.cursor()
    curs.execute("""SELECT id, name FROM player
                        WHERE name LIKE "%%s%"; """, [partial_name])
    db.commit()
    
    result = curs.fetchone()
    result['outcome'] = True
    return json.dumps(result)

def setMatchResults(m_id, p1_wins, p2_wins, draws):
    curs = db.cursor()
    curs.execute("""UPDATE t_match
                        SET p1_wins = %s, p2_wins = %s, draws = %s
                        WHERE m_id = %s; """, [p1_wins, p2_wins, draws, m_id])
    db.commit()

    result = {}
    result['outcome'] = True
    return json.dumps(result)


def startTournament(t_id):
    curs = db.cursor()
    curs.execute("""UPDATE tournament
                        SET start_date = CURDATE()
                        WHERE id = %s; """, [t_id])
    db.commit()

    return generatePairings(t_id)

