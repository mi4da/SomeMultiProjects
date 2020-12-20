import dask.array as da
import numpy as np
from time import time
from dask.distributed import Client


def hit_test(x, y):
    return x ** 2 + y ** 2 < 1


def node_sum(node):
    pass


if __name__ == '__main__':
    st = time()
    N = 100
    chunksize = N // 2
    x_data = np.random.uniform(-1, 1, N)
    y_data = np.random.uniform(-1, 1, N)
    # x = da.from_array(x_data, chunks=chunksize)
    # y = da.from_array(y_data, chunks=chunksize)
    client = Client("172.20.10.3:8786")
    node = client.map(hit_test, x_data, y_data)
    total = client.submit(sum, node)
    pi = 4 * total.result() / N
    print("pi= ", pi)
    et = time()
    print("时间：", (et - st))
