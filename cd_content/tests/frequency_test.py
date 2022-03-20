import math


def frequency_test(vector):
    """Tests randomness using ratio of ones to zeros"""
    S = 0
    for v in vector:
        if v == 0:
            S -= 1
        else:
            S += 1
    return 1 - math.erf(abs(S) / math.sqrt(2 * len(vector)))
