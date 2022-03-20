import math


def run_test(vector):
    """Tests randomness by counting number of runs in vector"""
    n_0 = 0
    n_1 = 0
    ro = 0
    if vector[0] == 0:
        n_0 = 1
    else:
        n_1 = 1
    for i in range(1, len(vector)):
        if vector[i] == 0:
            n_0 += 1
            if vector[i - 1] == 1:
                ro += 1
        else:
            n_1 += 1
            if vector[i - 1] == 0:
                ro += 1
    n = n_0 + n_1
    expected = 2 * n_0 * n_1 / n + 1
    variance = 2 * n_0 * n_1 * (2 * n_0 * n_1 - n) / (n * n * (n - 1))
    return 1 - math.erf(abs(ro + 1 - expected) / math.sqrt(2 * variance))
