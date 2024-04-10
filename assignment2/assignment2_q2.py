import numpy as np


def plain_mc(_n, _b, seed=None):
    if seed:
        rng = np.random.default_rng(seed)
    else:
        rng = np.random.default_rng()
    random_matrix = rng.normal(0, 1, (3, _n))
    random_matrix[0, :] = random_matrix[0, :] + random_matrix[1, :]
    random_matrix[2, :] = 2 * random_matrix[2, :] + random_matrix[1, :] + 1
    random_matrix[1, :] = np.minimum(random_matrix[0, :], random_matrix[2, :])
    bool_matrix = random_matrix[1, :] > _b
    return np.mean(bool_matrix), np.std(bool_matrix) / np.sqrt(_n)


def cross_entropy(_n, _b, _N, seed=None):
    if seed:
        rng = np.random.default_rng(seed)
    else:
        rng = np.random.default_rng()
    random_matrix = rng.normal(0, 1, (3, _N))
    h_x = np.minimum(random_matrix[0, :] + random_matrix[1, :],
                     2 * random_matrix[2, :] + random_matrix[1, :] + 1) > _b
    theta1 = np.sum(h_x * random_matrix[0, :])/np.sum(h_x)
    theta2 = np.sum(h_x * random_matrix[1, :]) / np.sum(h_x)
    theta3 = np.sum(h_x * random_matrix[2, :]) / np.sum(h_x)
    random_matrix_y = np.zeros((3, _n))
    if seed:
        rng = np.random.default_rng(seed)
    else:
        rng = np.random.default_rng()
    random_matrix_y[0, :] = rng.normal(theta1, 1, (1, _n))
    random_matrix_y[1, :] = rng.normal(theta2, 1, (1, _n))
    random_matrix_y[2, :] = rng.normal(theta3, 1, (1, _n))
    h_y = np.minimum(random_matrix_y[0, :] + random_matrix_y[1, :],
                     2 * random_matrix_y[2, :] + random_matrix_y[1, :] + 1) > _b
    h = h_y * np.exp((theta1**2+theta2**2+theta3**2)/2 -
                     (theta1*random_matrix_y[0, :]+theta2*random_matrix_y[1, :]+theta3*random_matrix_y[2, :]))
    return np.mean(h), np.std(h)/np.sqrt(_n)


if __name__ == "__main__":
    n = 10000
    N = 2000
    for b in [1, 2, 3]:
        plain_mu, plain_variance = plain_mc(n, b)
        print(f"with b = {b} estimation from plain MC is", plain_mu, "std  is", plain_variance)
    for b in [1, 2, 3]:
        ce_mu, ce_variance = cross_entropy(n, b, N)
        print(f"with parameter {b} estimation from cross-entropy MC is", ce_mu, "std  is", ce_variance)
