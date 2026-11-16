import copy
import datetime as dt
import unittest
from forecast_history import build_features

class HistoryTests(unittest.TestCase):
    def setUp(self):
        self.rows=[{'date':str(dt.date(2012,1,1)+dt.timedelta(days=i)), 'count':i+1} for i in range(14)]

    def test_known_lags_and_means(self):
        x=build_features('2012-01-15', self.rows)
        self.assertEqual(x[5:], [14.,8.,11.,7.5])

    def test_order_independent_and_no_mutation(self):
        before=copy.deepcopy(self.rows)
        self.assertEqual(build_features('2012-01-15',self.rows),build_features('2012-01-15',self.rows[::-1]))
        self.assertEqual(self.rows,before)

    def test_target_and_future_rejected(self):
        for date in ['2012-01-15','2012-01-16']:
            rows=copy.deepcopy(self.rows);rows[-1]['date']=date
            with self.assertRaises(ValueError):build_features('2012-01-15',rows)

    def test_missing_duplicate_and_stale_days(self):
        for rows in [self.rows[:-1],self.rows[:-1]+[self.rows[0]],
                     [{'date':'2011-12-31','count':1}]+self.rows[1:]]:
            with self.assertRaises(ValueError):build_features('2012-01-15',rows)

    def test_invalid_counts_and_dates(self):
        for value in [True, -1, float('nan'), float('inf'), '3']:
            rows=copy.deepcopy(self.rows);rows[0]['count']=value
            with self.assertRaises(ValueError):build_features('2012-01-15',rows)
        for date in ['20120115','bad',None,'2011-01-10']:
            with self.assertRaises(ValueError):build_features(date,self.rows)
