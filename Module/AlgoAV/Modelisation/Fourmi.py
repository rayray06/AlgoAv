# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 12:20:50 2022

@author: ray-h
"""
import numpy as np
from collections import deque
import random
import copy


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
    
    def SetParameters(alpha:float,beta:float,Deposit:float):
        if alpha < 0:
            raise ValueError("alpha must be greater or equal to 0")
        elif beta < 1:
            raise ValueError("beta must be greater or equal to 1")
        else:
            Fourmi.Alpha=alpha
            Fourmi.Beta=beta
            
    def Eliminate(self):
        self.Alive = False
        
    def ChoosePath(self):
        Choices = [0]*self.MapSize
        MaxWeigth = (max(self.WMap[self.CurrentPosition])+1)*1.1
        for i in range(self.MapSize):
            if self.WMap[self.CurrentPosition][i] > 0:
                Choices[i] = (((MaxWeigth)-self.WMap[self.CurrentPosition][i])**Fourmi.Alpha)*(self.PheromonMap[self.CurrentPosition][i]**Fourmi.Beta)
            else:
                Choices[i] = 0
        SumChoices = sum(Choices)
        Choices[i] /= SumChoices
        
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
            
        
        