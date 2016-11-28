"""
This file tests the listTournaments (lt) method of the API
Author: TangentTally
"""
import unittest
import sys
sys.path.insert(0, "../src")
import tr_api


class TestLt(unittest.TestCase):

    def setUp(self):
        self.topdict = tr_api.listTournaments(None, None)

    def tearDown(self):
        pass

    def test_key_in_dict(self):
        self.assertFalse(not self.topdict.keys())

    def test_tournament1_id(self):
        self.assertEqual(self.topdict.get('rows')[0].get('id'), 1)

    def test_tournament1_name(self):
        self.assertEqual(self.topdict.get('rows')[0].get('name'), '1')

    def test_tournament1_no_players(self):
        self.assertEqual(self.topdict.get('rows')[0].get('num_players'), 0)

    # def test_tournament1_3_players(self):
    #     #tr_api.addPlayer(1, 1)
    #     #tr_api.addPlayer(2, 1)
    #     #tr_api.addPlayer(3, 1)
    #     self.topdict = tr_api.listTournaments(None, None)
    #     self.assertEqual(self.topdict.get('rows')[0].get('num_players'), 3)
    #
    # def test_new_tournament_id(self):
    #     self.assertEqual(self.topdict.get('id'), 1)
    #
    # def test_new_tournament_max_rounds(self):
    #     self.assertEqual(self.topdict.get('max_rounds'), 10)
    #
    # def test_new_tournament_name(self):
    #     self.assertEqual(self.topdict.get('name'), 'Test')
    #
    # def test_new_tournament_same_name_id(self):
    #     self.assertEqual(self.topdict2.get('id'), 2)
    #
    # def test_new_tournament_same_name_max_rounds(self):
    #     self.assertEqual(self.topdict2.get('max_rounds'), 5)
    #
    # def test_new_tournament_same_name_name(self):
    #     self.assertEqual(self.topdict2.get('name'), 'Test')
    #
    # def test_fail_tournament_invalid_id(self):
    #     self.assertFalse(self.topdict3.get('outcome'))
    #
    # def test_fail_tournament_invalid_name(self):
    #     self.assertFalse(self.topdict4.get('outcome'))
