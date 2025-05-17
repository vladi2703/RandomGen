import random
from typing import List, Optional


class RandomGen(object):
    # Values that may be returned by next_num()
    _random_nums = []
    # Probability of the occurrence of random_nums
    _probabilities = []

    _cumulative_sums = []
    _lookup_table = {}
    _max_decimal_places = 0

    def __init__(self, random_nums: List[int], probabilities: List[float]):
        """
        Initializes the random generator with the given random numbers and their probabilities.
        :param random_nums: List of random numbers to be generated.
        :param probabilities: List of probabilities corresponding to each random number.
        """
        if len(random_nums) != len(probabilities):
            raise ValueError("random_nums and probabilities must have the same length")
        minimal_probability = probabilities[0]

        self._random_nums = random_nums
        self._probabilities = probabilities

        self._lookup_table = {}
        self._cumulative_sums = [0] * len(probabilities)
        self._cumulative_sums[0] = probabilities[0]
        for i in range(1, len(probabilities)):
            if not 0 <= probabilities[i] <= 1:
                raise ValueError("Probabilities must be between 0 and 1")

            minimal_probability = min(minimal_probability, probabilities[i])
            self._cumulative_sums[i] = self._cumulative_sums[i - 1] + probabilities[i]
            self._max_decimal_places = max(
                self._max_decimal_places,
                RandomGen._get_decimal_places(probabilities[i]),
            )
        if not abs(self._cumulative_sums[-1] - 1) < 1e-6:
            raise ValueError("Probabilities must sum to 1")

        # TODO: Think of a cleaner way to do this
        # If the smallest probability is very small, use only binary search -
        # caching will get too memory intensive 
        if self._max_decimal_places > 10:
            self.next_num = self._binary_next
        else:
            self.next_num = self._lookup_next

    def _binary_next(self, number_to_find: Optional[float] = None) -> int:
        """
        Returns a random number based on the initialized probabilities using binary search.
        :param number_to_find: A number to find in the cumulative sums.
        """
        if number_to_find:
            rand_num = number_to_find
        else:
            rand_num = random.random()

        left, right = 0, len(self._cumulative_sums) - 1
        while left < right:
            mid = (left + right) // 2
            if self._cumulative_sums[mid] < rand_num:
                left = mid + 1
            else:
                right = mid
        return self._random_nums[left]

    def _lookup_next(self) -> int:
        """
        Returns a random number based on the initialized probabilities using a lookup table.
        If the number is not found in the lookup table, it uses binary search to find the number.
        """
        rand_num = random.random()
        rand_num = round(rand_num, self._max_decimal_places + 1)

        # Convert to string for lookup
        rand_key = str(rand_num)

        if rand_key in self._lookup_table:
            return self._lookup_table[rand_key]
        else:
            res = self._binary_next(rand_num)
            self._lookup_table[rand_key] = res
            return res

    def _get_decimal_places(num: float) -> int:
        """
        Returns the number of decimal places in a float.
        """
        num_str = str(num)
        if "." in num_str:
            decimal_part = num_str.split(".")[1]
            # Remove trailing zeros
            decimal_part = decimal_part.rstrip("0")
            return len(decimal_part)
        elif "e" in num_str:
            # Handle scientific notation (e.g., 1e-5)
            parts = num_str.split("e")
            if "-" in parts[1]:
                # For negative exponent (e.g., 1e-5), the exponent indicates decimal places
                return int(parts[1][1:])  # Remove the negative sign and convert to int
        else:
            return 0

    def next_num(self):
        """
        Returns one of the randomNums.
        When this method is called multiple times over a long period, it should return the numbers roughly with
        the initialized probabilities.
        """
        pass