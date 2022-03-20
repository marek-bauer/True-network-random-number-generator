import scipy.stats as stats
import scipy.special as spec
from .utils import safe_div, get_range, T, RANGES


def get_probabilities():
    """Computer theoretical probabilities for 1024 test"""
    res = [sum(map(lambda x: spec.comb(1024, x, exact=True), range(RANGES[0] + 1)))]
    for i in range(len(RANGES) - 1):
        t = sum(map(lambda x: spec.comb(1024, x, exact=True), range(RANGES[i] + 1, RANGES[i + 1] + 1)))
        res.append(t)
    t = sum(map(lambda x: spec.comb(1024, x, exact=True), range(RANGES[T - 2] + 1, 1025)))
    res.append(t)
    return list(map(lambda x: x / 2 ** 1024, res))


def block_frequency_test_1024(vector):
    """Tests randomness using 1024-bits block frequencies with ranges"""
    p = get_probabilities()
    O = [0] * T
    s = 0
    N = len(vector) // 1024
    for i in range(len(vector)):
        s += vector[i]
        if i % 1024 == 1024 - 1:
            O[get_range(s)] += 1
            s = 0
    chi_sq = 0
    for i in range(T):
        E_i = N * p[i]
        if E_i != 0.0:
            chi_sq += (O[i] - E_i) ** 2 / E_i

    return 1 - stats.chi2.cdf(chi_sq, T - 1)


def block_frequency_test(vector, M):
    """Tests randomness using M-bits block frequencies"""
    O = [0] * (M + 1)
    s = 0
    N = len(vector) // M
    for i in range(len(vector)):
        s += vector[i]
        if i % M == M - 1:
            O[s] += 1
            s = 0
    chi_sq = 0
    for i in range(M + 1):
        E_i = safe_div(N * spec.comb(M, i, exact=True), 2 ** M)
        if E_i != 0.0:
            chi_sq += (O[i] - E_i) ** 2 / E_i

    return 1 - stats.chi2.cdf(chi_sq, M)
