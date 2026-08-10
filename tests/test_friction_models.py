import unittest

import pandas as pd

from src.core.FixedTransactionCostModel import FixedTransactionCostModel
from src.core.ProportionalFrictionModel import ProportionalFrictionModel


class TestFrictionModels(unittest.TestCase):
    def setUp(self):
        self.prices = pd.DataFrame({'close': [100.0, 105.0, 110.0, 108.0, 112.0]})
        self.signals = pd.Series([1, 1, -1, -1, 0])

    def test_fixed_transaction_cost_model(self):
        model = FixedTransactionCostModel(fixed_amount=2.0)
        costs = model.calculate_friction(self.prices, self.signals)
        
        # Expected trades (shifted signals difference):
        # shifted_signals = [0, 1, 1, -1, -1]
        # diff = [NaN, 1, 0, -2, 0] -> abs filled: [0, 1, 0, 2, 0]
        # Prices: [100, 105, 110, 108, 112]
        # cost = trade_delta * (2.0 / price)
        # c0 = 0
        # c1 = 1 * (2.0 / 105.0) = 0.019047...
        # c2 = 0
        # c3 = 2 * (2.0 / 108.0) = 0.037037...
        # c4 = 0
        
        self.assertEqual(len(costs), 5)
        self.assertAlmostEqual(costs[1], 1 * (2.0 / 105.0))
        self.assertAlmostEqual(costs[3], 2 * (2.0 / 108.0))
        self.assertEqual(costs[0], 0)
        self.assertEqual(costs[2], 0)
        self.assertEqual(costs[4], 0)

    def test_proportional_friction_model(self):
        model = ProportionalFrictionModel(proportional_rate=0.001)
        costs = model.calculate_friction(self.prices, self.signals)
        
        # trade_delta = [0, 1, 0, 2, 0]
        # cost = trade_delta * 0.001
        self.assertEqual(len(costs), 5)
        self.assertEqual(costs[1], 0.001)
        self.assertEqual(costs[3], 0.002)
        self.assertEqual(costs[0], 0)
        self.assertEqual(costs[2], 0)
        self.assertEqual(costs[4], 0)

if __name__ == '__main__':
    unittest.main()
