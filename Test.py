from CMIndex import *
import sympy
from Indexes import *
from time import time
import numpy as np
import math as mt
import multiprocessing as mp

results =[]
def example():
    q=.50
    vecVot=[20,25,25,30]
    votMin=sum(vecVot)*q
    [matrEcu,  solutionCM, eqCoal]=powerIndexCM(vecVot,q)
    solutionHP=hollPack(vecVot,q)
    solutionSH=shapley(vecVot,q)
    solutionDP=deegPack(vecVot,q)
    solutionB=banzhaf(vecVot,q)
    print("Vector de votantes")
    print(vecVot)
    print("Cota")
    print(votMin)
    print("CM value V1")
    print(solutionCM)
    print("Shapley")
    print(solutionSH)
    print("Banzhaf")
    print(solutionB)
    print("Deegan-Packel")
    print(solutionDP)
    print("Holler-Packel")
    print(solutionHP)

def calcIndexes(vecVot, q):
    """
    Calculate the power indexes of a given game and return the excecution
    time

    VecVot: Vector of player weights
    q: percent of the total weight (quota, o to 1)

    """
    #CM
    timeVec=[0]*5
    indexVec=[0]*5
    iniT=time()
    [matrEcu,  solutionCM, eqcoal]=powerIndexCM(vecVot,q)
    finT=time()
    timeVec[0]=finT-iniT
    indexVec[0]=solutionCM.x.tolist()
    
    #Holler Packel
    iniT=time()
    solutionHP=hollPack(vecVot,q)
    finT=time()
    timeVec[3]=finT-iniT
    indexVec[3]=solutionHP
    
    #Shapley
    iniT=time()
    solutionSH=shapley(vecVot,q)
    finT=time()
    timeVec[1]=finT-iniT
    indexVec[1]=solutionSH
    
    #DeeganPackel
    iniT=time()
    solutionDP=deegPack(vecVot,q)
    finT=time()
    timeVec[4]=finT-iniT
    indexVec[4]=solutionDP

    #Banzhaf
    iniT=time()
    solutionB=banzhaf(vecVot,q)
    finT=time()
    timeVec[2]=finT-iniT
    indexVec[2]=solutionB

    return [timeVec, indexVec]
    
    
def genAndCalc(i,playNum,q):
    """
    Generates a random vector of weights and calculate all the indexes of power an return the vector generated
    the time of excecution and the vector of power in this order

    playNum: Numbers of players
    q: percent of the total weight (quota, o to 1)
    """
    vecVot=np.ceil(np.random.uniform(0,100,playNum)).tolist()
    [timeVec, indexVec]=calcIndexes(vecVot,q)
    return [vecVot,timeVec,indexVec]

def collect_result(result):
    global results
    results.append(result)

def test(itNum, playNum, q, prnt):
    """
    Generete a number itNum of examples of WVG and calculate power indexes

    playNum: Number of players to generate the players vector weights
    itNum: Vector of player weight
    q: percent of the total weight (quota, o to 1)
    """
    vecVot=[]
    timeVec=[]
    indexVec=[]
    results=[]
    pool = mp.Pool(mp.cpu_count())
    results = pool.starmap_async(genAndCalc,[(i, playNum, q) for i in range(itNum)]).get()
    
    pool.close()

    for x in results:
        vecVot.append(x[0])
        timeVec.append(x[1])
        indexVec.append(x[2])
    
    if prnt: 
        for x in range(itNum):
            print("Vector de votantes, tiempos y índices" + str(x))
            print(vecVot[x])
            print(timeVec[x])
            print("CM" + str(indexVec[x][0]))
            print("SH" + str(indexVec[x][1]))
            print("B" + str(indexVec[x][2]))
            print("HP" + str(indexVec[x][3]))
            print("DP" + str(indexVec[x][4]))
        


