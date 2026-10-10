import unittest
from evaluation import evaluate, predict, run_evaluation

class EvaluationTests(unittest.TestCase):

    def test_final_holdout_not_used_for_selection(self):
        data = [100 + 0.4 * i + i % 7 for i in range(168)]
        a = evaluate(data, 7, 28)
        data[-28:] = [999] * 28
        b = evaluate(data, 7, 28)
        self.assertEqual(a['model_selection'], b['model_selection'])
        self.assertEqual(a['predicted'], b['predicted'])

    def test_public_dataset(self):
        r = run_evaluation({'dataset': 'airpassengers'})
        self.assertEqual(r['test_days'], 12)
        self.assertEqual(r['train_days'], 132)

    def test_seasonal_naive(self):
        self.assertEqual(predict([1, 2] * 4, 3, 2, 'seasonal_naive'), [1, 2, 1])
