# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 14:55:00 2022

@author: ray-h
"""
from AlgoAV.Modelisation.ColonyList import CreationColony,ColonyType,MoveAnts,SetNextStep
from typing import Tuple,Deque,List
import random



def FourmiOpti(WMap:Tuple[Tuple[Tuple[float]]],CitySize:int,Evap:float,Alpha:float,Beta:float,IterationCount:int,Deposit:float,StartingVertice:int,ColonySize:int,StartValue:float,MaxTime:int,ObjectDeliveryList :List[int]) -> Tuple[float,Deque[int],Deque[int]] :
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
    MaxTime : int
        The maximum number of steps
    ObjectDeliveryList : List[int]
        The position of the object to retrieve

    Returns
    -------
    Tuple[float,Deque[int],Deque[int]] 
        The best path found, its length and the step time coreesponding

    """
    random.seed()
    ColonyO: ColonyType = CreationColony(WMap, CitySize, StartingVertice, ColonySize, StartValue,ObjectDeliveryList)
    for i in range(IterationCount):
        MoveAnts(ColonyO,WMap,Alpha,Beta,MaxTime,ObjectDeliveryList)
        if(i < IterationCount-1):
            SetNextStep(ColonyO,Evap,Deposit,ObjectDeliveryList)
    return ColonyO[6],ColonyO[7],ColonyO[8]
