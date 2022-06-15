# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 12:20:54 2022

@author: ray-h
"""
import numpy as np
import copy
import random
from typing import List
from collections import deque


def ExistChemin(matriceAdj: List[List[bool]], u: int, v: int) -> bool :
    """
    

    Parameters
    ----------
    matriceAdj : List[List[int]]
        DESCRIPTION.
    u : int
        DESCRIPTION.
    v : int
        DESCRIPTION.

    Returns
    -------
    bool 
        DESCRIPTION.
    
    @authors : Charlie, Valentin, Dylan
    """
    n = len(matriceAdj)  # nombre de sommets dans le graphe
    file = deque()
    visites = [False] * n
    # ajouter le premier sommet à la file d'attente
    file.append(u)
    while file:
        # supprimer le sommet supérieur de la pile et marqué comme visité
        courant = file.pop()
        visites[courant] = True
 
        # visiter les sommets adjacents
        for i in range(n):
            # Il existe un chemin de u à i(v)
            if matriceAdj[courant,i] > 0:
            # Si le sommet i est le sommet voulu (i = v)
                if i == v:
                    return True
                # le sommet i n'est pas encore visité
                elif not(visites[i]):
                    file.append(i)
                    # ajouter i à la file marqué comme visité
                    visites[i] = True
    return False
 
    
def connecte(matriceAdj: List[List[bool]]) -> bool:
    """
    

    Parameters
    ----------
    matriceAdj : List[List[bool]]
        DESCRIPTION.

    Returns
    -------
    bool
        DESCRIPTION.
    @authors : Charlie, Valentin, Dylan
    """
    n = len(matriceAdj)  # nombre de sommets
    for i in range(1,n):
        if not(ExistChemin(matriceAdj, 0, i)):
                return False    
    return True

def GraphGen(nVille: int) -> List[List[int]]:
    """
    Function used to generate the adjacence array from a connected non oriented graph of nVille cities

    Parameters
    ----------
    nVille : int
        Number of cities wanted for our graph.

    Returns
    -------
    List[List[int]]
        Adjacence array of said graph.

    """
    MatriceValid = False # Initialised the fact that the Array is yet to generate
    b_symm = [[False]*nVille for _ in range(nVille)] #Initialised sure to be invalid array
    while(not(MatriceValid)):
        Mat = np.random.choice((True, False), size=(nVille,nVille), p=[0.3, 0.7]) #Creation of a random array
        
        # we do the or operation with the trasposition to create symmetry
        b_symm = np.logical_or(Mat, Mat.T)
        
        for i in range(nVille):#We set the diagnonal to false to prohib loop back to itself
            b_symm[i,i] = False
        
        MatriceValid = connecte(b_symm) #We check if the graph is connected
    # We return the array in array of integers
    return b_symm.astype(int)

def WeigthSet(MatAdj:List[List[int]],nVille:int,seed:int,maxWeigth:float) -> List[List[float]]:
    """
    
    Set a given adjacence array as Weigthed
    Parameters
    ----------
    MatAdj : List[List[int]]
        Corresponding adjacence array
    nVille : int
        Number of cities of the array
    seed : int
        Seed use to generate array
    maxWeigth : float
        MaxWeigth for graph

    Returns
    -------
    List[List[float]]
        Weigth Array.
    @ray-h
    """
    Matrice_Final = MatAdj.astype(float)
    
    random.seed(a=seed)
    for i in range(nVille):
        for j in range(i):
            print(random.random())
            Matrice_Final[j,i] *= 1 + (random.random() * maxWeigth)
            Matrice_Final[i,j] = Matrice_Final[j,i]
    return Matrice_Final
    
print(WeigthSet(GraphGen(10),10,5,50))