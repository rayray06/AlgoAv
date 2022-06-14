# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 15:11:35 2022

@author: ray-h
"""

def InitPheromon(Mat):
    PheromonMap = np.zeros(Mat.shape)
    for i in range(len(PheromonMap)):
        order = sum(Mat[i])
        value = 1/order
        for j in range(len(PheromonMap[i])):
            PheromonMap[i,j] = value * Mat[i,j]