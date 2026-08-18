import unittest

from calculator import calculator

class TestOperating(unittest.TestCase):

    def setUp(self):
        self.calc = calculator(8,2)

    def test_sum(self):
        self.assertEqual(self.calc.get_sum(),10, "the sum is wrong")

    def test_diff(self):
        self.assertEqual(self.calc.get_diff(),6, "the sum is wrong")

    def test_prod(self):
        self.assertEqual(self.calc.get_prod(),16, "the sum is wrong")

    def test_div(self):
        self.assertEqual(self.calc.get_div(),4, "the sum is wrong")

    def tearDown(self):
        return super().tearDown()

if __name__ == "__main__":
    unittest.main()