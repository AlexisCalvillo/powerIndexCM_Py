import Test as tst
import numpy as np
import multiprocessing as mp
#a=np.random.uniform(0,100,50)
#print(a)
if __name__ == '__main__':
    print("Number of processors: ", mp.cpu_count())
    tst.test(50,6,0.5, True)