import math


def safe_div(a: int, b: int) -> float:
    l_a = math.ceil(math.log2(a))
    shift = l_a - 52
    if shift > 0:
        return (a >> shift) / (b >> shift)
    else:
        return a / b


RANGES = [256, 384, 448, 480, 496, 504, 508, 510, 511, 512, 513, 515, 519, 527, 543, 575, 639, 767]
T = len(RANGES) + 1


def get_range(x):
    for i in range(len(RANGES)):
        if x <= RANGES[i]:
            return i
    return len(RANGES)


if __name__ == "__main__":
    import scipy.special as spec

    M = 1024
    SIZE = 12 * 8 * 1024 * 1024
    for i in range(M + 1):
        print(str(safe_div(SIZE * spec.comb(M, i, exact=True), 2 ** M)) + " - " + str(
            SIZE * spec.comb(M, i, exact=True) / 2 ** M))
