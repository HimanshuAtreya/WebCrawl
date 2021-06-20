import unittest

from lambda_function import tesla

class MyTestCase(unittest.TestCase):
    def test_something(self):

        self.assertIsNotNone(tesla('https://cxl.com/blog/bayesian-frequentist-ab-testing/'))


if __name__ == '__main__':
    unittest.main()
