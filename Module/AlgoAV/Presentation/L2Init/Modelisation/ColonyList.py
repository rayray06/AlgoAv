# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 1:41 2022

@author: ray-h
"""

from typing import List,Tuple,Deque,Union
from AlgoAV.Presentation.L2Init.Modelisation.FourmiList import CreateFourmi,UpdatePheromon,FourmiType,ChoosePath
import copy

ColonyType = List[Union[int,List[List[float]],List[FourmiType],int,int,int,float,Deque[int]]]
"""
List Representing the colony having for value :
0 : The size of the graph : Integer ;
1 : Array reprensenting the pheromonMap : List of List of float ;
2 : the list of ant : List of FourmiType ;
3 : The starting vertex of every ants : Integer ;
4 : The size of the colony : Integer ;
5 : The time to live of every ants : Integer
6 : Best Path Length
7 : Best Path
"""

def CreationColony(Mat: Tuple[Tuple[float]],CitySize:int,StartingVertice:int,ColonySize:int,StartValue:float) -> ColonyType:
    """
    Create a colny element represented as a ColonyType

    Parameters
    ----------
    Mat : Tuple[Tuple[float]]
        Array representing the travel time between two vertice.
    CitySize : int
        The number of vertice to visit.
    StartingVertice : int
        The vertice from which every ant start.
    ColonySize : int
        The number of ant in the colony.
    StartValue : float
        The starting pheromon value.

    Returns
    -------
    ColonyType
        The colony with the given parameters.

    """
    PheromonMap = [[StartValue if (Mat[i][j] > 0) else 0 for i in range(CitySize)] for j in range(CitySize)] # Creating the pheromon Map
    ListAnt = [CreateFourmi(StartingVertice) for _ in range(ColonySize)] # Generating every ant of the first iteration
    return [CitySize,PheromonMap,ListAnt,StartingVertice,ColonySize,CitySize-1,float('inf'),None]

def SetNextStep(Colony: ColonyType,Evap: float,Depo: float):
    """
    
    Prepare the colony to start the next iteration
    
    Parameters
    ----------
    Colony : ColonyType
        DESCRIPTION.
    Evap : float
        DESCRIPTION.
    Depo : float
        DESCRIPTION.

    Returns
    -------
    None.

    """
    for i in range(Colony[0]): #Evaporate the aleready existing pheromon
        for j in range(i):
            Colony[1][i][j] *= (1-Evap)
            Colony[1][j][i] *= (1-Evap)
    for ant in Colony[2]:# Update pheromon repartion following
            UpdatePheromon(ant,Colony[1],Depo)
    Colony[2] = [CreateFourmi(Colony[3]) for _ in range(Colony[4])] # Create the next iteration of ants

def MoveAnts(Colony: ColonyType,WMapRef:Tuple[Tuple[float]],Alpha:float,Beta:float):
    """
    

    Parameters
    ----------
    Colony : ColonyType
        DESCRIPTION.
    WMap : Tuple[Tuple[float]]
        DESCRIPTION.
    Alpha : float
        DESCRIPTION.
    Beta : float
        DESCRIPTION.

    Returns
    -------
    None.

    """

    for antIndex in range(Colony[4]-1,-1,-1):# We iterate through every ants
        ant: FourmiType = Colony[2][antIndex]
        WMapCopy = [[ WMapRef[i][j] if j != Colony[3] else 0 for j in range(Colony[0])] for i in range(Colony[0])]
        for i in range(Colony[5]): # We iterate until the arrive to their iteration limit (TTL)
            NewVertice = ChoosePath(tuple(Colony[1][ant[0]]),Colony[0],tuple(WMapCopy[ant[0]]),Alpha,Beta)

            ant[2] += WMapRef[ant[0]][NewVertice] # We add the path weigth to the total path length
            ant[1].append(NewVertice) # We add the Vertice to the path
            ant[0] = NewVertice

            for y in range(Colony[0]):
                WMapCopy[y][NewVertice] = 0
                
        ant[2] += WMapRef[ant[0]][Colony[3]] # We add the path weigth to the total path length
        ant[1].append(Colony[3]) # We add the Vertice to the path
        ant[0] = Colony[3]

        if(ant[2] < Colony[6]): #We check if we got a better path
            Colony[6] = ant[2]
            Colony[7] = copy.deepcopy(ant[1])
