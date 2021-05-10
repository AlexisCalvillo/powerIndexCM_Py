#IndexesUtils.py

#Imports
import numpy as np

def calcCombVal(vecVot,nPlayTot, votMin):
  """
    Generate a matrix with all the valid combinations 
    
    Paramters
    -------
    nPlayTot: number
      Number of players 
    
    VecVot: list 
      Vector of player weights
    
    votMin: number
      Quota of the game en terms of wwights

    Return
    -------
    MCombVal: list
      Matrix representatión with all the valid player
      combinations (>votMin)
    """

  MComb=[]
  for i in range(2**nPlayTot):
    MComb.append([int(n) for n in bin(i)[2:].zfill(nPlayTot)])
  #Generates the matrix with all the valid combinations
  MCombVal=[]  
  for x in MComb:
    if(np.dot(x,vecVot)>votMin):
      MCombVal.append(x)
  return MCombVal

def calcMatrEcu(vecVot, q):
  """
  Calculates the set of minimal winning coalitions and the number of 
  "parent" games

  Parameters
  -------
  vecVot: list
    Vector of weights
  
  q: number
    Percent of the total weight (quota, o to 1)

  Return
  -------
  matrEcu: list
    Matrix representatión of the minimal winning coalition and
    the number of parent games.
  """

  matrEcu=[]
  nPlayTot=len(vecVot)
  votMin=np.sum(vecVot)*q
  MCombVal=calcCombVal(vecVot,nPlayTot, votMin)
  
  i=nPlayTot
  for x in MCombVal:
    if i>=np.sum(x):i=np.sum(x)
  
  condPar=1
  cont=-1 
  while  condPar:
    nivInf=[[0]*nPlayTot]
    nivSup=[[0]*nPlayTot]
    for x in MCombVal:
      if(np.sum(x)==i+1):
        nivSup.append(x)
      if(np.sum(x)==i):
        nivInf.append(x)
    if len(nivInf)==1:condPar=0
    #Obtiene la matriz con las coaliciones hojas y el número de ramas de las que se derivan
    
    for yInf in nivInf:
      aux=0
      for ySup in nivSup:
        if(np.dot(yInf,ySup)==i):
          if ySup in MCombVal : MCombVal.remove(ySup) 
          if(aux==0):
            matrEcu.append(yInf+[1])
            aux=1
            cont=cont+1
          else:
            matrEcu[cont][nPlayTot]=matrEcu[cont][nPlayTot]+1  
    i=i+1  
    
  return matrEcu
