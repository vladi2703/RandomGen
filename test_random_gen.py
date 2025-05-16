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
        # Test different length lists
        with self.assertRaises(ValueError):
            RandomGen([1, 2, 3], [0.3, 0.7])

        # Test probabilities not between 0 and 1
        with self.assertRaises(ValueError):
            RandomGen([1, 2], [0.5, 1.5])

        # Test probabilities don't sum to 1
        with self.assertRaises(ValueError):
            RandomGen([1, 2, 3], [0.3, 0.3, 0.3])

    def test_binary_next(self):
        # Test that binary_next returns values from random_nums
        for _ in range(100):
            result = self.random_gen._binary_next()
            self.assertIn(result, self.random_nums)

    def test_lookup_next(self):
        # Test that lookup_next returns values from random_nums
        for _ in range(100):
            result = self.random_gen._lookup_next()
            self.assertIn(result, self.random_nums)

        # Test that lookup table is being used
        self.assertGreater(len(self.random_gen._lookup_table), 0)

    def test_next_num(self):
        # Test that next_num returns values from random_nums
        for _ in range(100):
            result = self.random_gen.next_num()
            self.assertIn(result, self.random_nums)

    def test_probability_distribution(self):
        # Test that the distribution matches the expected probabilities
        # Run a large number of trials to ensure statistical significance
        trials = 100000
        results = Counter()

        for _ in range(trials):
            results[self.random_gen.next_num()] += 1

        # Check that each number appears with roughly the expected frequency
        for i, num in enumerate(self.random_nums):
            expected_count = trials * self.probabilities[i]
            actual_count = results[num]

            # Allow for some statistical variance (within 5%)
            self.assertLess(
                abs(actual_count - expected_count) / trials,
                0.05,
                f"Number {num} appeared with frequency {actual_count / trials:.4f}, "
                f"expected {self.probabilities[i]:.4f}",
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
        results = Counter([skewed_gen.next_num() for _ in range(10000)])
        self.assertGreater(
            results[1], results[2] * 5
        )  # 1 should appear much more frequently

        # Test with e in probabilities
        e_gen = RandomGen([1, 2], [5e-1, 0.5])
        results = Counter([e_gen.next_num() for _ in range(10000)])
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
