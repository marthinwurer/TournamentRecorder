"""
This file tests the createTournament (ct) method of the API
Author: TangentTally
"""
import unittest
import sys
sys.path.insert(0, "../src")
import tr_api

count = 0

def setUpHelper(self):
    global count
    count = count + 1

class Test_Ltp(unittest.TestCase):

    def setUp(self):
        if count == 0:
            self.topdict = tr_api.createTournament('Java Sucks', 10)
        elif count == 1:
            self.topdict2 = tr_api.createTournament('Test', 5)
        elif count == 2:
            self.topdict3 = tr_api.createTournament('abc', 10)
        elif count == 3:
            self.topdict4 = tr_api.createTournament('Tset', -1)
        setUpHelper(self)

    def tearDown(self):
        pass

    def test_tournament_1(self):
        self.assertTrue(self.topdict.get('outcome'))

    def test_tournament_2(self):
        self.assertTrue(self.topdict2.get('outcome'))


    # due to all the parameter checks being done in the GUI testing arguments
    # that should result in an outcome of false cannot be done here
    # def test_tournament_3(self):
    #     self.assertFalse(self.topdict3.get('outcome'))
    #
    # def test_tournament_4(self):
    #     self.assertFalse(self.topdict4.get('outcome'))