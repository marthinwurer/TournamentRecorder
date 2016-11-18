"""
This file tests to make sure the database is empty
Author: TangentTally
"""
import unittest
import sys
sys.path.insert(0, "../src")
import tr_api

class Test_Db_Empty(unittest.TestCase):

    def setUp(self):
        self.topdict = tr_api.listPlayers()
        self.topdict2 = tr_api.listTournaments(None, None)

    def tearDown(self):
        pass

    def test_no_players(self):
        self.assertEqual(len(self.topdict.get('rows')), 0)

    def test_no_tournaments(self):
        self.assertEqual(len(self.topdict2.get('rows')), 0)
