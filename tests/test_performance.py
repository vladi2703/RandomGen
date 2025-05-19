import unittest
import random
import time
from random_gen import RandomGen


class PerformanceTest(unittest.TestCase):
    def setUp(self):
        random.seed(42)

    @unittest.skip("Performance demo test")
    def test_performance(self):
        # Test with different numbers of elements
        for nums_count in [10, 20, 40, 10_000]:
            for trails in [10_000, 100_000, 1_000_000]:
                with self.subTest(nums_count=nums_count):
                    numbers = [i for i in range(1, nums_count + 1)]

                    # Test with many decimal places (should use binary search)
                    some_precise_num = 1e-12
                    precise_probs = (nums_count - 1) * [
                        round((1 - some_precise_num) / (nums_count - 1), ndigits=12)
                    ]
                    precise_probs.append(some_precise_num)

                    precise_gen = RandomGen(numbers, precise_probs)
                    self.assertEqual(
                        precise_gen._number_generator, precise_gen._binary_next
                    )

                    # Test with few decimal places (should use lookup table)
                    simple_probs = nums_count * [round(1 / nums_count, ndigits=4)]
                    simple_gen = RandomGen(numbers, simple_probs)
                    self.assertEqual(
                        simple_gen._number_generator, simple_gen._lookup_next
                    )

                    # Test with linear search
                    linear_gen = RandomGen(numbers, simple_probs)
                    linear_gen._number_generator = linear_gen._linear_search

                    # Test linear with precise probabilities
                    linear_gen_precise = RandomGen(numbers, precise_probs)
                    linear_gen_precise._number_generator = (
                        linear_gen_precise._linear_search
                    )

                    start = time.time()
                    for _ in range(trails):
                        simple_gen.next_num()
                    simple_time = time.time() - start

                    start = time.time()
                    for _ in range(trails):
                        precise_gen.next_num()
                    precise_time = time.time() - start

                    if nums_count < 1000:
                        start = time.time()
                        for _ in range(trails):
                            linear_gen.next_num()
                        linear_time = time.time() - start

                        start = time.time()
                        for _ in range(trails):
                            linear_gen_precise.next_num()
                        linear_time_precise = time.time() - start

                    print(
                        f"Size {nums_count}:, Trails {trails}, Lookup table: {simple_time:.6f}s, Binary search: {precise_time:.6f}s, Linear search: {linear_time:.6f}s, Linear search with precise: {linear_time_precise:.6f}s"
                    )
                    simple_time, precise_time, linear_time, linear_time_precise = (
                        0,
                        0,
                        0,
                        0,
                    )
