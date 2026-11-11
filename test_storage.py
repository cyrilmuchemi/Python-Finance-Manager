import os
import tempfile
import unittest
import json
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
        self.assertEqual(len(manager.transactions), 0)
        self.assertEqual(manager.budgets, {})

    def test_save_manager_creates_json(self):
        manager = FinanceManager()
        manager.set_budget("food", 5000.0)
        trans = Transaction(1, "2026-11-06", "income", 50000.0, "salary", "Monthly Pay")
        manager.add_transaction(trans)

        save_data(manager, self.test_file)
        self.assertTrue(os.path.exists(self.test_file))

    def test_save_and_reload_preserves_data(self):
        manager = FinanceManager()
        manager.set_budget("rent", 15000.0)
        trans = Transaction(1, "2026-11-06", "income", 50000.0, "salary", "Monthly Pay")
        manager.add_transaction(trans)

        save_data(manager, self.test_file)
        reloaded_manager = load_data(self.test_file)

        self.assertIsInstance(reloaded_manager, FinanceManager)
        self.assertEqual(reloaded_manager.budgets, {"rent": 15000.0})
        self.assertEqual(len(reloaded_manager.transactions), 1)

    def test_corrupted_json_backs_up_file(self):
        with open(self.test_file, "w") as file:
            file.write("{invalid json content}")

        manager = load_data(self.test_file)

        self.assertIsInstance(manager, FinanceManager)
        self.assertEqual(len(manager.transactions), 0)
        self.assertTrue(os.path.exists(self.test_file + ".back"))

    def test_budget_normalization_on_load(self):
        raw_data = {
            "transactions": [],
            "budgets": {
                "Food": 4000.0,
                "TRANSPORT": 1200.0
            }
        }

        with open(self.test_file, "w") as file:
            json.dump(raw_data, file)

        manager = load_data(self.test_file)

        self.assertEqual(manager.budgets, {
            "food": 4000.0,
            "transport": 1200.0
        })

if __name__ == "__main__":
    unittest.main()
