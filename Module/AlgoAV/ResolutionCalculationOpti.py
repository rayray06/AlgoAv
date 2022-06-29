from AlgoAV.Generation.GraphGen import GraphGen , WeigthSetFixed
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
from time import process_time
if __name__ == "__main__":
    
    Nb_Test = 5
    MinSize = 5
    MaxSize = 260
    StepSize = 20
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
        maxWeigth = 5
        Evap = 0.25
        Alpha = 5
        Beta = 0.5
        Deposit = 90
        StartValueDeposit = 90
        IterationUsed = 2
        ColonySize = math.ceil(nb_Cities)

        seed = None
        if seed is not None:
            random.seed(seed)
        else:
            random.seed()

        for test in range(Nb_Test):
            print("=================================\nGeneration Full Graph ("+str(test)+","+str(nb_Cities)+")")
            startingVertice = random.choice(range(nb_Cities))
            ListDeliveries = list(range(nb_Cities))

            ListDeliverieTreated = tuple(np.unique(ListDeliveries).tolist())
            CityTotreat = len(ListDeliverieTreated)
            Graph = GraphGen(nb_Cities)
            MaxTime = 10

            WGraph = WeigthSetFixed(Graph,nb_Cities,seed,maxWeigth,MaxTime)
            
            
            start = process_time()
            EquivArray, WFullGraph = SetFullGraph(ListDeliverieTreated,nb_Cities,WGraph,MaxTime)

            IterationUsed = math.ceil(CityTotreat/4)
            ColonySize = math.ceil(CityTotreat/2)

            print("\Generation time : "+str(process_time()-start)+" s")
            random.seed()
            


            print("Starting Calculation")
            MinWeigth, BestPath, BestPathTimeStep = \
            FourmiOpti(WFullGraph,
                        nb_Cities,
                        Evap,
                        Alpha,
                        Beta,
                        IterationUsed,
                        Deposit,
                        startingVertice,
                        ColonySize,
                        StartValueDeposit,
                        MaxTime
                        )
            print("The next to optimal path length is : ", MinWeigth)
            print("The optimal path is : ")

            OptimalPath = deque()
            StartValue = BestPath.popleft()
            EndValue = BestPath.popleft()
            stepIndex = BestPathTimeStep.popleft()
            while(len(BestPath)>0):
                Equiv = copy.deepcopy(EquivArray[stepIndex][ListDeliverieTreated[StartValue]][ListDeliverieTreated[EndValue]])
                while(len(Equiv)>1):
                    OptimalPath.append(Equiv.popleft())
                StartValue = EndValue
                EndValue = BestPath.popleft()
                stepIndex = BestPathTimeStep.popleft()
            Equiv = copy.deepcopy(EquivArray[stepIndex][ListDeliverieTreated[StartValue]][ListDeliverieTreated[EndValue]])
            while(len(Equiv)>0):
                OptimalPath.append(Equiv.popleft())
            while(len(OptimalPath)>0):
                print(OptimalPath.popleft(),end="->")

            print("\nExecution time : "+str(process_time()-start)+" s")
            List_CurResult.append(process_time()-start)
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
    plt.title("Temps d'execution par taille d'instance")
    plt.show()
                                
                                    
    
    