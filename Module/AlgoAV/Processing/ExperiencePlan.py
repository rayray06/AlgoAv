from pulp import *
import numpy as np
import math

def Borne(CitySize,WMat):
    StateMat = {}
    OrderList = {}
    for i in range(CitySize):
        for j in range(CitySize): # create a binary variable
            StateMat[i, j] = LpVariable('x{},{}'.format(i, j),lowBound=0,upBound=1, cat=const.LpBinary)

    for i in range(CitySize): # create a binary variable
        OrderList[i] = LpVariable('u{}'.format(i),lowBound=1,upBound=CitySize, cat=const.LpInteger)

    
    # probleme
    prob = LpProblem("Shortest_Delivery", LpMinimize)

    # fonction objective
    cost = lpSum([[ WMat[n][m]*StateMat[n, m] for m in range(CitySize)] for n in range(CitySize)])
    prob += cost

    # contrainte
    for n in range(CitySize) :
        prob += lpSum([ StateMat[n,m] for m in range(CitySize)]) == 1,"All entered constraint "+str(n)
        prob += lpSum([ StateMat[m,n] for m in range(CitySize)]) == 1,"All exited constraint "+str(n)

    for i in range(CitySize) :
        for j in range(CitySize):
            if i != j and (i != 0 and j != 0):
                prob += OrderList[i] - OrderList[j] <= CitySize * (1 - StateMat[i, j]) - 1

    

    cont2 = lpSum([ StateMat[m,m] for m in range(CitySize)]) == 0,"No loop constraint"
    prob += cont2

    prob.solve(PULP_CBC_CMD(msg=0,timeLimit=math.ceil(CitySize*60*1/4)))
    print(LpStatus[prob.status])
    return prob.objective.value() if (LpStatus[prob.status] == "Optimal") else None

