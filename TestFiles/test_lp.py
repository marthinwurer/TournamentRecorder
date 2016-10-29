import unittest
import sys
sys.path.insert(0, '/home/red1717/PycharmProjects/TournamentRecorder/src')
import tr_api


class TestLp(unittest.TestCase):

    def setUp(self):
        self.topdict = tr_api.listPlayers()

    def tearDown(self):
        pass

    def test_key_in_dict(self):
        self.assertFalse(not self.topdict.keys())

    def test_player1_id(self):
        self.assertEqual(self.topdict.get('rows')[0].get('id'), 1)

    def test_player1_name(self):
        self.assertEqual(self.topdict.get('rows')[0].get('name'), 'Evan')

    def test_player3_id(self):
        self.assertEqual(self.topdict.get('rows')[2].get('id'), 3)

        def test_player1_name(self):
            self.assertEqual(self.topdict.get('rows')[2].get('name'), 'Will')