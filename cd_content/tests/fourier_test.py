import numpy as np
import numpy.fft as fft
import math


def fourier_test(vector):
    """Tests randomness using Fourier transform"""
    transformed = fft.fft(list(map(lambda x: 2 * x - 1, vector)))
    max_range = (len(vector) - 1) // 2 + 1
    passed = 0
    kappa = np.sqrt(-len(vector) * np.log(0.05))
    for r in transformed[1:max_range]:
        if abs(r) < kappa:
            passed += 1
    return 1 - math.erf(abs(passed - max_range * 0.95) / np.sqrt(2 * max_range * 0.95 * 0.05))
