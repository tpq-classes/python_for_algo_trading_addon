#
# Monte Carlo Simulation of GBM
# using NumPy
#
import q
import math
import numpy as np
from IPython import embed

@q
def simulate_paths(S0, T, r, v, M, I):
    dt = T / M
    S = np.zeros((M + 1, I))
    S[0] = S0
    for t in range(1, M + 1):
        rnd = np.random.standard_normal(I)
        S[t] = S[t - 1] * np.exp((r - v ** 2 / 2) * dt +
                v * math.sqrt(dt) * rnd)
    return S

@q
def value_put_option(S0, K, T, r, v, M, I):
    S = simulate_paths(S0, T, r, v, M, I)
    h = np.maximum(K - S[-1], 0)
    return h.mean() * math.exp(-r * T)


if __name__ == '__main__':
    S0, T, r, v = 36, 1, 0.06, 0.2
    M, I = 50, 50000
    embed()
    S = simulate_paths(S0, T, r, v, M, I)
    S0_ = S[-1].mean() * math.exp(-r * T)
    print(f'average disc value = {S0_:.3f}')
    K = 40
    P0 = value_put_option(S0, K, T, r, v, M, I)
    print(f'put option value   = {P0:.3f}')
