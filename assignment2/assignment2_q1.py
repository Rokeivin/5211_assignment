import numpy as np


def mode_matching(_a, _n, seed=None):
    if seed:
        rng = np.random.default_rng(seed)
    else:
        rng = np.random.default_rng()
    random_matrix = rng.normal(0, 1, (1, _n))
    samples = np.zeros(random_matrix.shape)
    samples[random_matrix > 0] = np.exp(a * np.sqrt(random_matrix[random_matrix > 0]))
    return np.mean(samples), np.std(samples)


def plain_mc(_a, _n, seed=None):
    if seed:
        rng = np.random.default_rng(seed)
    else:
        rng = np.random.default_rng()


if __name__ == "__main__":
    N = 10 ** 4
    a = 1
    # mu_plain, variance_plain = plain_mc(a, N)
    mu_mode, variance_mode = mode_matching(a, N)
    # print("estimation from plain MC is", mu_plain)
    # print("variance from plain MC is", variance_plain)
    print("estimation from mode matching is", mu_mode)
    print("variance from mode matching is", variance_mode)
