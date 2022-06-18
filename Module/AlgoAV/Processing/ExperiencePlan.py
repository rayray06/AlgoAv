from pulp import *
import numpy as np
def Borne(CitySize,WMat):
    StateMat = {}
    for i in range(CitySize):
        for j in range(CitySize): # create a binary variable
            StateMat[i, j] = LpVariable('x{},{}'.format(i, j), cat='Binary')
    
    # probleme
    prob = LpProblem("Shortest_Delivery", LpMinimize)

    # fonction objective
    cost = lpSum([[ WMat[n][m]*StateMat[n, m] for m in range(CitySize)] for n in range(CitySize)])
    prob += cost

    # contrainte
    for n in range(CitySize) :
        prob += lpSum([ StateMat[n,m] for m in range(CitySize)]) == 1,"One place constraint "+str(n)

    cont2 = lpSum([ StateMat[m,m] for m in range(CitySize)]) == 0,"No loop constraint"
    prob += cont2

    prob.solve()
    return value(prob.objective) if (LpStatus[prob.status] == "Optimal") else None

