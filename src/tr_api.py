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
    pass

def finishRound(r_id):
    pass

def generatePairings(t_id):
    pass

def getPlayer(p_id):
    pass

def listPlayers():
    return sendRequest('listPlayers', {})

def listTournaments(sort_on, filter_types):
    pass

def listTournamentPlayers(t_id):
    pass

def matchList(r_id):
    pass

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
