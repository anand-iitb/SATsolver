#!/usr/bin/python3

from unittest import result
from z3 import *
import argparse
import itertools
import time


x=[Bool("x_%i"%i) for i in range(10)]
def sum_to_one( ls ):
    fs=[]
    print(x)
    for i in range(len(ls)):
        fs.append(And([x[i]]+[Not(x[ii]) for ii in range(i)]+[Not(x[ii]) for ii in range(i+1,len(ls))]))
    ors=Or(fs+[And([Not(x[i]) for i in range(len(ls))])])
    # print(ors)
    return ors

# number of variables
n=10

# constructed list of variables
vs = ["a","b","c","d","e","f","g","h","i","j"]

print(vs)

# write function that encodes that exactly one variable is one

    
# call the function
F = sum_to_one(vs)
print (F)

# construct Z3 solver

# add the formula in the solver

# check sat value
result=Solver()
result.add(F)
# result.add(x[0])
result.add(x[1])
if str(result.check()) == "sat":
    m=result.model()
    print(m)

else:
    print("unsat")
