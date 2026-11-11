import unittest
from unittest.mock import patch
from models import FinanceManager
from transactions import add_transaction, set_budget
from transactions import process_add_transaction, process_set_budget

class TestTransactions(unittest.TestCase):
    @patch('builtins.input', side_effect=['income', '2026-11-11', '1000', 'Salary', 'Monthly Pay'])
    def test_add_income_transaction(self, mock_input):
        manager = FinanceManager()

        add_transaction(manager)

        self.assertEqual(len(manager.transactions), 1)
        trans = manager.transactions[0]
        self.assertEqual(trans.type, 'income')
        self.assertEqual(trans.amount, 1000.0)
        self.assertEqual(trans.category, 'Salary')

    @patch('builtins.input', side_effect=['Food', '500'])
    def test_set_budget(self, mock_input):
        manager = FinanceManager()
        set_budget(manager)

        self.assertIn('food', manager.budgets)
        self.assertEqual(manager.budgets['food'], 500.0)

    def test_process_add_transaction(self):
        manager = FinanceManager()

        trans = process_add_transaction(
            manager,
            "income",
            "2026-11-11",
            1000,
            "Salary",
            "Monthly Pay"
        )

        self.assertEqual(trans.id, 1)
        self.assertEqual(len(manager.transactions), 1)

    def test_process_set_budget(self):
        manager = FinanceManager()

        result = process_set_budget(manager, "Food", 500)

        self.assertEqual(result, 500.0)
        self.assertEqual(manager.budgets["food"], 500.0)

    def test_transaction_ids_increment(self):
        manager = FinanceManager()

        first = process_add_transaction(
            manager, "income", "26-11-11",
            1000, "Salary", "Monthly Pay" 
        )

        second = process_add_transaction(
            manager, "expense", "26-11-11",
            200, "Food", "Lunch" 
        )

        self.assertEqual(first.id, 1)
        self.assertEqual(second.id, 2)

    def test_process_add_transaction_rejects_negative_amount(self):
        manager = FinanceManager()

        with self.assertRaises(ValueError):
            process_add_transaction(
                manager,
                "expense",
                "2026-11-11",
                -100,
                "Food",
                "Lunch"
            )

        self.assertEqual(len(manager.transactions), 0)


if __name__ == "__main__":
    unittest.main()
