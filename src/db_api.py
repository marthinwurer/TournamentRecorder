"""
This file contains all of the code that will actually talk to the database. 
The flask server will do all of the checking and then it will call the 
funcitons in this file, and then return the results to the caller. 
Author: TangentTally
"""
import MySQLdb
import MySQLdb.cursors
import json
from datetime import datetime

config = {}
with open("config.json") as file:
    config = json.load(file)


db = MySQLdb.connect(config['dbserver'], config['dbusername'],
                        config['dbpassword'], config['dbname'],
                        cursorclass=MySQLdb.cursors.DictCursor)


def json_serial(obj):
    """
    JSON serializer for objects not serializable by default json code
    Taken from http://stackoverflow.com/a/22238613/3000741
    """

    # hassattr taken from http://stackoverflow.com/a/25895504/3000741
    if isinstance(obj, datetime) or hasattr(obj, 'isoformat'):
        serial = obj.isoformat()
        return serial
    print(type(obj))
    raise TypeError ("Type not serializable")


def tournament_status(t_id):
    """
        Check the status of a tournament
    """
    curs = db.cursor()
    curs.execute("""SELECT start_date, end_date
                        FROM tournament
                        WHERE id = %s; """, [t_id])
    result = curs.fetchone()
    if result['start_date'] == None:
        return "not started"
    elif result['end_date'] == None:
        return "started"
    else:
        return "finished"


def addPlayer(p_id, t_id):
    """
        Add a player to the given tournament. Only works if the tournament has not been 
        started and the player is not in the tournament
        :returns {outcome}
    """
    curs = db.cursor()

    # get the status of the current tournament
    t_status = tournament_status(t_id)

    # if the tournament is started or finsihed, then nothing happens. fail.
    if t_status != "not started":
        return '{"outcome":false, "reason": "Tournament started"}'

    # check if the player is in the tournament already
    curs.execute("""SELECT COUNT(*) AS count FROM tournament_player WHERE p_id=%s;""", [p_id])

    if curs.fetchone()['count'] > 0:
        return '{"outcome":false, "reason": "Player already registered"}'

    curs.execute("""INSERT INTO tournament_player
                        (p_id, t_id) VALUES
                        (%s  , %s  ); """, [p_id, t_id])
    db.commit()
    return '{"outcome":true}'


def createPlayer(DCI, name):
    """
    Creates a new player with the given DCI # and name.
    Fails if the DCI # already exists.
    :param DCI:
    :param name:
    :return: outcome
    """
    curs = db.cursor()
    curs.execute("""SELECT id FROM player WHERE id = %s""", [DCI])
    if curs.fetchone() != None:
        return '{"outcome":false, "reason":"DCI Exists"}'

    curs.execute("""INSERT INTO player
                        (id, name) VALUES
                        (%s  , %s  ); """, [DCI, name])
    db.commit()
    return '{"outcome":true}'


def createTournament(name, max_rounds):
    """
    Creates a new tournament with the given name and a maximum number of rounds
    :param name:
    :param max_rounds:
    :return: outcome
    """
    curs = db.cursor()
    curs.execute("""INSERT INTO tournament
                        (name, max_rounds) VALUES
                        (%s  , %s  ); """, [name, max_rounds])
    db.commit()
    return '{"outcome":true}'

def finishRound(r_id):
    """
    Finishes the given round
    Fails if the round does not exist, if the round is already finished, or if
    there are matches in progress.
    has a done field if the tournament has finished
    :param r_id:
    :returns outcome
    """
    curs = db.cursor()

    # make sure that there is a round to complete
    curs.execute("""SELECT end_date, t_id, number FROM round
                        WHERE id = %s; """, [r_id])
    result = curs.fetchone()
    if result == None:
        return '{"outcome":false, "reason":"Round does not exist"}'

    finished = result['end_date']
    t_id = result['t_id'] # grab this for testing the tournament
    r_number = result['number']
    if finished != None:
        return '{"outcome":false, "reason":"Round already finished"}'

    # then make sure that all matches are complete
    curs.execute("""SELECT COUNT(*) AS num FROM t_match
                        WHERE r_id = %s AND draws IS NULL; """, [r_id])
    num_unfinished = curs.fetchone()['num']
    if num_unfinished != 0:
        return '{"outcome":false, "reason":"Unfinished Matches"}'

    curs.execute("""UPDATE round
                        SET end_date=NOW()
                        WHERE id=%s; """, [r_id])

    outcome = {'outcome': True}

    # if the round is the last, finish the tournament
    # Get the max rounds of the current tournament
    curs.execute("""SELECT max_rounds 
                        FROM tournament
                        WHERE id = %s;""", [t_id])
    max_rounds = curs.fetchone()['max_rounds']
    # if the number of rounds is equal to the max rounds, finish the tournament
    if max_rounds == r_number:
        curs.execute("""UPDATE tournament
                            SET end_date=CURDATE()
                            WHERE id=%s; """, [t_id])
        outcome['done'] = True
    
    db.commit()
    return json.dumps(outcome)

def generatePairings(t_id):
    """
        Generate the pairings. 
        Only works if there are no rounds in progress for the tournament and 
        the tournament is not finished.
        :returns outcome
    """
    curs = db.cursor()

    # get the status of the current tournament
    t_status = tournament_status(t_id)

    # if the tournament is started or finsihed, then nothing happens. fail.
    if t_status != "started":
        return '{"outcome":false, "reason": "Tournament finished"}'

    # check if all the rounds in the tournament are finished. if not, fail
    curs.execute("""SELECT COUNT(*) AS num FROM round
                        WHERE t_id = %s AND end_date IS NULL; """, [t_id])
    num_unfinished = curs.fetchone()['num']
    if num_unfinished != 0:
        return '{"outcome":false, "reason":"Unfinsished Rounds"}'

    # create a round
    #get the previous round's number
    curs.execute("""SELECT MAX(number) AS max FROM round
                        WHERE t_id = %s; """, [t_id])
    result = curs.fetchone()
    print(result)
    previous = result['max']

    if previous == None:
        previous = 0

    num = previous + 1

    #insert it
    curs.execute("""INSERT INTO round
                        (t_id, number, start_date) VALUES
                        (%s  , %s  , NOW()); """, [t_id, num])

    # get its id
    curs.execute("""SELECT LAST_INSERT_ID() AS id; """, [])
    r_id = curs.fetchone()['id']

    # get a list of players
    curs.execute("""SELECT id, p_id, standing(id) AS standing
                        FROM tournament_player
                        WHERE t_id=%s AND dropped IS NULL
                        ORDER BY standing DESC; """, [t_id])
    playerList = curs.fetchall()
    print( playerList)

    # insert all the matches
    for ii in range(0, len(playerList), 2):
        first = playerList[ii]['id']
        table_num = ii // 2 + 1
        if ii + 1 < len(playerList):
            second = playerList[ii + 1]['id']
            curs.execute("""INSERT INTO t_match
                                (r_id, p1_id, p2_id, table_number) VALUES
                                (%s  , %s , %s , %s ); """, [r_id, first, second, table_num])
        else:
            second = None
            curs.execute("""INSERT INTO t_match
                            (r_id, p1_id, p2_id, table_number, 
                                p1_wins, p2_wins, draws) VALUES
                            (%s  , %s , %s , %s, 1, 0, 1 ); """,
                                [r_id, first, second, table_num])


    # only commit once everything is done
    db.commit()

    result = {}
    result['outcome'] = True
    return json.dumps(result)



def getPlayer(p_id):
    """
    Returns the information for the given player.
    {outcome, name, id}
    :param p_id:
    :return: {outcome, name, id}
    """
    curs = db.cursor()
    curs.execute("""SELECT id, name FROM player
                        WHERE id=%s; """, [p_id])
    db.commit()

    result = curs.fetchone()
    if result == None:
        return '{"outcome":false, "reason": "Player does not exist"}'
    result['outcome'] = True
    return json.dumps(result)

def getTournamentPlayer(tp_id):
    """
    Returns the information for the given Tournamanet player.
    {outcome, name, id, t_id, p_id, dropped, standing}
    :param p_id:
    :return: {outcome, name, id}
    """
    curs = db.cursor()
    curs.execute("""SELECT id, t_id, p_id, dropped, STANDING(id) AS standing FROM tournament_player
                        WHERE id=%s; """, [tp_id])
    db.commit()

    result = curs.fetchone()
    if result == None:
        return '{"outcome":false, "reason": "Player does not exist"}'
    result['outcome'] = True
    return json.dumps(result)

def listPlayers():
    """
    :returns:
    {outcome: true/false,
     rows:[{id, name }]}
    """
    curs = db.cursor()
    curs.execute("""SELECT id, name FROM player; """, [])
    db.commit()
    
    result = curs.fetchall()
    
    #add the outcome variable
    output = {'outcome': True, 'rows': result}
    
    return json.dumps(output)
    

def listTournaments(sort_on, filter_types):
    """
    Returns a list of tournaments sorted by sort on and filtered by the types in filter types
    :returns:
    {outcome: true/false,
     rows:[{id, name, num_players, start_date, end_date}]}
    """
    curs = db.cursor()
    curs.execute("""SELECT t.id, t.name, (
                        SELECT COUNT(*)
                        FROM tournament_player as p
                        WHERE p.t_id=t.id) as num_players,
                        t.start_date, t.end_date
                    FROM tournament as t; """, [])
    db.commit()
    
    result = curs.fetchall()
    
    #add the outcome variable
    output = {'outcome': True, 'rows': result}
    
    return json.dumps(output, default=json_serial)

def listTournamentPlayersHelper(t_id):
    curs = db.cursor()
    curs.execute("""SELECT tp.id, tp.p_id, (
                            SELECT name FROM player AS p WHERE p.id=tp.p_id
                            ) AS name, standing(tp.id) AS standing, dropped
                        FROM tournament_player AS tp
                        WHERE tp.t_id=%s; """, [t_id])
    db.commit()
    
    result = curs.fetchall()
    
    return result


def listTournamentPlayers(t_id):
    """
    :param t_id:
    :return:
    {outcome:
     rows:[
        { id, p_id, name, standing, dropped (None if not dropped, 1 if dropped) }]
    }
    """
    # call the helper function
    output = {'outcome': True, 'rows': listTournamentPlayersHelper(t_id)}
    
    return json.dumps(output)

def listActiveTournamentPlayers(t_id):
    """
    :param t_id:
    :return:
    {outcome:
     rows:[
        { id, p_id, name, standing, dropped (None if not dropped, 1 if dropped) }]
    }
    """
    curs = db.cursor()
    curs.execute("""SELECT tp.id, tp.p_id, (
                            SELECT name FROM player AS p WHERE p.id=tp.p_id
                            ) AS name, standing(tp.id) AS standing, dropped
                        FROM tournament_player AS tp
                        WHERE tp.t_id=%s AND tp.dropped IS NULL; """, [t_id])

    # build the output
    output = {'outcome': True, 'rows': curs.fetchall()}

    return json.dumps(output)

def matchList(r_id):
    """
    :param r_id:
    :return:
    {outcome:
     rows:[
        { id, table_number, p1_id, p2_id, p1_wins, p2_wins, draws}
        ]
    }
    """
    curs = db.cursor()
    curs.execute("""SELECT id, table_number, p1_id, p2_id, p1_wins, p2_wins, draws,
                        (SELECT p.name FROM player AS p WHERE p.id=(SELECT p_id FROM tournament_player WHERE id=p1_id)) AS p1_name,
                        (SELECT p.name FROM player AS p WHERE p.id=(SELECT p_id FROM tournament_player WHERE id=p2_id)) AS p2_name
                        FROM t_match
                        WHERE r_id = %s; """, [r_id])
    db.commit()
    
    result = curs.fetchall()
    
    #add the outcome variable
    output = {'outcome': True, 'rows': result}
    
    return json.dumps(output)

def removePlayer(tp_id, t_id):
    """
        Only do this if the player has no outstanding match results.

        If the tournament has not started, the tournament player is deleted instead of being
        set to dropped.

        :returns outcome
    """
    print( tp_id, t_id)
    curs = db.cursor()
    
    # get the status of the current tournament
    t_status = tournament_status(t_id)

    # if the tournament is finsihed, then nothing happens. fail.
    if t_status == "finished":
        return '{"outcome":false, "reason": "Tournament finished"}'

    # if the tournament has not been started, then delete the tournament player
    if t_status == "not started":
        curs.execute("""DELETE FROM tournament_player WHERE id = %s;""",
                        [tp_id])
        db.commit()
        return '{"outcome":true}'


    # check the number of ongoing matches the player is in.
    curs.execute("""SELECT COUNT(*) AS count FROM t_match 
                        WHERE (p1_id = %s OR p2_id = %s) AND draws IS NULL;""", [tp_id, tp_id])
    count = curs.fetchone()['count']
    print(count)

    # if there are no ongoing matches, then remove the plyer. otherwise, report failure
    if count == 0:
        curs.execute("""UPDATE tournament_player
                            SET dropped = 1
                            WHERE id = %s; """, [tp_id])
        db.commit()
        return '{"outcome":true}'
    else:
        return '{"outcome":false, "reason": "Match in progress"}'


def roundList(t_id):
    """
    List the rounds for the given tournament
    :param t_id:
    :return:
    {outcome:
     rows:[
        { id, table_number, p1_id, p2_id, p1_wins, p2_wins, draws}
        ]
    }
    """
    curs = db.cursor()
    curs.execute("""SELECT id, number, start_date, end_date
                        FROM round
                        WHERE t_id = %s; """, [t_id])
    db.commit()
    
    result = curs.fetchall()
    
    #add the outcome variable
    output = {'outcome': True, 'rows': result}
    
    return json.dumps(output, default=json_serial)

def searchPlayers(partial_name):
    """
    Look for players whose name contains the partial name
    :param partial_name:
    :return:
    {outcome: true/false,
     rows:[{id, name }]}
    """
    curs = db.cursor()
    curs.execute("""SELECT id, name FROM player
                        WHERE name LIKE %s; """, ['%' + partial_name + '%'])
    db.commit()

    result = curs.fetchall()
    
    #add the outcome variable
    output = {'outcome': True, 'rows': result}
    
    return json.dumps(output)

def setMatchResults(m_id, p1_wins, p2_wins, draws):
    """
        Sets the results of a match.
        Only works if the round is not finished.
    """
    curs = db.cursor()

    # get the round ID
    curs.execute("""SELECT r_id FROM t_match WHERE id = %s;""", [m_id])
    r_id = curs.fetchone()['r_id']

    # get the round status. exit if round is finished
    curs.execute("""SELECT end_date FROM round
                        WHERE id = %s; """, [r_id])
    result = curs.fetchone()
    finished = result['end_date']
    if finished != None:
        return '{"outcome":false, "reason":"Round results finalized"}'


    curs.execute("""UPDATE t_match
                        SET p1_wins = %s, p2_wins = %s, draws = %s
                        WHERE id = %s; """, [p1_wins, p2_wins, draws, m_id])
    db.commit()

    result = {}
    result['outcome'] = True
    return json.dumps(result)


def startTournament(t_id):
    """
        Start a tournament. 
        Only works if the tournament has not been started yet.
    """
    curs = db.cursor()

    # get the status of the current tournament
    t_status = tournament_status(t_id)

    # if the tournament is started or finsihed, then nothing happens. fail.
    if t_status != "not started":
        return '{"outcome":false, "reason": "Tournament started"}'

    curs.execute("""UPDATE tournament
                        SET start_date = CURDATE()
                        WHERE id = %s; """, [t_id])
    db.commit()
    result = generatePairings(t_id)

    return result

