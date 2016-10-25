"""
This file sets up the database for the main client
Author: Benjamin Maitland
"""
import MySQLdb

db = MySQLdb.connect("localhost", "root", "root")





def main():
    confirm = input("Are you sure you want to reset the database? This will delete ALL INFORMATION (Y/n) ")
    if confirm == 'Y':
        curs = db.cursor()
        curs.execute('DROP DATABASE IF EXISTS TournamentRecorder;')
        db.commit()
        curs.execute('CREATE DATABASE TournamentRecorder;')
        curs.execute('USE TournamentRecorder;')
        db.commit()
        curs.execute("""CREATE TABLE player(
                            id int NOT NULL,
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
                            p_id int NOT NULL,
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
                            p2_id int NOT NULL,
                            table_number int NOT NULL,
                            p1_wins int,
                            p2_wins int,
                            draws int,
                            PRIMARY KEY (id),
                            FOREIGN KEY(r_id) REFERENCES round(id),
                            FOREIGN KEY(p1_id) REFERENCES player(id),
                            FOREIGN KEY(p2_id) REFERENCES player(id)
                            );""")
        db.commit()


if __name__ == "__main__":
    main()
