"""
This file tests the listTournaments (lt) method of the API
Author: TangentTally
"""
import unittest
import sys
sys.path.insert(0, '/home/red1717/PycharmProjects/TournamentRecorder/src')
import tr_api


class TestLt(unittest.TestCase):
    def setUp(self):
        self.topdict = tr_api.listTournaments(None, None)

    def tearDown(self):
        pass

    def test_key_in_dict(self):
        self.assertFalse(not self.topdict.getKeys())

    def test_tournament1_id(self):
        self.assertEqual(self.topdict.get('rows')[0].get('id'), 1)

    def test_tournament1_name(self):
        self.assertEqual(self.topdict.get('rows')[0].get('name'), '1')

    def test_tournament1_no_players(self):
        self.assertEqual(self.topdict.get('rows')[0].get('num_players'), 0)

    def test_tournament1_3_players(self):
        #tr_api.addPlayer(1, 1)
        #tr_api.addPlayer(2, 1)
        #tr_api.addPlayer(3, 1)
        self.topdict = tr_api.listTournaments(None, None)
        self.assertEqual(self.topdict.get('rows')[0].get('num_players'), 3)