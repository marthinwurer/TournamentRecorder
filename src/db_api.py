"""
This file contains all of the code that will actually talk to the database. 
The flask server will do all of the checking and then it will call the 
funcitons in this file, and then return the results to the caller. 
"""
import MySQLdb

db = MySQLdb.connect("localhost", "root", "root", "TournamentRecorder")

def addPlayer(p_id, t_id):
    cur = db.cursor()
    curs.execute("""INSERT INTO tournament_player
                        (t_id, p_id) VALUES
                        (%s  , %s  ); """, [p_id, t_id])
    db.commit()
