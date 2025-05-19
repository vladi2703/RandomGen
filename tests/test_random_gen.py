import unittest
import random
from collections import Counter
from random_gen import RandomGen


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
        with self.assertRaises(
            ValueError, msg="random_nums and probabilities must have the same length"
        ):
            RandomGen([1, 2, 3], [0.3, 0.7])

        with self.assertRaises(ValueError, msg="Probabilities must be between 0 and 1"):
            RandomGen([1, 2], [0.5, 1.5])

        with self.assertRaises(ValueError, msg="Probabilities must be between 0 and 1"):
            RandomGen([-1, 0.5, 0.5, 0.5, 0.5], [0.5, 1.5, 0.6, 1.9, 1.1])

        with self.assertRaises(ValueError, msg="Probabilities must sum to 1"):
            RandomGen([1, 2, 3], [0.3, 0.3, 0.3])

        with self.assertRaises(ValueError, msg="Probabilities should not be empty"):
            RandomGen([], [])

        with self.assertRaises(ValueError, msg="Probabilities should not be None"):
            RandomGen([1, 2], None)

        with self.assertRaises(ValueError, msg="Invalid set of numbers"):
            RandomGen([1, "some"], [0.5, 0.5])

        with self.assertRaises(ValueError, msg="Invalid set of probabilities"):
            RandomGen([0.5, 0.5], [1, "some"])

    def test_only_binary_next(self):
        possible_values = [1, 2]
        small_probabilities_gen = RandomGen(possible_values, [1 - (1e-12), 1e-12])
        for _ in range(100):
            result = small_probabilities_gen._binary_next()
            self.assertIn(
                result,
                possible_values,
                f"result from binary search not in {possible_values=}",
            )

    def test_next_num(self):
        # Test that next_num returns values from random_nums
        for _ in range(100):
            result = self.random_gen.next_num()
            self.assertIn(
                result, self.random_nums, f"result not in {self.random_nums=}"
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
        expected_frequencies = [9903, 97]
        observed_frequencies = [results[1], results[2]]
        self.assertEqual(
            observed_frequencies,
            expected_frequencies,
            f"Expected frequencies: {expected_frequencies}, but got: {observed_frequencies}",
        )

        # Test with scientific notation
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

    def test_distribution_accuracy(self):
        trials = 100_000
        results = Counter()

        for _ in range(trials):
            results[self.random_gen.next_num()] += 1

        observed_counts = [results[num] for num in self.random_nums]
        # Tested that passes the chi-square test with a significance level of 0.0001
        expected_counts = [10074, 19894, 30390, 20124, 19518]
        self.assertEqual(
            observed_counts,
            expected_counts,
            f"Expected counts: {expected_counts}, but got: {observed_counts}",
        )
