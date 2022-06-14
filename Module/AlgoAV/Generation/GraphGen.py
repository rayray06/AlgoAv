# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 12:20:54 2022

@author: ray-h
"""
import numpy as np
import copy
from typing import List


def ConexionCheck(Mat: List[List[int]],Curindex: int,nVille: int,Visited: List[int]) -> bool :
    """
    Check if a given graph is connected or not using recursion

    Parameters
    ----------
    Mat : List[List[int]]
        Adjacense array to check.
    Curindex : int
        The current node visited.
    nVille : int
        the number of city in the graph.
    Visited : List[int]
        the list of already visited cities.

    Returns
    -------
    bool 
        Return if the graph is connected or not.

    """
    Visited[Curindex] = 1
    for i in range(nVille):
        Mat[i,Curindex] = 0
    for i in range(nVille):
        if Mat[Curindex,i] == 1:
            ConexionCheck(Mat,i,nVille,Visited)
    return sum(Visited) == nVille

def GraphGen(nVille: int) -> List[List[int]]:
    MatriceValid = False
    while(not(MatriceValid)):
        Mat = np.random.choice((True, False), size=(nVille,nVille), p=[0.3, 0.7])
        
        # on fait le `ou` logique de la matrice et de sa transposée
        b_symm = np.logical_or(Mat, Mat.T)
        
        for i in range(nVille):
            b_symm[i,i] = False
        MatriceValid = ConexionCheck(copy.deepcopy(b_symm),0,nVille,np.zeros(nVille , dtype=np.int64))
    # on renvoie la matrice de booléens convertie en matrice d'entiers
    return b_symm.astype(int)

