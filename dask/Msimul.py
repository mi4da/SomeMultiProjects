import dask.array as da
import numpy as np
import time
from graphviz import Graph
st = time.time()
N = 100000
chunksize = 1000

x_data = np.random.uniform(-1, 1, N)
y_data = np.random.uniform(-1, 1, N)

x = da.from_array(x_data, chunks=chunksize)
y = da.from_array(y_data, chunks=chunksize)

hit_test = x ** 2 + y ** 2 < 1
hits = hit_test.sum()
pi = 4 * hits / N
et = time.time()
# 在主机里安装以后，记得也要pip install graphviz
# pi.visualize()
print("pi:", pi.compute())
print("时间：", (et - st))
