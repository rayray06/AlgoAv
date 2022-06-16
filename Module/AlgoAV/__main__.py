from AlgoAV.Generation.GraphGen import GraphGen , WeigthSet
from AlgoAV.Modelisation.InitPheromon import Colony
from AlgoAV.Modelisation.FullGraph import SetFullGraph
import numpy as np
import random
import math

if __name__ == "__main__":
    
    ItterationUsed = 500
    
    seed = 20
    random.seed(a=seed)
    SizeTest = 100
    maxWeigth = 50
    
    startingVertice = random.choice(range(SizeTest))
    ListDeliveries = random.choices(range(SizeTest),k=math.floor(SizeTest*0.6))
    
    ListDeliveries.append(startingVertice)
    ListDeliverieTreated = np.unique(ListDeliveries).tolist()
    
    Graph = GraphGen(SizeTest)
    WGraph = WeigthSet(Graph,SizeTest,seed,maxWeigth)
    EquivArray, WFullGraph = SetFullGraph(ListDeliverieTreated,SizeTest,WGraph)
    
    random.seed()
    Colony = Colony(WFullGraph,len(ListDeliverieTreated),ListDeliverieTreated.index(startingVertice))
    MinWeigth = 0
    BestPath = None
    print(WFullGraph)
    for i in range(ItterationUsed):
        Colony.MoveAnts()
        MinWeigth, BestPath = Colony.BestAnts()
        print("====================Iteration N°"+str(i)+"====================")
        print(BestPath)
        print(MinWeigth)
        Colony.SetNextStep()
    
    