import unittest
import re
import time

from src.utils import get_time, StopClock


class TestUtils(unittest.TestCase):
    def test_get_time(self):
        """
        Test that the time has a useful format
        """
        t = get_time()

        # should only have chars for useful file names and that do not conflict with CSV etc
        self.assertTrue(re.match("^[a-zA-Z0-9:_-]+$", t))

    def test_stop_clock(self):
        sc = StopClock()
        time.sleep(2)
        s = sc.stop()
        self.assertTrue("took" in s)
        self.assertFalse("total" in s)
        self.assertGreater(sc.get_duration(), 2)
        time.sleep(1)
        s = sc.stop()
        self.assertTrue("took" in s)
        self.assertTrue("total" in s)
        self.assertGreater(sc.get_duration(), 3)
