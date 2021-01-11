import dask.array as da
import numpy as np
from time import time
from dask.distributed import Client


def hit_test(N, HiddenVar):
    # 不管有多少个元素，一律生成10个节点，每个节点n个数据
    n = N / 10
    x = np.random.uniform(-1, 1, n)
    y = np.random.uniform(-1, 1, n)
    z = x ** 2 + y ** 2 < 1
    # 返回统计平方和小于1的个数
    return z.sum()


if __name__ == '__main__':
    """先计算"""
    st = time()
    N = 10000
    # x_data = np.random.uniform(-1, 1, N)
    # y_data = np.random.uniform(-1, 1, N)
    # x = da.from_array(x_data, chunks=chunksize)
    # y = da.from_array(y_data, chunks=chunksize)
    client = Client("172.20.10.3:8786")
    node = client.map(hit_test, N, range(N // 10))
    total = client.submit(sum, node)
    pi = 4 * total.result() / N
    print("pi= ", pi)
    et = time()
    print("时间：", (et - st))
