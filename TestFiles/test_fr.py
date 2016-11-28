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

    def tearDown(self):
        pass
