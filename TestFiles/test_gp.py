"""
This file tests the get player info (gp) method of the API
Author: TangentTally
"""
import unittest
import sys
sys.path.insert(0, "../src")
import tr_api


class TestGp(unittest.TestCase):

    def setUp(self):
        self.player = tr_api.getPlayer(1)
        self.player2 = tr_api.getPlayer(3)
        self.player3 = tr_api.getPlayer(-1)

    def tearDown(self):
        pass

    def test_get_player_id(self):
        self.assertEqual(self.player['id'], 1)

    def test_get_player_name(self):
        self.assertEqual(self.player['name'], 'Evan')

    def test_get_player2_id(self):
        self.assertEqual(self.player2['id'], 3)

    def test_get_player2_name(self):
        self.assertEqual(self.player2['name'], 'Will')

    def test_fail_gp_player_nonexist(self):
        self.assertFalse(self.player3.get('outcome'))

    def test_fail_gp_error_message(self):
        self.assertEqual(self.player3.get('reason'), 'Player does not exist')
