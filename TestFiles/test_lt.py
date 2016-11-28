"""
This file tests the listTournaments (lt) method of the API
Author: TangentTally
"""
import unittest
import sys
sys.path.insert(0, "../src")
import tr_api
import time


class TestLt(unittest.TestCase):

    def setUp(self):
        self.topdict = tr_api.listTournaments(None, None)

    def tearDown(self):
        pass

    def test_key_in_dict(self):
        self.assertTrue(self.topdict.keys())

    def test_success(self):
        self.assertTrue(self.topdict.get('outcome'))

    def test_tournament1_id(self):
        self.assertEqual(self.topdict.get('rows')[0].get('id'), 1)

    def test_tournament1_name(self):
        self.assertEqual(self.topdict.get('rows')[0].get('name'), 'Java Sucks')

    def test_tournament1_player_count(self):
        self.assertEqual(self.topdict.get('rows')[0].get('num_players'), 3)

    def test_tournament1_start_date(self):
        self.assertEqual(self.topdict.get('rows')[0].get('start_date'), time.strftime("%Y-%m-%d"))

    def test_tournament1_end_date(self):
        self.assertEqual(self.topdict.get('rows')[0].get('end_date'), None)

    def test_tournament3_id(self):
        self.assertEqual(self.topdict.get('rows')[2].get('id'), 3)

    def test_tournament3_name(self):
        self.assertEqual(self.topdict.get('rows')[2].get('name'), 'Boston')

    def test_tournament3_player_count_with_dropped_player(self):
        self.assertEqual(self.topdict.get('rows')[2].get('num_players'), 5)

    def test_tournament3_start_date(self):
        self.assertEqual(self.topdict.get('rows')[2].get('start_date'), time.strftime("%Y-%m-%d"))

    def test_tournament3_end_date(self):
        self.assertEqual(self.topdict.get('rows')[2].get('end_date'), None)
