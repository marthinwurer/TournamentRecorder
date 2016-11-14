"""
This file tests the create player (cp) method of the API
Author: TangentTally
"""
import unittest
import sys
sys.path.insert(0, '/home/red1717/PycharmProjects/TournamentRecorder/src')
import tr_api


class TestAp(unittest.TestCase):
    def setUp(self):
        self.topdict = tr_api.listPlayers()

    def tearDown(self):
        pass

    def test_player_not_in_db(self):
        try:
            self.assertEqual(self.topdict.get('rows')[4].get('id'), 5)
        except IndexError:
            self.assertTrue(True)

    def test_add_player(self):
        tr_api.createPlayer(5, 'Brown')
        self.topdict = tr_api.listPlayers()
        self.assertEqual(len(self.topdict.get('rows')), 5)

    def test_new_player_id(self):
        self.assertEqual(self.topdict.get('rows')[4].get('id'), 5)

    def test_new_player_name(self):
        self.assertEqual(self.topdict.get('rows')[4].get('name'), 'Brown')