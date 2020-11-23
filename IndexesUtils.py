#IndexesUtils.py

#Imports
import numpy as np

def calcCombVal(vecVot,nPlayTot, votMin):
  #Genera matriz con todas las combinaciones
  """
    Generate a matrix with all the posibble combinations 
    
    nPlayTot: Number of players
    VecVot: Vector of player weights
  """
  MComb=[]
  for i in range(2**nPlayTot):
    MComb.append([int(n) for n in bin(i)[2:].zfill(nPlayTot)])
  #Genera matriz con todas las combinaciones validas
  MCombVal=[]  
  for x in MComb:
    if(np.dot(x,vecVot)>votMin):
      MCombVal.append(x)
  return MCombVal

def calcMatrEcu(vecVot, q):
  """
    Cauclates the set of minimal winning coalitions and the number of paths to reach that coalition

    VecVot: Vector of player weights
    q: percent of the total weight (quota, o to 1)
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
