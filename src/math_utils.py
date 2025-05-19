from typing import List, Tuple

import scipy.stats as stats


def chi_square_test(
    observed_freqs: List[int],
    expected_freqs: List[int],
    alpha: float = 0.05,
) -> Tuple[float, float, bool]:
    """
    Perform a chi-square goodness-of-fit test from scratch.

    Parameters:
    - observed_freqs: List of observed frequencies from your random generator
    - expected_freqs: List of expected frequencies based on your probability distribution
    - alpha: Significance level (default: 0.05)

    Returns:
    - chi_square_stat: The calculated chi-square statistic
    - p_value: The calculated p-value
    - reject_null: Boolean, whether to reject the null hypothesis
    """
    chi_square_statistic = sum(
        (o - e) ** 2 / e for o, e in zip(observed_freqs, expected_freqs)
    )

    degrees_of_freedom = len(observed_freqs) - 1

    # Calculate p-value using the chi-square distribution
    p_value = 1 - stats.chi2.cdf(chi_square_statistic, degrees_of_freedom)

    reject_null = p_value < alpha

    return chi_square_statistic, p_value, reject_null
