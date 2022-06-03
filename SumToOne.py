#!/usr/bin/python3

from unittest import result
from z3 import *
import argparse
import itertools

def SumToOne(x):
    n=len(x)
    fs=[]
    for i in range(n):
        fs.append(And([x[i]]+[Not(x[ii]) for ii in range(i)]+[Not(x[ii]) for ii in range(i+1,n)]))
    return Or(fs)
    
print("Hello there! This will give you a model of satisfiable for Atmost one.\nGive me the number of Variables")
n=int(input())

variables=[Bool("v_%i"%i) for i in range(n)]

F = SumToOne(variables)

result=Solver()
result.add(F)

if str(result.check()) == "sat":
    m=result.model()
    print(m)
else:
    print("unsat")
