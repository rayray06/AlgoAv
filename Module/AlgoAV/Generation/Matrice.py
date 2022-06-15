# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 14:23 2022

@author: Charlie
"""
import numpy as np
import numpy.linalg as alg


def creationMatrice(SommetMin: int , SommetMax: int):
    """
    Create a random and symmetrical matrice where vertex can't connect to itself

    Parameters
    ----------
    SommetMin : int
        Minimum vertex numbers
    SommetMax : int
        Maximum vertex numbers

    Returns
    -------
    Matrix : matrix 
        Return the generated matrix

    """
  
    Sommet = np.random.randint(SommetMin,SommetMax)
    
    Matrix = np.random.randint(2, size=(Sommet,Sommet))
    
    for i in range(Sommet):
            Matrix[i,i] = 0
            y=0
            while y < i :
                Matrix[i,y]=Matrix[y,i]
                y+=1
    return Matrix

   

# Cette fonction utilise un algorithme de parcours en largeur
# pour savoir s'il existe un chemin entre deux sommets
# le graphe est représenté par la matrice d'adjacence
 
 
def ExistChemin(matriceAdj, u, v):
    """
    Check if a way exist between two vertex

    Parameters
    ----------
    matriceAdj : matrix
        The matrix generated
    u : int
        the vertex on the x-axis
    v : int
        the vertex on the y-axis

    Returns
    -------
    Bool 
        Return if a way exist or not between two vertex

    """
    n = len(matriceAdj)  # nombre de sommets dans le graphe
    file = []
    visites = [False] * n
    # ajouter le premier sommet à la file d'attente
    file.append(u)
    while file:
        # supprimer le sommet supérieur de la pile et marqué comme visité
        courant = file.pop(0)
        visites[courant] = True
 
        # visiter les sommets adjacents
        for i in range(n):
            # s'il existe et qu'un bord entre u et i et
            # le sommet i n'est pas encore visité
            if matriceAdj[courant][i] > 0 and visites[i] == False:
                # ajouter i à la file marqué comme visité
                file.append(i)
                visites[i] = True
 
            # Si le sommet i est le sommet voulu (i = v)
            # donc il existe un chemin de u à i(v)
            elif matriceAdj[courant][i] > 0 and i == v:
                return True
              
 
    return False
 
    
def connecte(matriceAdj):
    """
    Check if the graph is connected

    Parameters
    ----------
    matriceAdj : matrix
        The matrix generated

    Returns
    -------
    Bool 
        Return if the generated matrix is connected or not

    """
    n = len(matriceAdj)  # nombre de sommets
    for i in range(n):
        for j in range(n):
            if (i != j) and ExistChemin(matriceAdj, i, j) == False:
                return False
              
    return True
    
#creationMatrice()
#print(Matrix)
#print(connecte(Matrix)) 
def verifMatrice():
    """
    Call functions until the matrix is generated and connected

    Parameters
    ----------

    Returns
    -------
    matrice : matrix 
        Return a randomly generated matrix which is symetrical , 
        connected and where vertex isn't connected to itself

    """

    matrice = creationMatrice(10,50) #generation de la matrice (MinSommet,MaxSommet)

    while connecte(matrice)==False: #Tant que la matrice n'est pas un graphe connecté , recréer la matrice
        matrice=creationMatrice(10,50)
    return matrice
  
matrice_global=verifMatrice()
print(matrice_global)
print('Matrice connecte :' ,connecte(matrice_global))

