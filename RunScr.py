from Test import example
import numpy as np
import multiprocessing as mp
a=np.random.uniform(0,100,50)
print(a)
example()
print("Number of processors: ", mp.cpu_count())