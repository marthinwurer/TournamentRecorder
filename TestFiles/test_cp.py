"""
This file tests the add player (ap) method of the API
Author: TangentTally
"""
import unittest
import sys
sys.path.insert(0, '/home/red1717/PycharmProjects/TournamentRecorder/src')
import tr_api


class TestAp(unittest.TestCase):
    def setUp(self):
        pass
        #self.topdict = tr_api.listPlayers()

    def tearDown(self):
        pass

    def test_player_not_in_db(self):
        self.topdict = tr_api.listPlayers()
        self.assertEqual(len(self.topdict.get('rows')), 4)

    def test_add_player(self):
    #     tr_api.createPlayer(5, 'Brown')
         self.topdict = tr_api.listPlayers()
         self.assertEqual(len(self.topdict.get('rows')), 5)

    # def test_new_player_id(self):
    #     self.topdict = tr_api.listPlayers()
    #     self.assertEqual(self.topdict.get('rows')[4].get('id'), 5)
    #
    # def test_new_player_name(self):
    #     self.topdict = tr_api.listPlayers()
    #     self.assertEqual(self.topdict.get('rows')[4].get('name'), 'Brown')