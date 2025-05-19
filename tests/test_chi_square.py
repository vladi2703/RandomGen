import unittest
from math_utils import chi_square_test


class TestChiSquareTest(unittest.TestCase):
    def test_chi_square_with_uniform_distribution(self):
        # Test with uniform distribution
        observed = [100, 100, 100, 100, 100]
        expected = [100, 100, 100, 100, 100]
        chi_square_stat, p_value, reject_null = chi_square_test(observed, expected)

        self.assertAlmostEqual(chi_square_stat, 0.0)
        self.assertGreater(p_value, 0.05)
        self.assertFalse(reject_null)

    def test_chi_square_with_skewed_distribution(self):
        # Test with highly skewed distribution that should reject null
        observed = [200, 50, 50, 50, 50]
        expected = [80, 80, 80, 80, 80]
        chi_square_stat, p_value, reject_null = chi_square_test(observed, expected)

        self.assertGreater(chi_square_stat, 0.0)
        self.assertLess(p_value, 0.05)
        self.assertTrue(reject_null)

    def test_chi_square_with_different_alpha(self):
        # Test with different alpha value
        observed = [110, 90, 105, 95, 100]
        expected = [100, 100, 100, 100, 100]
        _, _, reject_null_001 = chi_square_test(observed, expected, alpha=0.01)

        # This distribution is close enough that it shouldn't be rejected at alpha=0.01
        self.assertFalse(reject_null_001)

if __name__ == "__main__":
    unittest.main()
