import unittest

from calculator import calculator

class TestOperating(unittest.TestCase):
    def test_sum(self):
        calculation = calculator(8,2)
        answer = calculation.get_sum()
        self.assertEqual(answer,10, "the sum is wrong")

    def test_diff(self):
        calculation = calculator(8,2)
        answer = calculation.get_diff()
        self.assertEqual(answer,6, "the sum is wrong")

    def test_prod(self):
        calculation = calculator(8,2)
        answer = calculation.get_prod()
        self.assertEqual(answer,16, "the sum is wrong")

    def test_div(self):
        calculation = calculator(8,0)
        answer = calculation.get_div()
        self.assertEqual(answer,0, "the sum is wrong")

if __name__ == "__main__":
    unittest.main()