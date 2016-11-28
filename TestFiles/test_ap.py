"""
This file tests the addPlayer (ap) method of the API
Author: TangentTally
"""
import unittest
import sys
sys.path.insert(0, "../src")
import tr_api

done = False

def setUpHelper(self):
    global done
    tr_api.addPlayer(1, 1)
    tr_api.addPlayer(3, 1)
    tr_api.addPlayer(5, 1)
    done = True

class Test_Ap(unittest.TestCase):

    def setUp(self):
        if done is False:
            setUpHelper(self)
        self.topdict = tr_api.listTournamentPlayers(1)
        self.topdict2 = tr_api.addPlayer(10, 1)
        self.topdict3 = tr_api.addPlayer(1, 10)

    def tearDown(self):
        pass

    def test_player1_id(self):
        self.assertEqual(self.topdict.get('rows')[0].get('id'), 1)

    def test_player1_name(self):
        self.assertEqual(self.topdict.get('rows')[0].get('name'), 'Evan')

    def test_player2_id(self):
        self.assertEqual(self.topdict.get('rows')[1].get('id'), 2)

    def test_player2_name(self):
        self.assertEqual(self.topdict.get('rows')[1].get('name'), 'Will')

    def test_player3_id(self):
        self.assertEqual(self.topdict.get('rows')[2].get('id'), 3)

    def test_player3_name(self):
        self.assertEqual(self.topdict.get('rows')[2].get('name'), 'Brown')

    def test_fail_player_does_not_exist(self):
        self.assertFalse(self.topdict2.get('outcome'))

    def test_fail_tournament_does_not_exist(self):
        self.assertFalse(self.topdict3.get('outcome'))
