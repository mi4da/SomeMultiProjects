from dask.distributed import Client
from time import time
import dask.array as da

def square(x):
    return x**2

if __name__ == '__main__':
    MAX = 100
    st = time()
    client = Client('172.20.10.3:8786')
    A = client.map(square,range(MAX))
    print('typeA:',type(A))
    total = client.submit(sum,A)
    # A.visualize()
    print(total.result())
    et = time()
    print("时间：",(et - st))
