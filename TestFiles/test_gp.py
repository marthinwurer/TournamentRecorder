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

    def tearDown(self):
        pass

    def test_get_player_id(self):
        self.assertEqual(self.player['id'], 1)

    def test_get_player_name(self):
        self.assertEqual(self.player['name'], 'Evan')