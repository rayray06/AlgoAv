# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 1:41 2022

@author: ray-h
"""
from typing import List,Tuple,Deque,Union
from collections import deque
import random
from functools import lru_cache

FourmiType = List[Union[int,Deque[int],float,Deque[int],int]]
"""
List representing an ant made of the following values:
0 : CurrentPosition of the ant in the graph : integer,
1 : PathTaken By the ant : FILO of integer,
2 : TotalLength of the chosen path
3 : Each Time Step Followed 
4 : Curent Time Step
"""

def CreateFourmi(StartVertice:int) -> FourmiType:
    """
    
    Create a ant object with the given parameter 
    Parameters
    ----------
    StartVertice : int
        The vertice from which the ant must start.

    Returns
    -------
    FourmiType
        The ant with the given parameters.

    """
    return [StartVertice,deque((StartVertice,)),0,deque((0,)),0]
    


def ChoosePath(PheromonMapRow:Tuple[float],CitySize:int,WMapRow:Tuple[float],Alpha:float,Beta:float) -> int:
    """
    
    Choose the next vertice to go folling the given context parameters
    Parameters
    ----------
    PheromonMapRow : Tuple[float]
        The row of the current position in the pheromonMap array.
    CitySize : int
        Number of city involved.
    WMapRow : Tuple[float]
        The row of the current position in the Weigthed array.
    Alpha : float
        The paramater alpha used by the ants.
    Beta : float
        The parameter beta used by the ants.

    Returns
    -------
    int
        The chosen next vertice.

    """

    Choices = PathChoiceCached(WMapRow,CitySize,PheromonMapRow,Alpha,Beta)
    
    Choice = random.choices(range(CitySize),weights=Choices,k=1)[0]

    return Choice

def UpdatePheromon(Fourmi: FourmiType,PheromonMap: List[List[float]],Depo: float):
    """

    Update the pheromon map depending of the given ant    

    Parameters
    ----------
    Fourmi : FourmiType
        Ant that update the map.
    PheromonMap : List[List[float]]
        The pheromon map.
    Depo : float
        The number of pheromon deposit by the ant.

    Returns
    -------
    None.

    """
    Start = Fourmi[1].popleft()
    Next = Fourmi[1].popleft()
    while(len(Fourmi[1])>0):
        PheromonMap[Start][Next] += Depo/Fourmi[2]
        Start = Next
        Next = Fourmi[1].popleft()
    PheromonMap[Start][Next] += Depo/Fourmi[2]
    
@lru_cache(maxsize=256)
def PathChoiceCached(WMapRow: Tuple[float],MapSize: int,PheromonMapRow: Tuple[float],Alpha: float,Beta: float) -> List[float]:
    """
    
    Give the probability to choose a Vertice over another

    Parameters
    ----------
    WMapRow : Tuple[float]
        The Weigth List of the graph starting from the current position.
    MapSize : int
        The number of concerned vertice.
    PheromonMapRow : Tuple[float]
        The Pheromon List of the graph starting from the current position.
    Alpha : float
        The paramater alpha used by the ants.
    Beta : float
        The parameter beta used by the ants.

    Returns
    -------
    List[float]
        The probability for to choose next vertice.

    """
    Choices = [0]*MapSize
    for i in range(MapSize):
        if WMapRow[i] > 0:
            Choices[i] = ((1/WMapRow[i])**Alpha)*(PheromonMapRow[i]**Beta)
        else:
            Choices[i] = 0 
    
    SumChoices = sum(Choices)
    for i in range(MapSize):
        Choices[i] /= SumChoices
    return Choices

