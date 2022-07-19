from z3 import *
import sys

input=open(sys.argv[1],"r")
lines=input.readlines()
r,k=lines[0].split(",")
r=int(r)
k=int(k)
c=r
cc=0
Red_car=[]
Horizontal_car=[]
Vertical_car=[]
Mines=[]

for line in lines:
    x=line.split(",")
    x[0]=int(x[0])
    x[1]=int(x[1])
    if(cc==0):
        cc=0
    elif(cc==1):
        Red_car.append(x[0]+1)
        Red_car.append(x[1]+1)
    elif(x[0]==0):
        Vertical_car.append([x[1]+1,int(x[2])+1])
    elif(x[0]==1):
        Horizontal_car.append([x[1]+1,int(x[2])+1])
    elif(x[0]==2):
        Mines.append([x[1]+1,int(x[2])+1])
    cc+=1

H=[[[Bool("h_%i_%i_%i"%(ii,jj,kk)) for kk in range(k+1)]for jj in range(c+1)] for ii in range(r+1)]
V=[[[Bool("v_%i_%i_%i"%(ii,jj,kk)) for kk in range(k+1)]for jj in range(c+1)] for ii in range(r+1)]
R=[[[Bool("r_%i_%i_%i"%(ii,jj,kk)) for kk in range(k+1)]for jj in range(c+1)] for ii in range(r+1)]
M=[[Bool("m_%i_%i"%(ii,jj)) for jj in range(c+1)] for ii in range(r+1)]

S=Solver()

#initial condition for horizontal car
for ii in range(1,r+1):
    for jj in range(c+1):
        if([ii,jj] in Horizontal_car):
            # print("h",ii,jj)
            S.add(H[ii][jj][0])
        else:
            S.add(Not(H[ii][jj][0]))

#initial condition for vertical car
for ii in range(r+1):
    for jj in range(1,c+1):
        if([ii,jj] in Vertical_car):
            # print("v",ii,jj)
            S.add(V[ii][jj][0])
        else:
            S.add(Not(V[ii][jj][0]))               

#initial condition for Red car
for ii in range(1,r+1):
    for jj in range(c+1):
        if(Red_car[0]==ii and Red_car[1]==jj):
            S.add(R[ii][jj][0])
        else:
            S.add(Not(R[ii][jj][0]))

#initial condition for mines
for ii in range(r+1):
    for jj in range(c+1):
        if([ii,jj] in Mines):
            S.add(M[ii][jj])
        else:
            S.add(Not(M[ii][jj]))

#boundary horizontal
for ii in range(1,r+1):
    for kk in range(1,k+1):
        S.add(Not(H[ii][0][kk]))
        S.add(Not(H[ii][c][kk]))
            

#boundary vertical
for jj in range(1,c+1):
    for kk in range(1,k+1):
        S.add(Not(V[r][jj][kk]))
        S.add(Not(V[0][jj][kk]))

#boundary red
for ii in range(1,r+1):
    for kk in range(1,k+1):
        S.add(Not(R[ii][0][kk]))
        S.add(Not(R[ii][c][kk]))

#clear cell checker
C=[[[And([Not(M[ii][jj])]+[Not(R[ii][jj][kk])]+[Not(R[ii][jj-1][kk])]+[Not(H[ii][jj][kk])]+[Not(H[ii][jj-1][kk])]+[Not(V[ii][jj][kk])]+[Not(V[ii-1][jj][kk])]) for kk in range(k+1)] for jj in range(1,c+1)] for ii in range(1,r+1)]
# print(C[0][0][5])

#red car moves right
for kk in range(k):
        for jj in range(1,c-1):
            for ii in range(1,r+1):
                S.add(Or([Not(R[ii][jj][kk])]+[Not(R[ii][jj+1][kk+1])]+[C[ii-1][jj+1][kk]]))
                #print([Not(R[ii][jj][kk])]+[Not(R[ii][jj+1][kk+1])]+[C[ii-1][jj+1][kk]])
                # S.add(FF)

#red car moves left
for kk in range(k):
        for jj in range(2,c):
            for ii in range(1,r+1):
                S.add(Or([Not(R[ii][jj][kk])]+[Not(R[ii][jj-1][kk+1])]+[C[ii-1][jj-2][kk]]))
                # S.add(FF)

#horizonal car moves right
for kk in range(k):
        for jj in range(1,c-1):
            for ii in range(1,r+1):
                S.add(Or([Not(H[ii][jj][kk])]+[Not(H[ii][jj+1][kk+1])]+[C[ii-1][jj+1][kk]]))

#horizonal car moves left
for kk in range(k):
        for jj in range(2,c):
            for ii in range(1,r+1):
                S.add(Or([Not(H[ii][jj][kk])]+[Not(H[ii][jj-1][kk+1])]+[C[ii-1][jj-2][kk]]))

#vertical car moves up
for kk in range(k):
        for jj in range(1,c+1):
            for ii in range(2,r):
                S.add(Or([Not(V[ii][jj][kk])]+[Not(V[ii-1][jj][kk+1])]+[C[ii-2][jj-1][kk]]))

#vertical car moves down
for kk in range(k):
        for jj in range(1,c+1):
            for ii in range(1,r-1):
                S.add(Or([Not(V[ii][jj][kk])]+[Not(V[ii+1][jj][kk+1])]+[C[ii+1][jj-1][kk]]))

#red car false in other rows
for kk in range(1,k+1):
    for ii in range(1,r+1):
        for jj in range(1,c):
            if(ii!=Red_car[0]):
                S.add(Not(R[ii][jj][kk]))

#in each move exactly one car moves
for kk in range(0,k):
    ll=[And([R[Red_car[0]][jj][kk],R[Red_car[0]][jj+1][kk+1]]) for jj in range(1,c-1)] + [And([R[Red_car[0]][jj][kk],R[Red_car[0]][jj-1][kk+1]]) for jj in range(2,c)]
    ll += [And([H[ii][jj][kk],H[ii][jj+1][kk+1]]) for ii in range(1,r+1) for jj in range(1,c-1)] + [And([H[ii][jj][kk],H[ii][jj-1][kk+1]]) for ii in range(1,r+1) for jj in range(2,c)]
    ll += [And([V[ii][jj][kk],V[ii+1][jj][kk+1]]) for ii in range(1,r-1) for jj in range(1,c+1)] + [And([V[ii][jj][kk],V[ii-1][jj][kk+1]]) for ii in range(2,r) for jj in range(1,c+1)]
    S.add(AtLeast(*ll,1),AtMost(*ll,1))

#number of all cars remain same
for kk in range(k+1):
    dr=[R[Red_car[0]][jj][kk] for jj in range(1,c)]
    dh=[H[ii][jj][kk] for ii in range(1,r+1) for jj in range(1,c)]
    dv=[V[ii][jj][kk] for ii in range(1,r) for jj in range(1,c+1)]
    S.add(AtLeast(*dr,1),AtMost(*dr,1))
    S.add(AtLeast(*dh,len(Horizontal_car)),AtMost(*dh,len(Horizontal_car)))
    S.add(AtLeast(*dv,len(Vertical_car)),AtMost(*dv,len(Vertical_car)))

#final goal to achieve
S.add(Or([R[Red_car[0]][c-1][kk] for kk in range(k+1)]))

#constraining the sequential moves
for kk in range(k):
    l = [Implies(R[Red_car[0]][jj][kk],Or([R[Red_car[0]][jj-1][kk+1],R[Red_car[0]][jj][kk+1],R[Red_car[0]][jj+1][kk+1]])) for jj in range(1,c)]
    l += [Implies(H[ii][jj][kk],Or([H[ii][jj-1][kk+1],H[ii][jj][kk+1],H[ii][jj+1][kk+1]])) for ii in range(1,r+1) for jj in range(1,c)]
    l += [Implies(V[ii][jj][kk],Or([V[ii-1][jj][kk+1],V[ii][jj][kk+1],V[ii+1][jj][kk+1]])) for ii in range(1,r) for jj in range(1,c+1)]
    S.add(l)

if(str(S.check())=="unsat"):
    print("unsat",end="")
else:
    m=S.model()
    for kk in range(k):
        repeat=""
        if(m.evaluate(R[Red_car[0]][c-1][kk])):
            if(m.evaluate(R[Red_car[0]][c-1][0])):
                # print(f"{Red_car[0]-1},{c-2}")
                pass
            break
        for ii in range(1,c+1):
            for jj in range(1,r+1):
                if(m.evaluate(C[ii-1][jj-1][kk]) and not m.evaluate(C[ii-1][jj-1][kk+1])):
                    if(m.evaluate(R[ii][jj][kk+1])):
                        print(f"{ii-1},{jj}")
                    elif(m.evaluate(R[ii][jj-1][kk+1])):
                        print(f"{ii-1},{jj-2}")
                    elif(m.evaluate(H[ii][jj][kk+1])):
                        print(f"{ii-1},{jj}")
                    elif(m.evaluate(H[ii][jj-1][kk+1])):
                        print(f"{ii-1},{jj-2}")
                    elif(m.evaluate(V[ii][jj][kk+1])):
                        print(f"{ii},{jj-1}")
                    elif(m.evaluate(V[ii-1][jj][kk+1])):
                        print(f"{ii-2},{jj-1}")
input.close()


