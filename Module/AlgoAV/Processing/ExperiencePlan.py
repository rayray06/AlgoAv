from pulp import *
import numpy as np
import math

def Borne(CitySize,WMat,MaxTime,StartingVertice):
    StateMat = {}
    OrderList = {}
    for t in range(MaxTime):
        for i in range(CitySize):
            for j in range(CitySize): # create a binary variable
                StateMat[t ,i, j] = LpVariable('x|{},{},{}|'.format(t, i, j),lowBound=0,upBound=1, cat=const.LpBinary)

    for i in range(CitySize): # create a order variable
        if(i != StartingVertice):
            OrderList[i] = LpVariable('u|{}|'.format(i),lowBound=1,upBound=CitySize, cat=const.LpInteger)
        else :
            OrderList[i] = 1

    
    # probleme
    prob = LpProblem("Shortest_Delivery", LpMinimize)

    # fonction objective
    cost = lpSum([[[ WMat[t][n][m]*StateMat[t,n, m] for m in range(CitySize)] for n in range(CitySize)]for t in range(MaxTime)])
    prob += cost

    # contrainte
    for n in range(CitySize) :
        prob += lpSum([[ StateMat[t,n,m] for m in range(CitySize)]for t in range(MaxTime)]) == 1,"All entered constraint "+str(n)
        prob += lpSum([[ StateMat[t,m,n] for m in range(CitySize)]for t in range(MaxTime)]) == 1,"All exited constraint "+str(n)

    prob += lpSum([ StateMat[0,StartingVertice,m] for m in range(CitySize)]) == 1,"Start at Time 0 Consistency"+str(t)

    for i in range(CitySize) :
        for j in range(CitySize):
            if i != j and (i != 0 and j != 0):
                prob += ( (OrderList[i] - OrderList[j]) + (CitySize - 1)*lpSum([StateMat[t,i, j] for t in range(MaxTime)]) ) <= (CitySize-2),"Start No sub loop "+str(i)+","+str(j)

    for t in range(MaxTime):
        for i in range(CitySize):
            for j in range(CitySize): # create a binary variable
                if(j != StartingVertice):
                    prob += StateMat[t,i,j] <= lpSum([StateMat[(t+math.floor(WMat[t][i][j]))%MaxTime,j,n] for n in range(CitySize)]),"No waiting Constraint"+str(i)+","+str(j)+","+str(t)
    
    prob += lpSum([[ StateMat[t,m,m] for m in range(CitySize)] for t in range(MaxTime)]) == 0,"No loop constraint"

    prob.solve(PULP_CBC_CMD(msg=0,timeLimit=MaxTime*CitySize*1/7))
    print(LpStatus[prob.status])
    return prob.objective.value() if (LpStatus[prob.status] == "Optimal") else None

