import numpy as np
from scipy.stats import norm

def plain_mc(_sigma, _mu, _r, _n, _m, _t, _s0, _k, seed=None):
    if seed:
        rng = np.random.default_rng(seed)
    else:
        rng = np.random.default_rng()
    dt = _t / _m
    dt_sqrt = np.sqrt(dt)
    random_matrix = rng.normal(0, 1, (_m, _n))
    prices_x = np.zeros((1, _n)) + _s0
    for _i in range(_m):
        prices_x = prices_x + _r * dt * prices_x + \
                   dt_sqrt * np.sqrt(_sigma**2+(_mu**2)*np.power(prices_x, 2)) * random_matrix[_i, :]
    value = np.exp(-_r*_t) * np.maximum(prices_x - _k, 0)
    return np.mean(value), np.std(value)/np.sqrt(_n)


def control_variate(_sigma, _mu, _r, _n, _m, _t, _s0, _k, seed=None):
    if seed:
        rng = np.random.default_rng(seed)
    else:
        rng = np.random.default_rng()
    dt = _t / _m
    dt_sqrt = np.sqrt(dt)
    new_sigma = _mu
    random_matrix = rng.normal(0, 1, (_m, _n))
    prices_x = np.zeros((1, _n)) + _s0
    prices_y = np.zeros((1, _n)) + np.log(_s0)
    for _i in range(_m):
        prices_x = prices_x + _r * dt * prices_x + \
                   dt_sqrt * np.sqrt(_sigma**2+(_mu**2)*np.power(prices_x, 2)) * random_matrix[_i, :]
        prices_y = prices_y + (_r - 0.5*(new_sigma**2))*dt + new_sigma * random_matrix[_i, :] * dt_sqrt
    prices_y = np.exp(prices_y)
    value_x = np.max(prices_x - _k, 0) * np.exp(-_r * _t)
    value_y = np.max(prices_y - _k, 0) * np.exp(-_r * _t)
    d1 = (np.log(_s0/_k)+(_r+0.5*new_sigma**2)*_t)/(new_sigma * np.sqrt(_t))
    d2 = d1 - new_sigma * np.sqrt(_t)
    m_y = _s0 * norm.cdf(d1) - _k * np.exp(-_r * _t) * norm.cdf(d2)
    mean_y = np.mean(value_y)
    b_star = np.sum((value_x - np.mean(value_x))*(value_y - mean_y)) / np.sum(np.power(value_y - mean_y, 2))
    h = value_x - b_star * (value_y - m_y)
    return np.mean(h), np.std(h)/np.sqrt(_n)


def path_diff():
    pass


if __name__ == "__main__":
    sigma = 2
    mu = 0.2
    r = 0.03
    n = 10000
    m = 30
    t = 1
    s0 = 50
    k = 50
    call_value, value_std = plain_mc(sigma, mu, r, n, m, t, s0, k)
    print("value of option estimated from plain MC is", call_value, "std is", value_std)
    call_value, value_std = control_variate(sigma, mu, r, n, m, t, s0, k)
    print("value of option estimated from plain MC is", call_value, "std is", value_std)

