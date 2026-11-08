import os
import tempfile
import unittest
from models import FinanceManager, Transaction
from storage import load_data, save_data

class TestStorage(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_file = os.path.join(self.test_dir.name, "test_finance.json")

    def tearDown(self):
        self.test_dir.cleanup()

    def test_load_when_no_file_exists(self):
        manager = load_data(self.test_file)
        self.assertIsInstance(manager, FinanceManager)
        self.assertAlmostEqual(len(manager.transactions), 0)
        self.assertAlmostEqual(manager.budgets, {})

    def test_save_manager_creates_json(self):
        manager = FinanceManager()
        manager.set_budget("food", 5000.0)
        trans = Transaction(1, "2026-11-06", "income", 50000.0, "salary", "Monthly Pay")
        manager.add_transaction(trans)

        save_data(manager, self.test_file)

        reloaded_manager = load_data(self.test_file)

        self.assertIsInstance(reloaded_manager, FinanceManager)
        self.assertEqual(reloaded_manager.budgets, {"food": 5000.0})  # ✅ Fixed to match what was set
        self.assertEqual(len(reloaded_manager.transactions), 1)
        
        restored_trans = reloaded_manager.transactions[0]
        self.assertIsInstance(restored_trans, Transaction)
        self.assertEqual(restored_trans.id, 1)
        self.assertEqual(restored_trans.amount, 50000.0)
        self.assertEqual(restored_trans.category, "salary")
        self.assertEqual(restored_trans.type, "income")

if __name__ == "__main__":
    unittest.main()
