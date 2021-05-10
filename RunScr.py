import Test as tst
import numpy as np
import multiprocessing as mp
import IndexesUtils as iu
import CMIndex
from time import time 
#a=np.random.uniform(0,100,50)
#print(a)
if __name__ == '__main__':
    print("Number of processors: ", mp.cpu_count())
    
    #tst.example(.50)
    #print(iu.
    #
    #calcCombVal([10,10,15,30,35],5,50))
    #N=1000
    #nJug=12
    #tst.test(10,3,.33,True)
    #initt=time()
    #i=1  
    #for x in range(5):
    #    tst.test(N,nJug,0.20*i-0.05,True)
    #    i=i+1
    #fintt=time()
    #print("Se tardó en correr las " + str(N*5) + " pruebas para " + str(nJug) + " jugadores "+ str(fintt-initt))
    print(CMIndex.powerIndexCM([20,25,25,30],0.5))