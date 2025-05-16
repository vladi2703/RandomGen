import random
import typing


class RandomGen(object):
    # Values that may be returned by next_num()
    _random_nums = []
    # Probability of the occurrence of random_nums
    _probabilities = []

    _cumulative_sums = []
    _lookup_table = {}

    def __init__(
        self, random_nums: typing.List[int], probabilities: typing.List[float]
    ):
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

        self._cumulative_sums = [0] * len(probabilities)
        self._cumulative_sums[0] = probabilities[0]
        for i in range(1, len(probabilities)):
            if not 0 <= probabilities[i] <= 1:
                raise ValueError("Probabilities must be between 0 and 1")

            minimal_probability = min(minimal_probability, probabilities[i])
            self._cumulative_sums[i] = self._cumulative_sums[i - 1] + probabilities[i]

        if not abs(self._cumulative_sums[-1] - 1) < 1e-6:
            raise ValueError("Probabilities must sum to 1")

    def _binary_next(self) -> int:
        """
        Returns a random number based on the initialized probabilities using binary search.
        """
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
        """
        rand_num = random.random()
        # TODO: make this 1 to the most decimal places in the probabilities list
        rand_num = round(rand_num, 1)
        if rand_num in self._lookup_table:
            print("Took from lookup table")
            return self._lookup_table[rand_num]
        else:
            left, right = 0, len(self._cumulative_sums) - 1
            while left < right:
                mid = (left + right) // 2
                if self._cumulative_sums[mid] < rand_num:
                    left = mid + 1
                else:
                    right = mid
            self._lookup_table[rand_num] = self._random_nums[left]
            return self._random_nums[left]

    def _get_decimal_places(num: float) -> int:
        """
        Returns the number of decimal places in a float.
        """
        num_str = str(num)
        if "." in num_str:
            decimal_part = num_str.split(".")[1]
            # Remove trailing zeros
            decimal_part.rstrip("0")
            return len(decimal_part)
        else:
            return 0

    def next_num(self):
        """
        Returns one of the randomNums. When this method is called multiple times over a long period, it should return the numbers roughly with the initialized probabilities.
        """
        return self._binary_next()
