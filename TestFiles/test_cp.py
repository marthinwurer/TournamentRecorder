"""
This file tests the create player (cp) method of the API
Author: TangentTally
"""
import unittest
import sys
sys.path.insert(0, "../src")
import tr_api


class TestAp(unittest.TestCase):
    def setUp(self):
        tr_api.createPlayer(1, 'Evan')
        self.topdict = tr_api.listPlayers()
        self.topdict2 = tr_api.createPlayer(1, "Fail2")

    def tearDown(self):
        tr_api.createPlayer(2, 'Ben')
        tr_api.createPlayer(3, 'Will')
        tr_api.createPlayer(4, 'Jon')

    def test_add_player(self):
        self.assertEqual(len(self.topdict.get('rows')), 1)

    def test_new_player_id(self):
        self.assertEqual(self.topdict.get('rows')[0].get('id'), 1)

    def test_new_player_name(self):
        self.assertEqual(self.topdict.get('rows')[0].get('name'), 'Evan')

    def test_fail_cp_same_id(self):
        self.assertFalse(self.topdict2.get('outcome'))

    def test_fail_cp_error_message(self):
        self.assertEqual(self.topdict2.get('reason'), 'DCI Exists')
