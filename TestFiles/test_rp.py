"""
This file tests the removePlayer (rp) method of the API
Author: TangentTally
"""
import unittest
import sys
sys.path.insert(0, "../src")
import tr_api

done = False

def setUpHelper(self):
    global done
    tr_api.removePlayer(1, 1)
    tr_api.removePlayer(2, 1)
    tr_api.createTournament("Boston", 20)
    tr_api.addPlayer(1, 3)
    tr_api.addPlayer(2, 3)
    tr_api.addPlayer(3, 3)
    tr_api.addPlayer(4, 3)
    tr_api.addPlayer(5, 3)
    tr_api.startTournament(3)
    tr_api.setMatchResults(1, 1, 0, 0)
    tr_api.removePlayer(12, 3)
    done = True

class Test_Rp(unittest.TestCase):

    def setUp(self):
        if done is False:
            setUpHelper(self)
        self.topdict = tr_api.listTournamentPlayers(1)
        self.topdict2 = tr_api.removePlayer(10, 1)
        self.topdict3 = tr_api.removePlayer(1, 10)
        self.topdict4 = tr_api.removePlayer(1, 1)

    def tearDown(self):
        pass

    def test_if_players_are_removed(self):
        self.assertEqual(len(self.topdict.get('rows')), 1)
    #
    # def test_fail_no_player(self):
    #     self.assertFalse(self.topdict2.get('outcome'))

    def test_fail_no_tournament(self):
        self.assertFalse(self.topdict3.get('outcome'))
    #
    # def test_fail_player_already_removed(self):
    #     self.assertFalse(self.topdict4.get('outcome'))

    def test_if_players_are_dropped(self):
        tr_api.removePlayer(12, 3)
        self.topdict5 = tr_api.listTournamentPlayers(3)
        self.assertEqual(self.topdict5.get('rows')[0].get('dropped'), 1)