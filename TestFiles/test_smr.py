"""
This file tests the setMatchResults (smr) method of the API
Author: TangentTally
"""
import unittest
import sys
sys.path.insert(0, "../src")
import tr_api

done = False

def setUpHelper(self):
    global done
    tr_api.setMatchResults(6, 2, 1, 0)
    tr_api.setMatchResults(7, 1, 2, 0)
    tr_api.setMatchResults(8, 2, 0, 1)
    tr_api.setMatchResults(9, 2, 1, 0)
    done = True

class Test_Rp(unittest.TestCase):

    def setUp(self):
        if done is False:
            setUpHelper(self)
        self.topdict = tr_api.matchList(3)

    def tearDown(self):
        pass

    def test_round1_match1_player1_wins(self):
        self.assertEqual(self.topdict.get('rows')[0].get('p1_wins'), 2)

    def test_round1_match1_player2_wins(self):
        self.assertEqual(self.topdict.get('rows')[0].get('p2_wins'), 1)

    def test_round1_match1_draws(self):
        self.assertEqual(self.topdict.get('rows')[0].get('draws'), 0)


    def test_round1_match2_player1_wins(self):
        self.assertEqual(self.topdict.get('rows')[1].get('p1_wins'), 1)

    def test_round1_match2_player2_wins(self):
        self.assertEqual(self.topdict.get('rows')[1].get('p2_wins'), 2)

    def test_round1_match2_draws(self):
        self.assertEqual(self.topdict.get('rows')[1].get('draws'), 0)


    def test_round1_match3_player1_wins(self):
        self.assertEqual(self.topdict.get('rows')[2].get('p1_wins'), 2)

    def test_round1_match3_player2_wins(self):
        self.assertEqual(self.topdict.get('rows')[2].get('p2_wins'), 0)

    def test_round1_match3_draws(self):
        self.assertEqual(self.topdict.get('rows')[2].get('draws'), 1)


    def test_round1_match4_player1_wins(self):
        self.assertEqual(self.topdict.get('rows')[3].get('p1_wins'), 2)

    def test_round1_match4_player2_wins(self):
        self.assertEqual(self.topdict.get('rows')[3].get('p2_wins'), 1)

    def test_round1_match4_draws(self):
        self.assertEqual(self.topdict.get('rows')[3].get('draws'), 0)
