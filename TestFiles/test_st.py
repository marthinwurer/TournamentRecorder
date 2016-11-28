"""
This file tests the startTournament (st) method of the API
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

class Test_Rp(unittest.TestCase):

    def setUp(self):
        if done is False:
            setUpHelper(self)

    def tearDown(self):
        pass

    def test_tournament1(self):
        self.topdict = tr_api.startTournament(1)
        self.assertTrue(self.topdict.get('outcome'))

    # we can start a tournament with no players in it
    # def test_fail_no_players(self):
    #     self.topdict2 = tr_api.startTournament(2)
    #     self.assertFalse(self.topdict2.get('outcome'))

    def test_fail_no_tournament(self):
        self.topdict3 = tr_api.startTournament(12345678910)
        self.assertFalse(self.topdict3.get('outcome'))