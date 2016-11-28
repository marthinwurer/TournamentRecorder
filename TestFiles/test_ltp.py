"""
This file tests the listTournamentPlayers (ltp) method of the API
Author: TangentTally
"""
import unittest
import sys
sys.path.insert(0, "../src")
import tr_api

done = False

def setUpHelper(self):
    global done
    tr_api.addPlayer(2, 1)
    tr_api.addPlayer(4, 1)
    done = True

class Test_Ltp(unittest.TestCase):

    def setUp(self):
        if done is False:
            setUpHelper(self)
        self.topdict = tr_api.listTournamentPlayers(1)
        self.topdict2 = tr_api.listTournamentPlayers(2)
        self.topdict3 = tr_api.listTournamentPlayers(12345678910)

    def tearDown(self):
        pass

    def test_player1_id(self):
        self.assertEqual(self.topdict.get('rows')[0].get('id'), 3)

    def test_player1_name(self):
        self.assertEqual(self.topdict.get('rows')[0].get('name'), 'Brown')

    def test_player2_id(self):
        self.assertEqual(self.topdict.get('rows')[1].get('id'), 1)

    def test_player2_name(self):
        self.assertEqual(self.topdict.get('rows')[1].get('name'), 'Ben')

    def test_player3_id(self):
        self.assertEqual(self.topdict.get('rows')[2].get('id'), 2)

    def test_player3_name(self):
        self.assertEqual(self.topdict.get('rows')[2].get('name'), 'Jon')


    def test_fail_no_players_in_tournament(self):
        self.assertEqual(len(self.topdict2.get('rows')), 0)

    # no error code when there is no tournament
    def test_fail_no_tournament(self):
       self.assertFalse(self.topdict3.get('outcome'))