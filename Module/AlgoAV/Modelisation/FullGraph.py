# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 11:58:48 2022

@author: ray-h
"""

from typing import List
from collections import deque
import copy
import numpy as np
from AlgoAV.Generation.GraphGen import WeigthSet, GraphGen

def Djiska(WGraph:List[List[float]],nVille:int, u:int , v:int) -> tuple[float,deque[int]]:
    
    Visited = deque()
    DistStart = [float('inf')]*(u) + [0.0] + [float('inf')]*(nVille-(u+1))
    copyWGraph = copy.deepcopy(WGraph)
    
    for i in range(len(copyWGraph)):
        for j in range(i+1):
            if(copyWGraph[i][j] == 0):
                copyWGraph[i][j] = float('inf')
                copyWGraph[j][i] = float('inf')
    
    while(v not in Visited):
        MinWeigth = float('inf')
        CurVertice = 0
        for i,value in enumerate(DistStart):
            if(value < MinWeigth) and (i not in Visited):
                MinWeigth = value
                CurVertice = i
        
        Visited.append(CurVertice)
 
        for i in range(nVille):
            if i not in Visited:
                curValue = DistStart[CurVertice] + copyWGraph[CurVertice][i]
                if(curValue < DistStart[i]):
                    DistStart[i] = curValue
                copyWGraph[CurVertice][i] = curValue
                copyWGraph[i][CurVertice]
        
    Path = deque((v,))
    cur = v
    while(u not in Path):
        MinWeigth = float('inf')
        CurVertice = 0
        for i,value in enumerate(copyWGraph[cur]):
            if(value < MinWeigth) and (i not in Path):
                MinWeigth = value
                CurVertice = i
        cur = CurVertice
        Path.appendleft(cur)
    return (DistStart[v],Path)