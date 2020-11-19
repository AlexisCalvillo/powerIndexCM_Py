#CMIndex

#Imports
import numpy as np
from scipy import optimize

def main(vecVot):
  global eqCoal
  global xs
  matrEcu=calcMatrEcu(vecVot)
  [xs,eqCoal]=calcFObj(matrEcu)
  print(eqCoal)
  bnd=()
  x0=[1/len(vecVot)]*len(vecVot)
  const=[]
  for i in range(len(matrEcu[0])-1):
    bnd=bnd+((0,1),)
  i=0
  nConst=len(matrEcu)-1
  for j in range(nConst):
    exec("""def constr"""+str(j+1)+"""(x0):
      equat=0  
      subst=[]
      equat=eqCoal["""+str(0)+"""]-eqCoal["""+str(j+1)+"""]
      for k in range(len(x0)):
        subst.append((xs[k],x0[k]))
      return -equat.subs(subst)""")
    exec("""const.append({'type':'ineq','fun': constr"""+str(j+1)+"""})""")
  con1={'type':'eq','fun':constraint1}
  const.append(con1)
  print(matrEcu)
  solution=optimize.minimize(objetive,x0,method='SLSQP',bounds=bnd,constraints=const,options={'maxiter':3e7,'ftol':1e-08})
  return [matrEcu, solution, eqCoal]
