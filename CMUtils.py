#CMUtils.py

#Imports
import numpy as np
from sympy import *

def prob(pag,njug):
  return pag if (njug==1) else  1-((1-pag))**(njug-1)

def probCo(pag,nJug): 
  pJug=prob(pag,nJug)
  #Devuelve la lista de funciones de cada uno de los jugadores de la coalicón
  return pJug

def calcFObj (matrEcu):
  xs=[]
  nJug=len(matrEcu[0])-1
  numCol=len(matrEcu)
  for i in range(nJug):
    #Se calcula cada una de las funciones
    xs.append(symbols("x"+str(i+1)))
  eqCoal=[]
  eqInd=[]
  for i in range (numCol):
    eqAux=1
    vecAux=matrEcu[i]
    nJugCol=np.sum(vecAux[0:nJug])
    for j in range (nJug):
      if matrEcu[i][j]==1:
        eqInd.append(probCo(xs[j],nJugCol))
        eqAux=eqAux*probCo(xs[j],nJugCol)
    eqCoal.append((eqAux)**(1/nJugCol))#*vecAux[nJug])
  return [xs,eqCoal]


def objetive(x0):
  subst=[]
  for i in range(len(x0)):
    subst.append((xs[i],x0[i]))
  return -eqCoal[0].subs(subst)


def constraint1(x0):
  sum=1
  for i in x0:
    sum=sum-i
  return sum
