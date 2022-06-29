from AlgoAV.Generation.GraphGen import GraphGen , WeigthSet
from AlgoAV.Modelisation.FullGraph import SetFullGraph
from AlgoAV.Processing.ExperiencePlan import Borne
from AlgoAV.Processing.FourmiOpti import FourmiOpti
import matplotlib.pyplot as plt
from collections import deque
import mysql.connector
import progressbar
import numpy as np
import random
import math
import copy
from time import process_time,perf_counter
if __name__ == "__main__":
    
    Nb_Test = 5
    MinSize = 5
    MaxSize = 25
    StepSize = 2
    SizeRange = range(MinSize,MaxSize,StepSize)

    List_MeanResult = []
    List_DerivationResult = []

    widgets = ['\n['
            , progressbar.Timer(),
        '] ',
        progressbar.Bar('*'),' ',
        progressbar.Percentage(),' | (',
        progressbar.ETA(), ')\n',
        ]

    nb_steps_bar = len(SizeRange)*Nb_Test
    value = 0

    Textbar = progressbar.ProgressBar(maxval=nb_steps_bar, 
                    widgets=widgets)
    Textbar.start()
    for nb_Cities in SizeRange:
        List_CurResult = []
        maxWeigth = 1000

        seed = None
        if seed is not None:
            random.seed(seed)
        else:
            random.seed()

        for test in range(Nb_Test):
            print("=================================\nGeneration Full Graph ("+str(test)+","+str(nb_Cities)+")")
            MinWeigth = None
            while MinWeigth is None :
                start = perf_counter()

                startingVertice = random.choice(range(nb_Cities))
                ListDeliveries = list(range(nb_Cities))

                ListDeliverieTreated = tuple(np.unique(ListDeliveries).tolist())
                CityTotreat = len(ListDeliverieTreated)
                Graph = GraphGen(nb_Cities)
                WGraph = WeigthSet(Graph,nb_Cities,seed,maxWeigth)
                
                
                _, WFullGraph = SetFullGraph(ListDeliverieTreated,nb_Cities,WGraph)

                random.seed()
                
                MinWeigth = Borne(CityTotreat,WFullGraph)
            print("The next to optimal path length is : ", MinWeigth)
            stop = perf_counter()
            print("\nExecution time : "+str(stop-start)+" s")
            List_CurResult.append(stop-start)
            value += 1
            Textbar.update(value)
        List_MeanResult.append(np.mean(List_CurResult))
        List_DerivationResult.append(1.96 * (np.nanstd(List_CurResult)/math.sqrt(Nb_Test)))
    Textbar.finish()
    print("Beginning Display")
    plt.plot(SizeRange, List_MeanResult)
    
    
    # affichage de la bande d'écart-type
    plt.fill_between(SizeRange,
                    np.subtract(List_MeanResult, List_DerivationResult), # borne haute
                    np.add(List_MeanResult, List_DerivationResult),      # borne basse
                    alpha=.5)                          # transparence
    plt.xlabel("Taille Instance")
    plt.ylabel("Temps d'execution")
    plt.title("Temps d'execution par taille d'instance Simplexe")
    plt.show()
                                
                                    
    
    