import itertools
import scipy.stats as stats


def partitions(n, k):
    """Generates a n-elements tuple with sum of elements equals k"""
    if n >= 0 and k >= 1:
        yield from partitions_with_prefixed(tuple(), n, k)


def partitions_with_prefixed(prefix, n, k):
    """Generates a n-elements tuple with prefix with sum of elements equals k"""
    if k == 1:
        yield prefix + (n,)
    else:
        for i in range(n + 1):
            yield from partitions_with_prefixed(prefix + (i,), n - i, k - 1)


def generate_all_orders(to, n):
    """Generates of n-elements tuples of increasing values with last value less than to"""
    for m in range(to + 1):
        for pat in partitions(to - m, n):
            yield tuple(itertools.accumulate(pat))


def compute_probability(m, k):
    """Gets probability of getting mxm matrix with rank (m-k)"""
    p = 1
    for i in range(m - k):
        p *= (1 - 2 ** (-m + i))
    if k == 0:
        return p
    s = 0
    for comb in generate_all_orders(m - k, k):
        s += 2 ** (-sum(comb))
    return p * s * (2 ** (-k ** 2))


def get_probabilities(m):
    """Gets list of theoretical probabilities of getting mxm matrix with specified rank"""
    result = []
    for k in range(min(9, m + 1)):
        result.append(compute_probability(m, k))
    if m >= 8:
        result.append(1.0 - sum(result))
    return result


def matrixfy(vector, n):
    """Generates nxn matrices out of vector"""
    i = iter(vector)
    while True:
        m = []
        for _ in range(n):
            row = []
            for _ in range(n):
                b = next(i, None)
                if b is None:
                    return
                row.append(b)
            m.append(row)
        yield m


def get_range(n):
    """Computes last point where number of zeros was equal to number of ones"""
    if n > 8:
        return 9
    else:
        return n


def matrix_rank(matrix):
    """Computes rank of binary matrix"""
    m = len(matrix[0])
    rank = 0
    for col in range(m):
        rows = []
        for j in range(len(matrix)):
            if matrix[j][col] == 1:
                rows += [j]
        if len(rows) >= 1:
            for c in range(1, len(rows)):
                for k in range(m):
                    matrix[rows[c]][k] = (matrix[rows[c]][k] + matrix[rows[0]][k]) % 2
            matrix.pop(rows[0])
            rank += 1
    for row in matrix:
        if sum(row) > 0:
            rank += 1
    return rank


probabilities = {}


def matrix_rank_test(vector, m):
    """Tests randomness using ranks of mxm matrices"""
    if m in probabilities.keys():
        p = probabilities[m]
    else:
        p = get_probabilities(m)
        probabilities[m] = p
    O = [0] * min(m + 1, 10)
    N = len(vector) // m ** 2
    for matrix in matrixfy(vector, m):
        rank = matrix_rank(matrix)
        O[get_range(m - rank)] += 1
    chi_sq = 0
    for i in range(min(m + 1, 10)):
        if p[i] != 0.0:
            E_i = N * p[i]
            chi_sq += (O[i] - E_i) ** 2 / E_i
    return 1 - stats.chi2.cdf(chi_sq, min(m, 9))
