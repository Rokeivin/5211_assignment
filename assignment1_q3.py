import numpy as np
import math
from scipy.stats import norm


def variance_reduction_mc(s0, r, vol, k, t, m, n, method, seed=None):
    m = int(m)
    n = int(n)
    dt = t / m
    if seed:
        rng = np.random.default_rng(seed)
    else:
        rng = np.random.default_rng()
    random_matrix = rng.normal(0, 1, (m, n))
    price_paths = np.zeros((m + 1, n))
    price_paths[0, :] = math.log(s0)
    price_paths[1:, :] = (r - 0.5 * vol ** 2) * dt + vol * random_matrix * math.sqrt(dt)
    price_paths = np.exp(np.cumsum(price_paths, axis=0))
    price_use = math.exp(-r * t) * (np.max(price_paths, axis=0) - k)
    price_use[price_use < 0] = 0
    if method == "plain":
        current_value = np.mean(price_use)
        se = np.std(price_use) / math.sqrt(n)
    elif method == "antithetic":
        price_paths_y = np.zeros((m + 1, n))
        price_paths_y[0, :] = math.log(s0)
        price_paths_y[1:, :] = (r - 0.5 * vol ** 2) * dt - vol * random_matrix * math.sqrt(dt)
        price_paths_y = np.exp(np.cumsum(price_paths_y, axis=0))
        price_use_y = math.exp(-r * t) * (np.max(price_paths_y, axis=0) - k)
        price_use_y[price_use_y < 0] = 0

        price_final = (price_use + price_use_y) / 2
        current_value = np.mean(price_final)
        se = np.std(price_final) / math.sqrt(n)

    elif method == "control":
        d1 = (np.log(s0 / k) + (r + 0.5 * vol ** 2) * t) / (vol * np.sqrt(t))
        d2 = d1 - vol * np.sqrt(t)
        euro_call = (s0 * norm.cdf(d1) - k * np.exp(-r * t) * norm.cdf(d2))
        price_use_y = math.exp(-r * t) * (price_paths[-1, :] - k)
        price_use_y[price_use_y < 0] = 0
        mean_y = np.mean(price_use_y)
        b_star = np.sum((price_use - np.mean(price_use)) * (price_use_y - mean_y)) \
                 / np.sum(np.power(price_use_y - mean_y, 2))
        h = price_use - b_star * (price_use_y - euro_call)
        current_value = np.mean(h)
        se = np.std(h)/math.sqrt(n)
    else:
        raise ValueError("illegal method")
    return current_value, se


if __name__ == "__main__":
    paras = (50, 0.05, 0.2, 55, 1, 50, 10000, "plain")
    price, std = variance_reduction_mc(*paras)
    print('With plain MC, price is', price, 's.e. is', std)
    paras = (50, 0.05, 0.2, 55, 1, 50, 10000, "antithetic")
    price, std = variance_reduction_mc(*paras)
    print('With antithetic MC, price is', price, 's.e. is', std)
    paras = (50, 0.05, 0.2, 55, 1, 50, 10000, "control")
    price, std = variance_reduction_mc(*paras)
    print('With control variate MC, price is', price, 's.e. is', std)

