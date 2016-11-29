"""
This file tests the search player *partial match* (sp) method of the API
Author: TangentTally
"""
import unittest
import sys
sys.path.insert(0, "../src")
import tr_api


class TestSp(unittest.TestCase):

    def setUp(self):
        tr_api.createPlayer(5, 'Brown')
        self.topdict = tr_api.searchPlayers('E')
        self.topdict2 = tr_api.searchPlayers('Evan')
        self.topdict3 = tr_api.searchPlayers('B')
        self.topdict4 = tr_api.searchPlayers('-1')

    def tearDown(self):
        pass

    def test_player_id(self):
        self.assertEqual(self.topdict.get('rows')[0].get('id'), 1)

    def test_player_name(self):
        self.assertEqual(self.topdict.get('rows')[0].get('name'), 'Evan')

    def test_full_match_id(self):
        self.assertEqual(self.topdict2.get('rows')[0].get('id'), 1)

    def test_full_match_name(self):
        self.assertEqual(self.topdict2.get('rows')[0].get('name'), 'Evan')

    def test_multiple_matches_id(self):
        self.assertEqual(self.topdict3.get('rows')[0].get('id'), 2)
        self.assertEqual(self.topdict3.get('rows')[1].get('id'), 5)

    def test_multiple_matches_name(self):
        self.assertEqual(self.topdict3.get('rows')[0].get('name'), 'Ben')
        self.assertEqual(self.topdict3.get('rows')[1].get('name'), 'Brown')

    def test_no_player(self):
        self.assertEqual(len(self.topdict4.get('rows')), 0)
