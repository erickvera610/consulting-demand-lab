import unittest
from core import forecast,mae,run
class Tests(unittest.TestCase):
    def test_linear(self):self.assertAlmostEqual(forecast(list(range(28)),1)[0],28)
    def test_mae(self):self.assertEqual(mae([1,3],[2,5]),1.5)
    def test_baseline(self):r=run({'noise':0});self.assertLess(r['mae'],r['baseline_mae'])
    def test_short(self):
        with self.assertRaises(ValueError):forecast([1],1)
