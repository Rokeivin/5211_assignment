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

def cross_entropy(_n, _b):
    pass

if __name__ == "__main__":
    n = 1000
    for b in [1, 2, 3]:
        plain_mu, plain_variance = plain_mc(n, b)
        print(f"with parameter {b} estimation from plain MC is", plain_mu, "std  is", plain_variance)
