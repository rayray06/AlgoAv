# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 12:20:50 2022

@author: ray-h
"""
import numpy as np

class Fourmi: 
    def __init__(self,PheromonMap):
        self.PheromonMap = PheromonMap
        self.CurrentPosition = 0