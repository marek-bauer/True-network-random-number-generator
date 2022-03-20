import scipy.stats as stats
from .utils import safe_div
import math

RANGES = [4, 6, 8, 9, 10, 11, 12, 13, 15, 18, 24, 30, 50, 100, 200, 400]
T = len(RANGES) + 1


def get_range(x):
    """Gets index of range to which contains x"""
    for i in range(len(RANGES)):
        if x <= RANGES[i]:
            return i
    return len(RANGES)


def _vectors_with_longest_run_under_run(length, max_run):
    """Gets number of vectors with longest run shorter then max_run"""
    results = [2 ** i for i in range(max_run + 1)]
    for i in range(max_run, length):
        results.append(sum(results[i - max_run:i + 1]))
    return results[length]


def _get_list_of_all_runs(length):
    """Gets a list with number of vectors with specified length specified longest run"""
    sum_prev = 0
    result = []
    for i in range(length + 1):
        less_of_eq = _vectors_with_longest_run_under_run(length, i)
        result.append(less_of_eq - sum_prev)
        sum_prev = less_of_eq
    return result


def get_probabilities():
    """Gets a theoretical probabilities of getting vector with longest run in specified range"""
    prev = 0
    res = []
    for i in range(len(RANGES)):
        t = _vectors_with_longest_run_under_run(1024, RANGES[i])
        res.append(t - prev)
        prev = t
    res.append(2 ** 1024 - sum(res))
    return list(map(lambda x: x / 2 ** 1024, res))


def _longest_run(vector):
    """Computes longest run of vector"""
    max_run = 0
    current_run = 0
    for v in vector:
        if v == 0:
            max_run = max(max_run, current_run)
            current_run = 0
        else:
            current_run += 1
    max_run = max(max_run, current_run)
    return max_run


p = get_probabilities()


def longest_run_in_block_test_1024(vector):
    """Tests randomness using length of longest run in 1024-bits blocks"""
    M = 1024
    O = [0] * T
    N = len(vector) // M
    for i in range(0, len(vector) // M):
        length_of_run = _longest_run(vector[M * i:M * (i + 1)])
        O[get_range(length_of_run)] += 1
    chi_sq = 0
    for i in range(T):
        E_i = N * p[i]
        if E_i != 0.0:
            chi_sq += (O[i] - E_i) ** 2 / E_i
    return 1 - stats.chi2.cdf(chi_sq, T - 1)


longest_runs = {}


def longest_run_in_block_test(vector, M):
    """Tests randomness using length of longest run in M-bits blocks"""
    T = math.ceil(M)
    if M in longest_runs.keys():
        list_of_longest_runs = longest_runs[M]
    else:
        list_of_longest_runs = _get_list_of_all_runs(M)
        longest_runs[M] = list_of_longest_runs
    O = [0] * T
    N = len(vector) // M
    for i in range(0, len(vector) // M):
        length_of_run = _longest_run(vector[M * i:M * (i + 1)])
        O[length_of_run] += 1
    chi_sq = 0
    for i in range(T):
        E_i = safe_div(N * sum(list_of_longest_runs[i: i + 1]), 2 ** M)
        if E_i != 0.0:
            chi_sq += (O[i] - E_i) ** 2 / E_i
    return 1 - stats.chi2.cdf(chi_sq, T - 1)
