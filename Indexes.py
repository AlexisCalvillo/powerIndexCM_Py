#indexes.py

#Imports
import numpy as np
import itertools as it
import math as mt
from IndexesUtils import *

#Índice de poder de shapley
def shapley(vecVot,q):
  nJugTot=len(vecVot)
  votMin=np.sum(vecVot)*q
  #Calcula todas las permutaciones
  permVot=it.permutations([i for i in range(nJugTot)], nJugTot)
  vecAp=[0]*nJugTot
  vecPag=[0]*nJugTot
  for x in permVot:
    acum=0
    i=0
    while i<nJugTot and acum<=votMin:
      acum=acum+vecVot[x[i]]
      i=i+1
    vecAp[x[i-1]]=vecAp[x[i-1]]+1
  posibl=mt.factorial(nJugTot)
  for i in range(nJugTot):
    vecPag[i]=vecAp[i]/posibl
  return vecPag
    
#Índice de poder banzhaf
def banzhaf(vecVot,q):
  nJugTot=len(vecVot)
  votMin=np.sum(vecVot)*q
  #Genera matriz con todas las combinaciones
  MComb=[]
  for i in range(2**nJugTot):
    MComb.append([int(n) for n in bin(i)[2:].zfill(nJugTot)])
  vecPag=[0]*nJugTot
  for x in MComb:
    if (np.dot(x,vecVot)>votMin):
      for y in range(nJugTot):
        xaux=x[:]
        xaux[y]=0
        if (np.dot(xaux,vecVot)<=votMin):
          vecPag[y]=vecPag[y]+1
  tot=np.sum(vecPag)
  for i in range(nJugTot):
    vecPag[i]=vecPag[i]/tot
  return vecPag

#Índice de poder Deegan-Packel
def deegPack(vecVot,q):
  nJugTot=len(vecVot)
  vecPag=[0]*nJugTot
  votMin=np.sum(vecVot)*q
  #Cálcula el conjunto de coaliciones mínimas
  matrEcu=calcMatrEcu(vecVot,q)
  #Cardinalidad del conjunto
  cardWm=len(matrEcu)
  for i in range(nJugTot):
    for j in range(cardWm):
      if(matrEcu[j][i]==1):
        vecPag[i]=vecPag[i]+1/np.sum(matrEcu[j][0:nJugTot])
    vecPag[i]=vecPag[i]/cardWm
  return vecPag

#índice de poder Holler-Packel
def hollPack(vecVot,q):
  nJugTot=len(vecVot)
  vecPag=[0]*nJugTot
  votMin=np.sum(vecVot)*q
  #Cálcula el conjunto de coaliciones mínimas
  matrEcu=calcMatrEcu(vecVot,q)
  #Cardinalidad del conjunto
  cardWm=len(matrEcu)
  for i in range(nJugTot):
    for j in range(cardWm):
      if(matrEcu[j][i]==1):
        vecPag[i]=vecPag[i]+1
  
  tot=np.sum(vecPag)
  for i in range(nJugTot):
    vecPag[i]=vecPag[i]/tot
  return vecPag
