import unittest
import random
from collections import Counter
from random_gen import RandomGen
from math_utils import chi_square_test


class TestRandomGen(unittest.TestCase):
    def setUp(self):
        random.seed(42)

        self.random_nums = [1, 2, 3, 4, 5]
        self.probabilities = [0.1, 0.2, 0.3, 0.2, 0.2]
        self.random_gen = RandomGen(self.random_nums, self.probabilities)

    def test_initialization(self):
        # Test that RandomGen initializes correctly
        self.assertEqual(self.random_gen._random_nums, self.random_nums)
        self.assertEqual(self.random_gen._probabilities, self.probabilities)
        for i, val in enumerate([0.1, 0.3, 0.6, 0.8, 1.0]):
            self.assertAlmostEqual(self.random_gen._cumulative_sums[i], val, places=7)

    def test_initialization_errors(self):
        # Test different length lists
        with self.assertRaises(ValueError):
            RandomGen([1, 2, 3], [0.3, 0.7])

        # Test probabilities not between 0 and 1
        with self.assertRaises(ValueError):
            RandomGen([1, 2], [0.5, 1.5])

        # Test probabilities don't sum to 1
        with self.assertRaises(ValueError):
            RandomGen([1, 2, 3], [0.3, 0.3, 0.3])

    def test_only_binary_next(self):
        possible_values = [1, 2]
        small_probabilities_gen = RandomGen(possible_values, [1 - (1e-12), 1e-12])
        # Test that binary_next returns values from possible_values
        for _ in range(100):
            result = small_probabilities_gen._binary_next()
            self.assertIn(result, possible_values)

    def test_next_num(self):
        # Test that next_num returns values from random_nums
        for _ in range(100):
            result = self.random_gen.next_num()
            self.assertIn(result, self.random_nums)

    def test_probability_distribution(self):
        # Test that the distribution matches the expected probabilities
        # Run a large number of trials to ensure statistical significance
        trials = 100_000
        results = Counter()

        for _ in range(trials):
            results[self.random_gen.next_num()] += 1

        observed_counts = [results[num] for num in self.random_nums]
        expected_counts = [trials * prob for prob in self.probabilities]

        # Use chi-square test to check if distribution matches expected probabilities
        chi_square_stat, p_value, reject_null = chi_square_test(
            observed_counts,
            expected_counts,
            alpha=0.0001,
        )

        # Print stats for debugging if the test fails
        self.assertFalse(
            reject_null,
            f"Chi-square test rejected the null hypothesis. Chi-square: {chi_square_stat:.4f}, "
            f"p-value: {p_value:.4f}, observed: {observed_counts}, expected: {expected_counts}",
        )

    def test_edge_cases(self):
        # Test with a single number
        single_gen = RandomGen([42], [1.0])
        self.assertEqual(single_gen.next_num(), 42)

        # Test with int
        single_gen = RandomGen([42], [1])
        self.assertEqual(single_gen.next_num(), 42)

        # Test with extreme probability differences
        skewed_gen = RandomGen([1, 2], [0.99, 0.01])
        trials = 10_000
        results = Counter([skewed_gen.next_num() for _ in range(trials)])
        expected_frequencies = [trials * 0.99, trials * 0.01]
        observed_frequencies = [results[1], results[2]]
        chi_square_stat, p_value, reject_null = chi_square_test(
            observed_frequencies,
            expected_frequencies,
            alpha=0.0001,
        )
        self.assertFalse(
            reject_null,
            f"Chi-square test rejected the null hypothesis. Chi-square: {chi_square_stat:.4f}, "
            f"p-value: {p_value:.4f}, observed: {observed_frequencies}, expected: {expected_frequencies}",
        )

        # Test with e in probabilities
        e_gen = RandomGen([1, 2], [5e-1, 0.5])
        results = Counter([e_gen.next_num() for _ in range(10_000)])
        self.assertAlmostEqual(results[1] / results[2], 1, delta=0.05)

    def test_get_decimal_places(self):
        # Test with various numbers
        self.assertEqual(RandomGen._get_decimal_places(1.234), 3)
        self.assertEqual(RandomGen._get_decimal_places(1.2000), 1)
        self.assertEqual(RandomGen._get_decimal_places(1.0), 0)
        self.assertEqual(RandomGen._get_decimal_places(1e-5), 5)
        self.assertEqual(RandomGen._get_decimal_places(1e5), 0)
        self.assertEqual(RandomGen._get_decimal_places(1.00000000000001), 14)


if __name__ == "__main__":
    unittest.main()
