import numpy as np
import math
import scipy.stats as stats


def var_average_price(beta_0, beta_1, beta_2, sigma_1, n, m, p, alpha, seed=None):
    if seed:
        rng = np.random.default_rng(seed)
    else:
        rng = np.random.default_rng()
    return_matrix = rng.normal(0, 1, (m, n))
    vol_matrix = np.zeros((2, n))
    vol_matrix[0, :] = sigma_1**2
    return_matrix[0, :] = sigma_1 * return_matrix[0, :]
    for i in range(1, m):
        vol_matrix[1, :] = beta_2 * vol_matrix[0, :] + \
                           beta_1 * np.power(return_matrix[i-1, :], 2) + \
                           beta_0
        return_matrix[i, :] = np.sqrt(vol_matrix[1, :]) * return_matrix[i, :]
        vol_matrix[0, :] = vol_matrix[1, :]
    total_return = np.sort(np.sum(return_matrix, axis=0))
    var = -total_return[math.floor(n * p)-1]
    k_1 = round(n*p - math.sqrt(n*p*(1-p))*stats.norm.ppf(1-alpha/2))
    k_2 = round(n*p + math.sqrt(n*p*(1-p))*stats.norm.ppf(1-alpha/2))
    return var, total_return[k_1-1], total_return[k_2-1]


if __name__ == "__main__":
    paras = (0.5, 0.3, 0.5, 1, 10000, 10, 0.05, 0.05)
    print(var_average_price(*paras))
    paras = (0.5, 0.3, 0.5, 1, 10000, 10, 0.01, 0.05)
    print(var_average_price(*paras))
