from CMIndex import *
import sympy
from Indexes import *
from time import time
import numpy as np
import math as mt
import multiprocessing as mp
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
    indexVec[0]=solutionCM.x
    
    #Holler Packel
    iniT=time()
    solutionHP=hollPack(vecVot,q)
    finT=time()
    timeVec[3]=finT-iniT
    indexVec[3]=solutionCM.x
    
    #Shapley
    iniT=time()
    solutionSH=shapley(vecVot,q)
    finT=time()
    timeVec[1]=finT-iniT
    indexVec[1]=solutionCM.x
    
    #DeeganPackel
    iniT=time()
    solutionDP=deegPack(vecVot,q)
    finT=time()
    timeVec[4]=finT-iniT
    indexVec[4]=solutionCM.x
    
    #Banzhaf
    iniT=time()
    solutionB=banzhaf(vecVot,q)
    finT=time()
    timeVec[2]=finT-iniT
    indexVec[2]=solutionCM.x

    return [timeVec, indexVec]
    
    
def genAndCalc(playNum,q):
    """
    Generates a random vector of weights and calculate all the indexes of power an return the vector generated
    the time of excecution and the vector of power in this order

    playNum: Numbers of players
    q: percent of the total weight (quota, o to 1)
    """
    vecVot=mt.ceil(np.random.Uniform(0,1,playNum)*100)
    [timeVec, indexVec]=calcIndexes(vecVot,q)
    return [vecVot,timeVec,indexVec]



def test(itNum, playNum, q):
    """
    Generete a number itNum of examples of WVG and calculate power indexes

    playNum: Number of players to generate the players vector weights
    itNum: Vector of player weight
    q: percent of the total weight (quota, o to 1)
    """
    pool = mp.Pool(mp.cpu_count())
    inputsN = range(itNum)
    for i in range(itNum):
        [vecVot,timeVec,indexVec] = pool.map_async(genAndCalc, args=(playNum,q))
    
    print(vecVot)
    print(timeVec)
    print(indexVec)
       


