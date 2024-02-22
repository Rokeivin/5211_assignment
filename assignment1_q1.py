import numpy as np
import math


def down_out_call(s0, r, vol, b, T, m, n, seed=None):
    m = int(m)
    n = int(n)
    price_paths = np.zeros((m+1, n))
    dt = T/m
    if seed:
        rng = np.random.default_rng(seed)
    else:
        rng = np.random.default_rng()
    random_matrix = rng.normal(0, 1, (m, n))
    price_paths[0, :] = math.log(s0)
    price_paths[1:, :] = (r-0.5*vol**2)*dt + vol * random_matrix
    price_paths = np.exp(np.cumsum(price_paths, axis=0))
    


if __name__ == "__main__":
    arr = np.array([[1, 2, 3], [4, 5, 6]])

    # 不指定axis，对整个数组进行累积求和
    cumsum_flat = np.cumsum(arr)
    print("Cumulative sum without specifying axis:\n", cumsum_flat)

    # 指定axis=0，沿着行的方向进行累积求和
    cumsum_axis0 = np.cumsum(arr, axis=0)
    print("Cumulative sum along axis 0:\n", cumsum_axis0)

    # 指定axis=1，沿着列的方向进行累积求和
    cumsum_axis1 = np.cumsum(arr, axis=1)
    print("Cumulative sum along axis 1:\n", cumsum_axis1)
