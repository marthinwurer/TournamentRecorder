"""
This file holds the API for the client side. It does all of the requests, 
as well as translating the server's responses.
Author: Benjamin Maitland
"""
import requests

#r = requests.post('http://localhost:5000/tr-api/',
#        json={'key':'value'})
#print( r.json())

def addPlayer(p_id, t_id):
    pass

def createPlayer(DCI, name):
    pass

def createTournament(name, max_rounds):
    pass

def finishRound(r_id):
    pass

def generatePairings(t_id):
    pass

def getPlayer(p_id):
    pass

def listPlayers():
    pass

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