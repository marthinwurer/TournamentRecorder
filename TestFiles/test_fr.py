"""
This file tests the finishRound (fr) method of the API
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
        self.topdict = tr_api.finishRound(3)

    def tearDown(self):
        pass

    def test_round_finished(self):
        self.assertTrue(self.topdict.get('outcome'))