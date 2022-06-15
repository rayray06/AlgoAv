# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 11:58:48 2022

@author: ray-h
"""
from typing import List
from collections import deque
import copy
import numpy as np

def Djiska(WGraph:List[List[float]],nVille:int, u:int , v:int) -> List[int]:
    
    Visited = deque()
    DistStart = [float('inf')]*(nVille-(u+1)) + [0.0] + [float('inf')]*(nVille-(v+1))
    copyWGraph = np.array()
    
    for i in range(len(copyWGraph)):
        for j in range(i+1):
            if(copyWGraph[i,j] == 0):
                copyWGraph[i,j] = float('inf')
                copyWGraph[j,i] = float('inf')
    
    while(v not in Visited):
        MinWeigth = float('inf')
        CurVertice = 0
        for i,value in enumerate(DistStart):
            if(value < MinWeigth) and (i not in Visited):
                MinWeigth = value
                CurVertice = i
        
        