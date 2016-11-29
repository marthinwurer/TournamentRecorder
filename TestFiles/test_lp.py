"""
This file tests the list players (lp) method of the API
Author: TangentTally
"""
import unittest
import sys
sys.path.insert(0, "../src")
import tr_api


class TestLp(unittest.TestCase):

    def setUp(self):
        self.topdict = tr_api.listPlayers()

    def tearDown(self):
        pass

    #checks to see if theyre are players returned
    def test_key_in_dict(self):
        self.assertTrue(self.topdict.keys())

    def test_number_of_players(self):
        self.assertEqual(len(self.topdict.get('rows')), 5)

    def test_player1_id(self):
        self.assertEqual(self.topdict.get('rows')[0].get('id'), 1)

    def test_player1_name(self):
        self.assertEqual(self.topdict.get('rows')[0].get('name'), 'Evan')

    def test_player3_id(self):
        self.assertEqual(self.topdict.get('rows')[2].get('id'), 3)

    def test_player3_name(self):
        self.assertEqual(self.topdict.get('rows')[2].get('name'), 'Will')
