#CMIndex

#Imports
import numpy as np
from scipy import optimize
from IndexesUtils import *
from sympy import symbols
import numpy as np
from  sympy import symbols

eqCoal=[]
xs=[]
fObj=[]
const=[]

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
  eqC=[]
  eqInd=[]
  for i in range (numCol):
    eqAux=1
    vecAux=matrEcu[i]
    nJugCol=np.sum(vecAux[0:nJug])
    for j in range (nJug):
      if matrEcu[i][j]==1:
        eqInd.append(probCo(xs[j],nJugCol))
        eqAux=eqAux*probCo(xs[j],nJugCol)
    eqC.append((eqAux)**(1/nJugCol))#*vecAux[nJug])
  return [xs,eqC]


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

def powerIndexCM(vecVot, q):
  """
  Calculates the power index CM 
  vecVot: vector of player weights 
  q: percent of the total weight (quota, o to 1)
  """
  global xs
  global eqCoal
  matrEcu=calcMatrEcu(vecVot, q)
  [xs,eqCoal]=calcFObj(matrEcu)
  #print(eqCoal)
  bnd=()
  x0=[1/len(vecVot)]*len(vecVot)
  for i in range(len(matrEcu[0])-1):
    bnd=bnd+((0,1),)
  i=0
  nConst=len(matrEcu)-1
  #print(eqCoal)
  for j in range(nConst):
    exec("""def constr"""+str(j+1)+"""(x0):
      equat=0  
      subst=[]
      equat=eqCoal["""+str(0)+"""]-eqCoal["""+str(j+1)+"""]
      for k in range(len(x0)):
        subst.append((xs[k],x0[k]))
      return -equat.subs(subst)
const.append({'type':'ineq','fun': constr"""+str(j+1)+"""})""",{'eqCoal':eqCoal, 'const':const, 'xs':xs})
  con1={'type':'eq','fun':constraint1}
  const.append(con1)
  solution=optimize.minimize(objetive,x0,method='SLSQP',bounds=bnd,constraints=const,options={'maxiter':3e7,'ftol':1e-08})
  print(solution)
  return [matrEcu, solution, eqCoal]
