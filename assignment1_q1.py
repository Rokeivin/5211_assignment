import numpy as np
import math


def down_out_call(s0, r, vol, b, k, t, m, n, seed=None):
    m = int(m)
    n = int(n)
    price_paths = np.zeros((m + 1, n))
    dt = t / m
    if seed:
        rng = np.random.default_rng(seed)
    else:
        rng = np.random.default_rng()
    random_matrix = rng.normal(0, 1, (m, n))
    price_paths[0, :] = math.log(s0)
    price_paths[1:, :] = (r - 0.5 * vol ** 2) * dt + vol * random_matrix * math.sqrt(dt)
    price_paths = np.exp(np.cumsum(price_paths, axis=0))
    if_out = np.sum(price_paths[1:, :] >= b, axis=0) > 0
    pay_off = price_paths[-1, :] - k
    if if_out.shape[0] == 0:
        pay_off[:, :] = 0
    else:
        pay_off[np.logical_not(if_out)] = 0
        pay_off[pay_off < 0] = 0
    return math.exp(-r * t) * np.sum(pay_off) / n, np.std(pay_off) / math.sqrt(n)


if __name__ == "__main__":
    paras = (50, 0.1, 0.2, 45, 50, 1, 12, 10000)
    price, std = down_out_call(*paras)
    print('with 10000 simulations, price is', price, 's.e. is', std)
    paras = (50, 0.1, 0.2, 45, 50, 1, 12, 40000)
    price, std = down_out_call(*paras)
    print('with 40000 simulations, price is', price, 's.e. is', std)
