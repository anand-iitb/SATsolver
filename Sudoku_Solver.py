#!/usr/bin/python3

from z3 import *
import argparse
import itertools
import time

problem1 = [
 [ 9, 0, 0,   0, 1, 0,   5, 0, 0],
 [ 7, 0, 0,   8, 0, 3,   0, 0, 2],
 [ 0, 0, 0,   0, 0, 0,   3, 0, 8],

 [ 0, 7, 8,   0, 2, 5,   6, 0, 0],
 [ 0, 0, 0,   0, 0, 0,   0, 0, 0],
 [ 0, 0, 2,   3, 4, 0,   1, 8, 0],

 [ 8, 0, 9,   0, 0, 0,   0, 0, 0],
 [ 5, 0, 0,   4, 0, 1,   0, 0, 9],
 [ 0, 0, 1,   0, 5, 0,   0, 0, 4]
]

problem2 = [
[ 0, 8, 0,   0, 0, 3,   0, 0, 0],
[ 5, 0, 3,   0, 4, 0,   2, 0, 0],
[ 7, 0, 4,   0, 8, 0,   0, 0, 3],

[ 0, 7, 0,   0, 0, 0,   5, 0, 0],
[ 0, 3, 0,   8, 0, 5,   0, 6, 0],
[ 0, 0, 1,   0, 0, 0,   0, 9, 0],

[ 9, 0, 0,   0, 3, 0,   7, 0, 6],
[ 0, 0, 7,   0, 2, 0,   3, 0, 1],
[ 0, 0, 0,   6, 0, 0,   0, 2, 0]
]

problem3 = [
[ 7, 0, 0,   8, 0, 5,   0, 0, 6],
[ 0, 0, 4,   0, 6, 0,   2, 0, 0],
[ 0, 5, 0,   2, 0, 4,   0, 9, 0],

[ 8, 0, 5,   0, 0, 0,   3, 0, 9],
[ 0, 1, 0,   0, 0, 0,   0, 6, 0],
[ 3, 0, 6,   0, 0, 0,   1, 0, 7],

[ 0, 6, 0,   5, 0, 7,   0, 1, 0],
[ 0, 0, 7,   0, 9, 0,   6, 0, 0],
[ 5, 0, 0,   3, 0, 6,   0, 0, 2]
]

problem = problem1

def sum_to_one(ls):
    fs=[]
    for i in range(len(ls)):
        fs.append(And([ls[i]]+[Not(ls[j]) for j in range(len(ls)) if j!=i]))
    ors=Or(fs)
    return ors


s = Solver()
vars=[[[Bool("x_%i_%i_%i" %(i,j,k)) for i in range(9)] for j in range(9)] for k in range(9)]

for i in range(9):
    for j in range(9):
        e=problem[i][j]
        if e!=0:
            s.add([vars[i][j][e-1]])

for i in range(9):
    for j in range(9):
        sum1=[]
        for k in range(9):
            sum1.append(vars[i][j][k])
        s.add(sum_to_one(sum1))

for j in range(9):
    for k in range(9):
        sum2=[]
        for i in range(9):
            sum2.append(vars[i][j][k])
        s.add(sum_to_one(sum2))

for i in range(9):
    for k in range(9):
        sum3=[]
        for j in range(9):
            sum3.append(vars[i][j][k])
        s.add(sum_to_one(sum3))

for k in range(9):
    for i in range(3):
        for j in range(3):
            sum4=[]
            for rr in range(3):
                for cc in range(3):
                    sum4.append(vars[3*i+rr][3*j+cc][k])
            s.add(sum_to_one(sum4))

if s.check() == sat:
    m = s.model()
    for i in range(9):
        if i % 3 == 0 :
            print("|-------|-------|-------|")
        for j in range(9):
            if j % 3 == 0 :
                print ("|", end =" ")
            for k in range(9):
                if is_true(m[vars[i][j][k]]):
                    print("{}".format(k+1), end =" ")
                    break
        print("|")
    print("|-------|-------|-------|")
else:
    print("sudoku is unsat")

# print vars
