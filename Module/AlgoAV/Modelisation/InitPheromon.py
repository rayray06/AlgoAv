# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 15:11:35 2022

@author: ray-h
"""
import numpy as np
import copy
from AlgoAV.Modelisation.Fourmi import Fourmi

class Colony:
    StartValue = 100
    ColonySize = 200
    Evap : float = 0.4
    
    def __init__(self,Mat,CitySize,StartingVertice):
        self.StartingVertice = StartingVertice
        self.CitySize = CitySize
        self.PheromonMap = [[Colony.StartValue if (Mat[i][j] > 0) else 0 for i in range(CitySize)] for j in range(CitySize)]

        newMat = list(copy.deepcopy(Mat))
        for i in range(CitySize):
            newMat[i] = list(newMat[i])

        self.Territory = newMat
        self.ListAnt = [Fourmi(newMat,CitySize,self.PheromonMap,StartingVertice) for _ in range(Colony.ColonySize)]
    
    def SetNextStep(self):
        for i in range(self.CitySize):
            for j in range(i):
                self.PheromonMap[i][j] *= (1-Colony.Evap)
                self.PheromonMap[j][i] *= (1-Colony.Evap)
        for i in self.ListAnt:
            if i.Alive:
                i.UpdatePheromon()
        self.ListAnt = [Fourmi(self.Territory,self.CitySize,self.PheromonMap,self.StartingVertice) for _ in range(Colony.ColonySize)]
    
    def BestAnts(self):
        BestPath = None
        MinWeigth = float('inf')
        for ant in self.ListAnt:
            if ant.Alive and ant.LengthPath < MinWeigth:
                BestPath = ant.PathTaken
                MinWeigth = ant.LengthPath
        return MinWeigth,BestPath
        
                
    
    def MoveAnts(self):
        for ant in self.ListAnt:
            for i in range(self.CitySize):
                NewVertice = ant.ChoosePath()
                if NewVertice != self.StartingVertice :
                    if ant.PathTaken.count(NewVertice) != 1:
                        ant.Eliminate()
                        break
                else :
                    if (len(ant.PathTaken) != self.CitySize+1) or (ant.PathTaken.count(NewVertice) != 2):
                        ant.Eliminate()
                        break