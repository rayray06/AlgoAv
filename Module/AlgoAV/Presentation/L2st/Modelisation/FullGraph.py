# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 11:58:48 2022

@author: ray-h
"""

from typing import List,Tuple,Deque
from collections import deque
import random
import copy
from functools import lru_cache
import numpy as np
from AlgoAV.Generation.GraphGen import WeigthSetFixed, GraphGen

def DjiskaSSSP(WGraph:Tuple[Tuple[float]],nVille:int, u:int,ListDeli:List[int]) -> Tuple[float,List[Deque[int]]]:
    """
    Do the Dijkstra's algorithm to find the shortest route between from the vertice u to all other vertices  

    Parameters
    ----------
    WGraph : List[List[float]]
        The weigth array use to determine the best path
    nVille : int
        The number of cities for our graph
    u : int
        The start vertice for the path

    Returns
    -------
    Tuple[float,Deque[int]]
        A tuple containing the total size of the shortest path at index 0 and A queu representing the corresponding path (including the start and end vertice)

    """
    Visited = deque() #Priority queu of the already visited vertice
    DistStart = [float('inf')]*(u) + [0.0] + [float('inf')]*(nVille-(u+1))#Array representing each vertice distance with the vertice u
    copyWGraph = list(copy.deepcopy(WGraph)) #A copy of the weigthed array to process the algoritm

    for i in range(nVille):
        copyWGraph[i] = list(copyWGraph[i])


    for i in range(len(copyWGraph)):#initialise every non-existing edge has infinite 
        for j in range(i+1):
            if(copyWGraph[i][j] == 0):
                copyWGraph[i][j] = float('inf')
                copyWGraph[j][i] = float('inf')
    
    while(any([ (i not in Visited) for i in ListDeli]) ):#Cycle through the shortest path from u and the already visited vertice until we visit the vertice v
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

    AllPath = []
    for i in ListDeli:
        Path = deque((i,))
        cur = i
        if(i == u):
            Path.append(i)
        while(u not in Path):# We cycle through the shortest edge from ou vertice v to backtrack to our vertice u
            MinWeigth = float('inf')
            CurVertice = 0
            for i,value in enumerate(copyWGraph[cur]):
                if(value < MinWeigth) and (i not in Path):
                    MinWeigth = value
                    CurVertice = i
            cur = CurVertice
            Path.appendleft(cur)
        AllPath.append(Path)
    return (DistStart,AllPath)

def SetFullGraph(ListDeli:Tuple[int],nVille:int,WGraph:Tuple[Tuple[Tuple[float]]] , MaxTime : int) -> Tuple[List[List[Deque[int]]],Tuple[Tuple[float]]] : 
    """
    Create a complete Graph corresponding to the given incomplete graph 

    Parameters
    ----------
    ListDeli : [int]
        List of the city to delivers need to be made unique indexes to be able to do the inverse translation
    nVille : int
        Number of cities to process.
    WGraph : List[List[float]]
        Weigthed array of the situation.

    Returns
    -------
    EquivArray : List[List[Deque[int]]]
        The transformation array from the direct path from the full graph to the true path for the ADEME probleme.
    WIntGraph : List[List[float]]
        Weigthed graph of the full graph.

    """
    EquivArray = [[[deque() for _ in range(nVille)] for _ in range(nVille)]for _ in range(MaxTime)]
    WIntGraph =  [[[0 for _ in range(nVille)] for _ in range(nVille)]for _ in range(MaxTime)]
    NewCityLength = len(ListDeli)

    for y in range(MaxTime):
        for i in ListDeli:
            Size, Equiv= DjiskaSSSP(WGraph[y], nVille, i,ListDeli)
            WIntGraph[y][i] = Size
            EquivArray[y][i] = Equiv
        for i in  range(nVille-1,-1,-1):
            if i not in ListDeli:
                WIntGraph[y].pop(i)
                
        for i in range(NewCityLength):
            for j in range(nVille-1,-1,-1):
                if j not in ListDeli:
                    WIntGraph[y][i].pop(j)
            WIntGraph[y][i] = tuple(WIntGraph[y][i])

    return  EquivArray , WIntGraph
     