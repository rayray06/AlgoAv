# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 11:58:48 2022

@author: ray-h
"""

from typing import List,Tuple,Deque
from collections import deque
import random
import copy
import numpy as np
from AlgoAV.Generation.GraphGen import WeigthSet, GraphGen

def Djiska(WGraph:List[List[float]],nVille:int, u:int , v:int) -> Tuple[float,Deque[int]]:
    """
    Do the Dijkstra's algorithm to find the shortest route between from the vertice u to v    

    Parameters
    ----------
    WGraph : List[List[float]]
        The weigth array use to determine the best path
    nVille : int
        The number of cities for our graph
    u : int
        The start vertice for the path
    v : int
        The end vertice for the path

    Returns
    -------
    Tuple[float,Deque[int]]
        A tuple containing the total size of the shortest path at index 0 and A queu representing the corresponding path (including the start and end vertice)

    """
    Visited = deque() #Priority queu of the already visited vertice
    DistStart = [float('inf')]*(u) + [0.0] + [float('inf')]*(nVille-(u+1))#Array representing each vertice distance with the vertice u
    copyWGraph = copy.deepcopy(WGraph)#A copy of the weigthed array to process the algoritm
    
    for i in range(len(copyWGraph)):#initialise every non-existing edge has infinite 
        for j in range(i+1):
            if(copyWGraph[i][j] == 0):
                copyWGraph[i][j] = float('inf')
                copyWGraph[j][i] = float('inf')
    
    while(v not in Visited):#Cycle through the shortest path from u and the already visited vertice until we visit the vertice v
        MinWeigth = float('inf')
        CurVertice = 0
        for i,value in enumerate(DistStart): #We search the accessible vertice for the closer one
            if(value < MinWeigth) and (i not in Visited):
                MinWeigth = value
                CurVertice = i
        
        Visited.append(CurVertice) # The vertice is then  considered visited
 
        for i in range(nVille):# We update every neighbour edge and vertice from visited vertice
            if i not in Visited:
                curValue = DistStart[CurVertice] + copyWGraph[CurVertice][i]
                if(curValue < DistStart[i]):
                    DistStart[i] = curValue
                copyWGraph[CurVertice][i] = curValue
                copyWGraph[i][CurVertice]
        
    Path = deque((v,))
    cur = v
    while(u not in Path):# We cycle through the shortest edge from ou vertice v to backtrack to our vertice u
        MinWeigth = float('inf')
        CurVertice = 0
        for i,value in enumerate(copyWGraph[cur]):
            if(value < MinWeigth) and (i not in Path):
                MinWeigth = value
                CurVertice = i
        cur = CurVertice
        Path.appendleft(cur)
    return (DistStart[v],Path)

def SetFullGraph(ListDeli:[int],nVille:int,WGraph : List[List[float]]): 
    """
    Create a complete Graph corresponding to the given incomplete graph 

    Parameters
    ----------
    ListDeli : [int]
        List of the city to delivers need to be made unique indexes to be able to do the inverse translation
    nVille : int
        DESCRIPTION.
    WGraph : List[List[float]]
        DESCRIPTION.

    Returns
    -------
    EquivArray : TYPE
        DESCRIPTION.
    WIntGraph : TYPE
        DESCRIPTION.

    """
    EquivArray = [[deque() for _ in range(nVille)] for _ in range(nVille)]
    WIntGraph =  [[0 for _ in range(nVille)] for _ in range(nVille)]
    
    for i in ListDeli:
        for j in ListDeli:
            if i != j:
                Size, Equiv= Djiska(WGraph, nVille, i, j)
                WIntGraph[i][j] = Size
                EquivArray[i][j] = Equiv
    for i in  range(nVille-1,-1,-1):
        if i not in ListDeli:
            WIntGraph.pop(i)
    for i in range(len(ListDeli)):
        for j in range(nVille-1,-1,-1):
            if j not in ListDeli:
                WIntGraph[i].pop(j)
    return  EquivArray , WIntGraph
     