"""
This file tests to make sure a tournament with no players, rounds
or matches retruns the proper flags
Author: TangentTally
"""
import unittest
import sys
sys.path.insert(0, "../src")
import tr_api


class Test_Empty_Tournament(unittest.TestCase):

    def setUp(self):
        self.topdict = tr_api.listTournaments(None, None)
        self.topdict2 = tr_api.listTournamentPlayers(1)

    def tearDown(self):
        pass

    def test_tournament_id(self):
        self.assertEqual(self.topdict.get('rows')[0].get('id'), 1)

    def test_tournament_name(self):
        self.assertEqual(self.topdict.get('rows')[0].get('name'), 'Java Sucks')

    def test_tournament_numPlayers(self):
        self.assertEqual(self.topdict.get('rows')[0].get('num_players'), 0)

    def test_tournament_startDate(self):
        self.assertEqual(self.topdict.get('rows')[0].get('start_date'), None)

    def test_tournament_endDate(self):
        self.assertEqual(self.topdict.get('rows')[0].get('end_date'), None)

    def test_no_players_in_tournament(self):
        self.assertEqual(len(self.topdict2.get('rows')), 0)