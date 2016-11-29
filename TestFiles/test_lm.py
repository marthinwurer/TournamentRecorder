"""
This file tests the listMatches (lm) method of the API
Author: TangentTally
"""
import unittest
import sys
sys.path.insert(0, "../src")
import tr_api

done = False

def setUpHelper(self):
    global done
    done = True

class Test_Rp(unittest.TestCase):

    def setUp(self):
        if done is False:
            setUpHelper(self)
        self.topdict = tr_api.matchList(3)

    def tearDown(self):
        pass

    def test_success(self):
        self.assertTrue(self.topdict.get('outcome'))

    def test_round1_match1_id(self):
        self.assertEqual(self.topdict.get('rows')[0].get('id'), 6)

    def test_round1_match1_player1_table_number(self):
        self.assertEqual(self.topdict.get('rows')[0].get('table_number'), 1)

    def test_round1_match1_player1_id(self):
        self.assertEqual(self.topdict.get('rows')[0].get('p1_id'), 23)

    def test_round1_match1_player1_name(self):
        self.assertEqual(self.topdict.get('rows')[0].get('p1_name'), 'Brown')

    def test_round1_match1_player2_id(self):
        self.assertEqual(self.topdict.get('rows')[0].get('p2_id'), 24)

    def test_round1_match1_player2_name(self):
        self.assertEqual(self.topdict.get('rows')[0].get('p2_name'), 'Green')

    def test_round1_match1_player1_wins(self):
        self.assertEqual(self.topdict.get('rows')[0].get('p1_wins'), 2)

    def test_round1_match1_player2_wins(self):
        self.assertEqual(self.topdict.get('rows')[0].get('p2_wins'), 1)

    def test_round1_match1_draws(self):
        self.assertEqual(self.topdict.get('rows')[0].get('draws'), 0)

    def test_round1_match2_id(self):
        self.assertEqual(self.topdict.get('rows')[1].get('id'), 7)

    def test_round1_match2_player1_table_number(self):
        self.assertEqual(self.topdict.get('rows')[1].get('table_number'), 2)

    def test_round1_match2_player1_id(self):
        self.assertEqual(self.topdict.get('rows')[1].get('p1_id'), 25)

    def test_round1_match2_player1_name(self):
        self.assertEqual(self.topdict.get('rows')[1].get('p1_name'), 'Red')

    def test_round1_match2_player2_id(self):
        self.assertEqual(self.topdict.get('rows')[1].get('p2_id'), 26)

    def test_round1_match2_player2_name(self):
        self.assertEqual(self.topdict.get('rows')[1].get('p2_name'), 'Blue')

    def test_round1_match2_player1_wins(self):
        self.assertEqual(self.topdict.get('rows')[1].get('p1_wins'), 1)

    def test_round1_match2_player2_wins(self):
        self.assertEqual(self.topdict.get('rows')[1].get('p2_wins'), 2)

    def test_round1_match2_draws(self):
        self.assertEqual(self.topdict.get('rows')[1].get('draws'), 0)

    def test_round1_match3_id(self):
        self.assertEqual(self.topdict.get('rows')[2].get('id'), 8)

    def test_round1_match3_player1_table_number(self):
        self.assertEqual(self.topdict.get('rows')[2].get('table_number'), 3)

    def test_round1_match3_player1_id(self):
        self.assertEqual(self.topdict.get('rows')[2].get('p1_id'), 19)

    def test_round1_match3_player1_name(self):
        self.assertEqual(self.topdict.get('rows')[2].get('p1_name'), 'Evan')

    def test_round1_match3_player2_id(self):
        self.assertEqual(self.topdict.get('rows')[2].get('p2_id'), 20)

    def test_round1_match3_player2_name(self):
        self.assertEqual(self.topdict.get('rows')[2].get('p2_name'), 'Ben')

    def test_round1_match3_player1_wins(self):
        self.assertEqual(self.topdict.get('rows')[2].get('p1_wins'), 2)

    def test_round1_match3_player2_wins(self):
        self.assertEqual(self.topdict.get('rows')[2].get('p2_wins'), 0)

    def test_round1_match3_draws(self):
        self.assertEqual(self.topdict.get('rows')[2].get('draws'), 1)

    def test_round1_match4_id(self):
        self.assertEqual(self.topdict.get('rows')[3].get('id'), 9)

    def test_round1_match4_player1_table_number(self):
        self.assertEqual(self.topdict.get('rows')[3].get('table_number'), 4)

    def test_round1_match4_player1_id(self):
        self.assertEqual(self.topdict.get('rows')[3].get('p1_id'), 21)

    def test_round1_match4_player1_name(self):
        self.assertEqual(self.topdict.get('rows')[3].get('p1_name'), 'Will')

    def test_round1_match4_player2_id(self):
        self.assertEqual(self.topdict.get('rows')[3].get('p2_id'), 22)

    def test_round1_match4_player2_name(self):
        self.assertEqual(self.topdict.get('rows')[3].get('p2_name'), 'Jon')

    def test_round1_match4_player1_wins(self):
        self.assertEqual(self.topdict.get('rows')[3].get('p1_wins'), 2)

    def test_round1_match4_player2_wins(self):
        self.assertEqual(self.topdict.get('rows')[3].get('p2_wins'), 1)

    def test_round1_match4_draws(self):
        self.assertEqual(self.topdict.get('rows')[3].get('draws'), 0)
