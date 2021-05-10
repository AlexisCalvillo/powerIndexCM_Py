from CMIndex import *
import sympy
from Indexes import *
from time import time
import numpy as np
import math as mt
import multiprocessing as mp
import csv


results =[]
def example(med):
    """
    Precharged example. Calculates and print the results of 
    5-player WVG (Weighted Voting Game) whose weights of 
    [10, 15, 15, 30, 35] repectly.

    Parameters
    -------
    med: number
        Quota of the defined game
    """
    q=med
    vecVot=[10,10,15,30,35]
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

    Parameters
    -------
    VecVot: list
         Vector of player weights

    q: number 
        Percent of the total weight (quota, o to 1)

    Return
    -------
    timeVec: list
        Vector with the calculation time of each one of the 
        indexes

    indexVec: list
        List of list with the value of each index power for all the
        players
    """
    #CM
    timeVec=[0]*5
    indexVec=[0]*5
    iniT=time()
    solutionCM=0
    [matrEcu,  solutionCM, eqcoal]=powerIndexCM(vecVot,q)
    finT=time()
    timeVec[0]=finT-iniT
    if(solutionCM!=0):
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
    Generates a random vector of weights and calculate all the power indexes and 
    return the vector generated the time of excecution, the vector of power, in this order

    Parameters
    -------
    i: number
        Thread number to parallel test
   
    playNum: number
        Numbers of players

    q: number
        Percent of the total weight (quota, o to 1)

    Return
    -------
    vecVot: list
    Vector of weights
 
    timeVec: list
        Vector with the calculation time of each one of the 
        indexes

    indexVec: list
        List of list with the value of each index power for all the
        players

    probVec: list
        List of list with the max and min probability of coalition

    puntPag: list
        List of list with the point which entries are CMIndex and vecVot normalized vector

    """
    vecVot=np.ceil(np.random.uniform(0,100,playNum)).tolist()
    [timeVec, indexVec]=calcIndexes(vecVot,q)

    probVec =[]
    for pI in indexVec:
        probVec.append(evaluaProb(vecVot,pI,q))
    
    puntPag = []
    normVecVot =[]
    tot=np.sum(vecVot)
    for x in vecVot:
        normVecVot.append(x/tot)
    puntPag=[indexVec[0],normVecVot]
    return [vecVot,timeVec,indexVec, probVec, puntPag]

def collect_result(result):
    """
    Collect the results of the paralell test
    """
    global results
    results.append(result)

def test(itNum, playNum, q, prnt=False):
    """
    Generete a number itNum of examples of WVG and calculate power indexes

    Parameters
    -------

    itNum: number
        Number of games to generate en calculates the indexes
    
    playNum: number
        Number of players in the generated games
    
    q: number
        percent of the total weight (quota, o to 1)

    prnt: boolean
        If prnt=True then the results are printed
    """
    vecVot=[]
    timeVec=[]
    probVec =[]
    indexVec=[]
    puntPag = []
    results=[]
    pool = mp.Pool(mp.cpu_count())
    results = pool.starmap_async(genAndCalc,[(i, playNum, q) for i in range(itNum)]).get()
    
    pool.close()

    for x in results:
        vecVot.append(x[0])
        timeVec.append(x[1])
        indexVec.append(x[2])
        probVec.append(x[3])
        puntPag.append(x[4])
    
    if prnt:
        strRes = str(playNum) + "Jug_"+ str(q) + "_cota.csv" 
        myFile = open(strRes, 'w',newline='', encoding='utf-8')
        with myFile:
            writer = csv.writer(myFile)
            for x in results: 
                writer.writerow([x[0],x[1][0],x[2],x[3],x[4]])


def evaluaProb(vecVot, vecPag, q):
    xs=[]
    eqCoal=[]
    nJug=len(vecVot)
    minMaxPag=[]
    matrEcu=calcMatrEcu(vecVot, q)
    if(len(matrEcu)==0):
        return [0, 0]
    [xs,fObj]=calcFObj(matrEcu)
    i=0
    subs=[]
    for k in range(len(vecPag)):
        subs.append((xs[k],vecPag[k]))
    resProb =[]
    for coal in fObj:
        resProb.append(coal.subs(subs))
    minMaxPag.append(np.min(resProb))
    minMaxPag.append(np.max(resProb))

    return minMaxPag    


