import unittest

from calculator_gui import evaluate


class EvaluateTests(unittest.TestCase):
    def test_basic_operations(self):
        self.assertEqual(evaluate("2+3"), "5")
        self.assertEqual(evaluate("10-4"), "6")
        self.assertEqual(evaluate("6×7"), "42")
        self.assertEqual(evaluate("9÷3"), "3")
        self.assertEqual(evaluate("1÷4"), "0.25")

    def test_priority_and_brackets(self):
        self.assertEqual(evaluate("2+3×4"), "14")
        self.assertEqual(evaluate("(2+3)×4"), "20")
        self.assertEqual(evaluate("-5+2"), "-3")

    def test_comma_decimal(self):
        self.assertEqual(evaluate("2,5×2"), "5")

    def test_errors(self):
        for bad in ["5÷0", "", "2++", "__import__('os')", "2**3", "abc"]:
            with self.assertRaises(ValueError, msg=bad):
                evaluate(bad)


if __name__ == "__main__":
    unittest.main()
