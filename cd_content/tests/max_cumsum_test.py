import math


def max_value_on_path(vector):
    """Computes maximum value of random walk"""
    m = 0
    path = 0
    for v in vector:
        path += 2 * v - 1
        m = max(m, path)
    return m


def max_cumsum_test(vector):
    """Tests randomness using maximum value of random walk"""
    m = max_value_on_path(vector)
    return 1 - math.erf(m / math.sqrt(2 * len(vector)))
