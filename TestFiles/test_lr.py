"""
This file tests the listRound (lr) method of the API
Author: TangentTally
"""
import unittest
import sys
sys.path.insert(0, "../src")
import tr_api
import time

done = False

def setUpHelper(self):
    global done
    done = True

class Test_Rp(unittest.TestCase):

    def setUp(self):
        if done is False:
            setUpHelper(self)
            print(tr_api.roundList(4))
        self.topdict = tr_api.roundList(4)

    def tearDown(self):
        pass

    def test_round_finished(self):
        self.assertTrue(self.topdict.get('outcome'))

    def test_id(self):
        self.assertEqual(self.topdict.get('rows')[0].get('id'), 3)

    def test_round_number(self):
        self.assertEqual(self.topdict.get('rows')[0].get('number'), 1)

    # due to time the start and end date cannot be checked
    # def test_tournament3_start_date(self):
    #     self.assertEqual(self.topdict.get('rows')[0].get('start_date'), time.strftime("%Y-%m-%d") + time.strftime("%H:%M:%S"))
    #
    # def test_tournament3_end_date(self):
    #     self.assertEqual(self.topdict.get('rows')[0].get('end_date'), time.strftime("%Y-%m-%d") + time.strftime("%H:%M:%S"))