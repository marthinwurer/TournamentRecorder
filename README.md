# TournamentRecorder
The first step for installation is to download the client from the git repo.

Once that is done, a python virtal environment must be set up. This is done with virtualenv. Installation instructions are [here][https://virtualenv.pypa.io/en/stable/installation/].

Once virtualenv is set up, you can then create the virtual environment.
    $ virtualenv -p /path/to/python3.5 venv

To begin using the virtual environment, it needs to be activated:
    $ source venv/bin/activate

If you are done working in the virtual environment for the moment, you can deactivate it:
    $ deactivate

To install all of the required libraries, activate the virtual environment, then run:
    $ pip install -r requirements.txt

Configure the server by modifying the database hostname, username, and password in the server file.
To start the server, export the path to the server python file, and then run it.
    $ export FLASK_APP=./src/server.py
    $ flask run

To run the client, modify the connection address, and then run the client.
    $ python ./src/client.py
