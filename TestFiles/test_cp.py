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
        self.topdict = tr_api.listPlayers()

    def tearDown(self):
        pass

    #checks to see that there are no players in db
    def test_player_not_in_db(self):
        try:
            self.assertEqual(self.topdict.get('rows')[0].get('id'), -1)
        except IndexError:
            self.assertTrue(True)

    def test_add_player(self):
        tr_api.createPlayer(1, 'Evan')
        self.topdict = tr_api.listPlayers()
        self.assertEqual(len(self.topdict.get('rows')), 1)

    def test_new_player_id(self):
        self.assertEqual(self.topdict.get('rows')[0].get('id'), 1)

    def test_new_player_name(self):
        self.assertEqual(self.topdict.get('rows')[0].get('name'), 'Evan')

    def test_fail_cp_same_id(self):
        self.topdict2 = tr_api.createPlayer(1, "Fail")
        self.assertFalse(self.topdict2.get('outcome'))

    def test_fail_cp_error_message(self):
        self.topdict3 = tr_api.createPlayer(1, "Fail2")
        self.assertEqual(self.topdict3.get('reason'), '')
