#IndexesUtils.py

#Imports
import numpy as np

def calcCombVal(vecVot,nJugTot, votMin):
  #Genera matriz con todas las combinaciones
  MComb=[]
  for i in range(2**nJugTot):
    MComb.append([int(n) for n in bin(i)[2:].zfill(nJugTot)])
  #Genera matriz con todas las combinaciones validas
  MCombVal=[]  
  for x in MComb:
    if(np.dot(x,vecVot)>votMin):
      MCombVal.append(x)
  return MCombVal

def calcMatrEcu(vecVot):
  #Cálcula las coaliciones mínimas y el número de "padres" o formas de llegar a estas
  matrEcu=[]
  nJugTot=len(vecVot)
  votMin=np.sum(vecVot)/2
  MCombVal=calcCombVal(vecVot,nJugTot, votMin)
  
  i=nJugTot
  for x in MCombVal:
    if i>=np.sum(x):i=np.sum(x)
  
  condPar=1
  #for i in range(nJugTot):
  cont=-1 
  while  condPar:
    nivInf=[[0]*nJugTot]
    nivSup=[[0]*nJugTot]
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
            matrEcu[cont][nJugTot]=matrEcu[cont][nJugTot]+1  
    i=i+1  
    
  return matrEcu
