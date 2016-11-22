"""
This file holds the API for the client side. It does all of the requests, 
as well as translating the server's responses.
Author: TangentTally
"""
import requests
import json

config = {}
with open("config.json") as file:
    config = json.load(file)

server_name = config['clientserver']

def sendRequest(function, params):
    r = requests.post('http://' + server_name + '/tr-api/' + function, 
            json=params)
    return r.json()

def addPlayer(p_id, t_id):
    """
        Add a player to the given tournament. Only works if the tournament has not been 
        started.
        :returns {outcome}
    """
    return sendRequest('addPlayer', {'p_id': p_id, 't_id': t_id})

def createPlayer(DCI, name):
    """
    Creates a new player with the given DCI # and name.
    Fails if the DCI # already exists.
    :param DCI:
    :param name:
    :return: outcome
    """
    return sendRequest('createPlayer', {'DCI': DCI, 'name': name})

def createTournament(name, max_rounds):
    """
    Creates a new tournament with the given name and a maximum number of rounds
    :param name:
    :param max_rounds:
    :return: outcome
    """
    return sendRequest('createTournament', {'name': name, 'max_rounds': max_rounds})

def finishRound(r_id):
    """
    Finishes the given round
    Fails if the round does not exist, if the round is already finished, or if
    there are matches in progress.
    :param r_id:
    :returns outcome
    """
    return sendRequest('finishRound', {'r_id': r_id})

def generatePairings(t_id):
    """
        Generate the pairings. 
        Only works if there are no rounds in progress for the tournament and 
        the tournament is not finished.
        :returns outcome
    """
    return sendRequest('generatePairings', {'t_id': t_id})

def getPlayer(p_id):
    """
    Returns the information for the given player.
    {outcome, name, id}
    :param p_id:
    :return: {outcome, name, id}
    """
    return sendRequest('getPlayer', {'p_id': p_id})

def listPlayers():
    """
    :returns:
    {outcome: true/false,
     rows:[{id, name }]}
    """
    return sendRequest('listPlayers', {})

def listTournaments(sort_on, filter_types):
    """
    :returns:
    {outcome: true/false,
     rows:[{id, name, num_players, start_date, end_date}]}
    """
    return sendRequest('listTournaments', {'sort_on': sort_on, 'filter_types': filter_types})

def listTournamentPlayers(t_id):
    """
    :param t_id:
    :return:
    {outcome:
     rows:[
        { id, p_id, name, standing, dropped (None if not dropped, 1 if dropped) }]
    }
    """
    return sendRequest('listTournamentPlayers', {'t_id': t_id})

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
    return sendRequest('matchList', {'r_id': r_id})

def removePlayer(p_id, t_id):
    """
        Only do this if the player has no outstanding match results.

        If the tournament has not started, the tournament player is deleted instead of being
        set to dropped.

        :returns outcome
    """
    return sendRequest('removePlayer', {'p_id': p_id, 't_id': t_id})

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
    return sendRequest('roundList', {'t_id': t_id})

def searchPlayers(partial_name):
    """
    Look for players whose name contains the partial name
    :param partial_name:
    :return:
    {outcome: true/false,
     rows:[{id, name }]}
    """
    return sendRequest('searchPlayers', {'partial_name': partial_name})

def setMatchResults(m_id, p1_wins, p2_wins, draws):
    """
        Sets the results of a match.
        Only works if the round is not finished.
    """
    return sendRequest('setMatchResults', {'m_id': m_id, 'p1_wins': p1_wins, 
                                            'p2_wins': p2_wins, 'draws': draws})

def startTournament(t_id):
    """
        Start a tournament. 
        Only works if the tournament has not been started yet.
    """
    return sendRequest('startTournament', {'t_id': t_id})


