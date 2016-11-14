"""
This file sets up the database for the main client
Author: TangentTally
"""
import MySQLdb
import MySQLdb.cursors
import json


def dbreset( config ):
    db = MySQLdb.connect(config['dbserver'], config['dbusername'],
                            config['dbpassword'],
                            cursorclass=MySQLdb.cursors.DictCursor)

    curs = db.cursor()
    curs.execute('DROP DATABASE IF EXISTS ' + config['dbname'] + ';')
    db.commit()
    curs.execute('CREATE DATABASE ' + config['dbname'] + ';')
    curs.execute('USE ' + config['dbname'] + ';')
    db.commit()
    curs.execute("""CREATE TABLE player(
                        id bigint NOT NULL,
                        name varchar(30),
                        wins int,
                        losses int,
                        draws int,
                        PRIMARY KEY (id)
                        );""")
    db.commit()
    curs.execute("""CREATE TABLE tournament(
                        id int NOT NULL AUTO_INCREMENT,
                        name varchar(20),
                        max_rounds int,
                        start_date date,
                        end_date date,
                        PRIMARY KEY (id)
                        );""")
    db.commit()
    curs.execute("""CREATE TABLE round(
                        id int NOT NULL AUTO_INCREMENT,
                        t_id int NOT NULL,
                        number int,
                        start_date datetime,
                        end_date datetime,
                        PRIMARY KEY (id),
                        FOREIGN KEY(t_id) REFERENCES tournament(id)
                        );""")
    db.commit()
    curs.execute("""CREATE TABLE tournament_player(
                        id int NOT NULL AUTO_INCREMENT,
                        t_id int NOT NULL,
                        p_id bigint NOT NULL,
                        dropped int,
                        PRIMARY KEY (id),
                        FOREIGN KEY(t_id) REFERENCES tournament(id),
                        FOREIGN KEY(p_id) REFERENCES player(id)
                        );""")
    db.commit()
    curs.execute("""CREATE TABLE t_match(
                        id int NOT NULL AUTO_INCREMENT,
                        r_id int NOT NULL,
                        p1_id int NOT NULL,
                        p2_id int,
                        table_number int NOT NULL,
                        p1_wins int,
                        p2_wins int,
                        draws int,
                        PRIMARY KEY (id),
                        FOREIGN KEY(r_id) REFERENCES round(id),
                        FOREIGN KEY(p1_id) REFERENCES tournament_player(id),
                        FOREIGN KEY(p2_id) REFERENCES tournament_player(id)
                        );""")
    db.commit()
    # this function finds the standing of the given player
    curs.execute("""CREATE FUNCTION standing( player_id int )
                    RETURNS int
                    NOT DETERMINISTIC
                    BEGIN
                        DECLARE ret_val int;
                        SELECT 
                            ( SELECT COUNT(*) * 3 
                            FROM t_match
                            WHERE
                                (p1_id = player_id AND p1_wins > p2_wins) 
                                OR
                                (p2_id = player_id AND p2_wins > p1_wins)
                            )
                        +
                            ( SELECT COUNT(*)
                            FROM t_match
                            WHERE (p1_id = player_id OR p2_id = player_id)
                                AND
                                p1_wins = p2_wins
                            )
                        INTO ret_val;
                        RETURN ret_val;
                    END;""")
    db.commit()





def main():
    config = {}
    with open("config.json") as file:
        config = json.load(file)

    confirm = input("Are you sure you want to reset the database '" + config['dbname'] + "'? This will delete ALL INFORMATION (Y/n) ")
    if confirm.upper() == 'Y':
        dbreset(config)
    else:
        print("reset canceled")



if __name__ == "__main__":
    main()
