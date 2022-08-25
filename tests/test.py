import os
import sys
sys.path.insert(0, os.path.abspath( os.path.join(os.path.dirname(__file__), '../src/') ))

import unittest
from preflight.checks import *

class TestPingConnectivityCheck(unittest.TestCase):
    def test_localhost(self):
        ctx = Context()
        check = PingConnectivityCheck('LOCAL_CONN', 'localhost')
        res = check.run(ctx)
        self.assertTrue(res.passed)
        self.assertEqual(res.msg, 'Connected.')
        self.assertTrue(ctx['localhost_connected'])
    
    def test_badhost(self):
        ctx = Context()
        check = PingConnectivityCheck('LOCAL_CONN', 'badhost')
        res = check.run(ctx)
        self.assertFalse(res.passed)
        self.assertEqual(res.msg, 'Not connected.')
        self.assertFalse(ctx['badhost_connected'])

class TestCheckSequence(unittest.TestCase):
    def test_sequence_good(self):
        seq = CheckSequence()
        seq.add(PingConnectivityCheck('CHECK1', 'localhost'))
        seq.add(PingConnectivityCheck('CHECK2', 'localhost'))
        res = seq.run()
        self.assertTrue(res)
        self.assertTrue(seq.results['CHECK1'].passed)
        self.assertTrue(seq.results['CHECK2'].passed)

    def test_sequence_bad(self):
        seq = CheckSequence()
        seq.add(PingConnectivityCheck('CHECK1', 'localhost'))
        seq.add(PingConnectivityCheck('CHECK2', 'badhost'))
        res = seq.run()
        self.assertFalse(res)
        self.assertTrue(seq.results['CHECK1'].passed)
        self.assertFalse(seq.results['CHECK2'].passed)