import math
import scipy.stats as stats

M = 2047
T = 16
SPAN = (M + 1) // T


def last_cross(vector):
    """Computes last point where number of zeros was equal to number of ones"""
    last = 0
    pos = vector[0]
    for i in range(1, len(vector)):
        pos += vector[i]
        if pos == 0:
            last = i
    return last


def get_probabilities():
    """Gets theoretical probabilities of last cross position"""
    res = []
    for i in range(T):
        p = 2 * (math.asin(math.sqrt((i + 1) * SPAN / (M + 1))) - math.asin(math.sqrt(i * SPAN / (M + 1)))) / math.pi
        res.append(p)
    return res


def last_cross_test(vector):
    """Tests randomness using position of last cross of zero line in random walk"""
    prob = get_probabilities()
    v = list(map(lambda x: 2 * x - 1, vector))
    O = [0] * T
    N = len(vector) // M
    for i in range(0, N):
        last = last_cross(v[M * i:M * (i + 1)])
        O[last // SPAN] += 1
    chi_sq = 0
    for i in range(T):
        if prob[i] != 0.0:
            E_i = N * prob[i]
            chi_sq += (O[i] - E_i) ** 2 / E_i
    return 1 - stats.chi2.cdf(chi_sq, T - 1)
