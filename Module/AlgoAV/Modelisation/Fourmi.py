# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 12:20:50 2022

@author: ray-h
"""
import numpy as np
from typing import List,Tuple,Deque
from collections import deque
import random
import copy
from functools import lru_cache

class Fourmi:
    
    Alpha:float = 1
    Beta: float = 2
    Deposit: float = 10
    
    def __init__(self,WMap,MapSize,PheromonMap,StartVertice):
        self.WMap = copy.deepcopy(WMap)
        self.MapSize = MapSize
        self.PheromonMap = PheromonMap
        self.CurrentPosition = StartVertice
        self.PathTaken = deque((StartVertice,))
        self.LengthPath = 0
        self.Alive = True
            
    def Eliminate(self):
        self.Alive = False
        
    def ChoosePath(self):


        WMapedTuple = copy.deepcopy(self.WMap)
        PheromonTuple = copy.deepcopy(self.PheromonMap)

        for i in range(self.MapSize):
            WMapedTuple[i] = tuple(WMapedTuple[i])
            PheromonTuple[i] = tuple(PheromonTuple[i])
        WMapedTuple = tuple(WMapedTuple)
        PheromonTuple = tuple(PheromonTuple)

        Choices = Fourmi.PathChoiceCached(WMapedTuple,self.CurrentPosition,self.MapSize,PheromonTuple)
        
        Choice = random.choices(range(self.MapSize),weights=Choices,k=1)[0]
        
        self.LengthPath += self.WMap[self.CurrentPosition][Choice]
        self.CurrentPosition = Choice
        self.PathTaken.append(Choice)
        
        for i in range(self.MapSize):
            self.WMap[i][Choice] = 0
        return Choice
 
    def UpdatePheromon(self):
        Start = self.PathTaken.popleft()
        Next = self.PathTaken.popleft()
        while(len(self.PathTaken)>0):
            self.PheromonMap[Start][Next] += Fourmi.Deposit/self.LengthPath 
            Start = Next
            Next = self.PathTaken.popleft()

    @lru_cache(maxsize=256)
    def PathChoiceCached(WMap:Tuple[Tuple[float]],CurrentPosition: int,MapSize: int,PheromonMap: Tuple[Tuple[float]]):

        Choices = Fourmi.PercentageCalculationCached(MapSize,WMap[CurrentPosition],PheromonMap[CurrentPosition])     
        
        SumChoices = sum(Choices)
        for i in range(MapSize):
            Choices[i] /= SumChoices
        return Choices

    @lru_cache(maxsize=256)
    def PercentageCalculationCached(MapSize:int,WMapRow:Tuple[float],PheromonMapRow:Tuple[float]):
        Choices = [0]*MapSize
        MaxWeigth = (max(WMapRow)+1)*1.1
        for i in range(MapSize):
            if WMapRow[i] > 0:
                Choices[i] = ((MaxWeigth-WMapRow[i])**Fourmi.Alpha)*(PheromonMapRow[i]**Fourmi.Beta)
            else:
                Choices[i] = 0
        return Choices
