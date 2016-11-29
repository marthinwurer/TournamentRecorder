# TournamentRecorder
By Team TangentTally 37

The first step for installation is to download the client from the git repo. If you can see this message locally, you're good.

At the moment, the server only runs on Ubuntu Linux. This has been tested on 14.04 and 16.04 lts. If you cannot get the server running, you can connect to one at:
    
    ttdbserver.student.rit.edu:5000

The client runs on both windows and linux.

The server will need a MySQL server running. On Ubuntu, this can be installed with:
    
    $ sudo apt install mysql-server

To run both the server and client, a python virtal environment must be set up. This is done with virtualenv. Installation instructions are [here](https://virtualenv.pypa.io/en/stable/installation/).

Once virtualenv is set up, you can then create the virtual environment.

    $ virtualenv -p /path/to/python3.5 venv

To begin using the virtual environment, it needs to be activated:

    $ source venv/bin/activate
	
	For Window Users:
	virtualenv provides a .bat script to activate the virtualenv. A Windows User
	will run the following instead:
	
	$ venv/Scripts/activate

If you are done working in the virtual environment for the moment, you can deactivate it:

    $ deactivate
	
	For Window Users:
	virtualenv provides a .bat script to activate the virtualenv. A Windows User
	will run the following instead:
	
	$ venv/Scripts/deactivate

The headers needed for all libraries to work are obtained by:

    $ sudo apt-get install libmysqlclient-dev
    $ sudo apt-get install python3-dev

To install all of the required libraries, activate the virtual environment, then run:

    $ pip install -r requirements.txt
	
	This commands downloads all the requirement packages listed in requirements.txt
	For Windows users, the referenced mysql-client in the file does not play well.
	Thus you may delete it if is an issue 

Configure the client and server by creating a config.json file. A default one is:

    {
      "dbserver": "localhost",
      "dbusername": "root",
      "dbpassword": "root",
      "clientserver": "ttdbserver.student.rit.edu:5000"
    }

dbserver is the database server, dbusername and dbpassword are the username and password, and clientserver is the server that the client will attempt to connect to.

To first set up the database, run:
    
    $ python ./src/dbsetup.py

Our database is normalized to First Normal Form.

To start the server, export the path to the server python file, and then run it.

    $ export FLASK_APP=./src/server.py
    $ flask run

To run the client, modify the connection address, and then run the client.

    $ python ./src/client.py

The list of commands for the client can be found by running the command 'help' in the shell. 

Don't worry, our final release will have a GUI client. This is just a proof of concept for our API and server. We stil have some core business logic that needs to be implemented.

To reboot the database server, log in to the database server, and run:

	$ screen -R

to attatch to the screen session. Then restart the server (Ctrl-C to stop it, ./run.sh to restart it). After the server has been restarted, hit Ctrl-a then d to disconnect from the screen session and leave the server running in the background.

To run unit tests on the program use localhost as the server and follow the order listed in Testing.txt
    $ python -m unittest test_(filename).py

# GUI Client

You can run the GUI client by running the following command when the virtual environment is set up.

    python ./src/clientGUI.py

To create a tournament, go under Tournament -> Create Tournament
To create a player, go under Players -> Create Player
To list the tournaments, go under Tournament -> List Tournament
To add players to a tournament, select a tournament from the list and then select players to add from the menus that appear. You may need to refresh the list of active players.
To start a tournament, select start tournament from the list of tournaments.
To view a round's matches, select the round in the round window.
To finish the round, go under Rounds -> Finish Round.
To generate pairings for the next round, go under Rounds -> Generate Pairings