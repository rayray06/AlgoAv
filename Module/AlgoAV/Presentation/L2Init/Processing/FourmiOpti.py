# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 14:55:00 2022

@author: ray-h
"""
from AlgoAV.Presentation.L2Init.Modelisation.ColonyList import CreationColony,ColonyType,MoveAnts,SetNextStep
from typing import Tuple,Deque
import random



def FourmiOpti(WMap:Tuple[Tuple[float]],CitySize:int,Evap:float,Alpha:float,Beta:float,IterationCount:int,Deposit:float,StartingVertice:int,ColonySize:int,StartValue:float) -> Tuple[float,Deque[int]] :
    """
    

    Parameters
    ----------
    WMap : Tuple[Tuple[float]]
        The weigth array of to process.
    CitySize : int
        The number of vertice to process
    Evap : float
        The pheromone evaporation
    Alpha : float
        Alpha parameter for the process 
    Beta : float
        Beta parameter for the the process
    IterationCount : int
        Iteration Number for the process
    Deposit : float
        The quantity of pheromone spread 
    StartingVertice : int
        The starting Vertice to solve our problem
    ColonySize : int
        The Number of ant to process
    StartValue : float
        The starting value for the pheromone quantity

    Returns
    -------
    Tuple[float,Deque[int]] 
        The best path found and its length

    """
    random.seed()
    ColonyO: ColonyType = CreationColony(WMap, CitySize, StartingVertice, ColonySize, StartValue)
    for i in range(IterationCount):
        MoveAnts(ColonyO,WMap,Alpha,Beta)
        if(i < IterationCount-1):
            SetNextStep(ColonyO,Evap,Deposit)
    return  ColonyO[6],ColonyO[7]
