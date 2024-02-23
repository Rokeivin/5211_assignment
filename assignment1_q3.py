import numpy as np
import math


def plain_mc(s0, r, vol, k, t, m, n, seed=None):
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
    price_paths[1:, :] = (r - 0.5 * vol ** 2) * dt + vol * random_matrix
    price_paths = np.exp(np.cumsum(price_paths, axis=0))
    price_use = math.exp(-r * t) * (np.max(price_paths, axis=1) - k)
    price_use[price_use < 0] = 0
    return np.mean(price_use), np.std(price_use) / math.sqrt(n)


def antithetic_mc(s0, r, vol, k, t, m, n, seed=None):
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
    price_paths[1:, :] = (r - 0.5 * vol ** 2) * dt + vol * random_matrix
    price_paths = np.exp(np.cumsum(price_paths, axis=0))


def control_variate_mc(s0, r, vol, b, k, t, m, n, seed=None):
    pass


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
    price_use = math.exp(-r * t) * (np.max(price_paths, axis=1) - k)
    price_use[price_use < 0] = 0
    if method == "plain":
        current_value = np.mean(price_use)
        se = np.std(price_use) / math.sqrt(n)
    elif method == "antithetic":
        price_paths_y = np.zeros((m + 1, n))
        price_paths_y[0, :] = math.log(s0)
        price_paths_y[1:, :] = (r - 0.5 * vol ** 2) * dt - vol * random_matrix * math.sqrt(dt)
        price_paths_y = np.exp(np.cumsum(price_paths_y, axis=0))
        price_use_y = math.exp(-r * t) * (np.max(price_paths_y, axis=1) - k)
        price_use_y[price_use_y < 0] = 0

        price_final = (price_use + price_use_y) / 2
        current_value = np.mean(price_final)
        se = np.std(current_value) / math.sqrt(n)

    elif method == "control":
        price_use_y = math.exp(-r * t) * (price_paths[-1, :] - k)
        price_use_y[price_use_y < 0] = 0
        mean_y = np.mean(price_use_y)
        b_star = ((price_use - np.mean(price_use)) * (price_use_y - mean_y)) \
                 / np.sum(np.power(price_use_y - mean_y))


    else:
        raise ValueError("illegal method")
    return current_value, se


if __name__ == "__main__":
    # paras = (50, 0.1, 0.2, 50, 1, 10, 10000)
    # price, std = plain_mc(*paras)
    # print('With plain MC, price is', price, 's.e. is', std)
    a = np.array([[1, 2, 3], [3, 4, 5]])
