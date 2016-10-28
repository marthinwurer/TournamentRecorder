"""
This file holds the API for the client side. It does all of the requests, 
as well as translating the server's responses.
Author: Benjamin Maitland
"""
import requests

server_name = 'localhost:5000'
#server_name = 'ttdbserver.student.rit.edu:5000'

#r = requests.post('http://localhost:5000/tr-api/',
#        json={'key':'value'})
#print( r.json())
def sendRequest(function, params):
    r = requests.post('http://' + server_name + '/tr-api/' + function, 
            json=params)
    return r.json()

def addPlayer(p_id, t_id):
    return sendRequest('addPlayer', {'p_id': p_id, 't_id': t_id})

def createPlayer(DCI, name):
    return sendRequest('createPlayer', {'DCI': DCI, 'name': name})

def createTournament(name, max_rounds):
    return sendRequest('createTournament', {'name': name, 'max_rounds': max_rounds})

def finishRound(r_id):
    return sendRequest('finishRound', {'r_id': r_id})

def generatePairings(t_id):
    return sendRequest('generatePairings', {'t_id': t_id})

def getPlayer(p_id):
    return sendRequest('getPlayer', {'p_id': p_id})

def listPlayers():
    return sendRequest('listPlayers', {})

def listTournaments(sort_on, filter_types):
    return sendRequest('listTournaments', {'sort_on': sort_on, 'filter_types': filter_types})

def listTournamentPlayers(t_id):
    return sendRequest('listTournamentPlayers', {'t_id': t_id})

def matchList(r_id):
    return sendRequest('matchList', {'r_id': r_id})

def removePlayer(p_id, t_id):
    return sendRequest('removePlayer', {'p_id': p_id, 't_id': t_id})

def roundList(t_id):
    return sendRequest('roundList', {'t_id': t_id})

def searchPlayers(partial_name):
    return sendRequest('searchPlayers', {'partial_name': partial_name})

def setMatchResults(m_id, p1_wins, p2_wins, draws):
    return sendRequest('setMatchResults', {'m_id': m_id, 'p1_wins': p1_wins, 
                                            'p2_wins': p2_wins, 'draws': draws})

def startTournament(t_id):
    return sendRequest('startTournament', {'t_id': t_id})


