from AlgoAV.Generation.GraphGen import GraphGen , WeigthSet
from AlgoAV.Modelisation.InitPheromon import Colony
from AlgoAV.Modelisation.Fourmi import Fourmi
from AlgoAV.Modelisation.FullGraph import SetFullGraph
from AlgoAV.Processing.ExperiencePlan import Borne
from ipywidgets import IntProgress
from IPython.display import display
import mysql.connector
import progressbar
import matplotlib.pyplot as plt
import numpy as np
import random
import math

if __name__ == "__main__":
    

    widgets = [' ['
               , progressbar.Timer(),
            '] ',
            progressbar.Bar('*'),' (',
            progressbar.ETA(), ') ',
            ]
    NbTest = 30

    seed = 20
    random.seed(a=seed)

    nb_steps_bar = NbTest
    SizeEnumerate = range(10,30,10)
    nb_steps_bar *= len(SizeEnumerate)

    IteRange = range(30,39,10)
    nb_steps_bar *= len(IteRange)
    
    AlphaRange = range(0,40,45)
    nb_steps_bar *= len(AlphaRange)
    
    BetaRange = range(0,40,45)
    nb_steps_bar *= len(BetaRange)
    
    EvapRange = range(10,14,5)
    nb_steps_bar *= len(EvapRange)
    
    DepRange = range(90,92,3)
    nb_steps_bar *= len(DepRange)

    StartRange = range(100,109,10)
    nb_steps_bar *= len(StartRange)

    ColonySIzeRange = range(30,90,20)
    nb_steps_bar *= len(ColonySIzeRange)
    
    Textbar = progressbar.ProgressBar(maxval=nb_steps_bar, 
                              widgets=widgets)
    Textbar.start()
    value = 0

    #Nombre Ville
    CorrespondingSize = []
    BestCompositionsList = []
    BestMeanValuesList = []
    BestMeanDerivativeValuesList = []
    for SizeTest in SizeEnumerate:

        Compositions = []
        MeanValues = []
        DerivativeValues = []
        maxWeigth = 1000
        
        startingVertice = random.choice(range(SizeTest))
        ListDeliveries = random.choices(range(SizeTest),k=(math.floor(SizeTest*0.6)+1))
        
        ListDeliveries.append(startingVertice)
        ListDeliverieTreated = tuple(np.unique(ListDeliveries).tolist())

        Graph = GraphGen(SizeTest)
        WGraph = WeigthSet(Graph,SizeTest,seed,maxWeigth)
        
        
        EquivArray, WFullGraph = SetFullGraph(ListDeliverieTreated,SizeTest,WGraph)
        
        borne = Borne(len(ListDeliverieTreated),WFullGraph)
        Sufficient = False
         
        for ItterationUsed in IteRange:
        #NIteration

            for Alpha in AlphaRange:
            #Alpha
                Fourmi.Alpha = Alpha/10

                for Beta in BetaRange:
                #Beta
                    Fourmi.Beta: float = Beta/10

                    for Evap in EvapRange:
                    #Evap
                        Colony.Evap = Evap/100

                        for Deposit in DepRange:    
                        #Deposit
                            Fourmi.Deposit = Deposit


                            for StartValue in StartRange:
                            #StartValue
                                Colony.StartValue = StartValue


                                for ColonySize in ColonySIzeRange :
                                #ColonySize

                                    random.seed()
                                    CurValues = []
                                    if not(Sufficient):
                                        Compo = (ItterationUsed,Alpha,Beta,Evap,Deposit,StartValue,ColonySize)
                                        Textbar.update(value)
                                        print(str(SizeTest)+": "+str(Compo))
                                    for _ in range(NbTest):
                                        if not(Sufficient):
                                            ColonyO = Colony(WFullGraph,len(ListDeliverieTreated),ListDeliverieTreated.index(startingVertice))
                                            MinWeigth = 0
                                            BestPath = None
                                            value += 1
                                            for i in range(ItterationUsed):
                                                ColonyO.MoveAnts()
                                                if(i < ItterationUsed-1):
                                                    ColonyO.SetNextStep()
                                            MinWeigth, BestPath = ColonyO.BestAnts()
                                            if(BestPath is not None) :
                                                CurValues.append((MinWeigth/borne)*100)
                                        else:
                                            value += 1
                                    if len(CurValues) > 0:
                                        meanValue = np.mean(CurValues)
                                        print(meanValue)
                                        Compositions.append(Compo)
                                        MeanValues.append(np.mean(CurValues))
                                        DerivativeValues.append(np.nanstd(CurValues))
                                        if meanValue < 230:
                                            Sufficient = True
        if len(MeanValues) > 0:
            indexBest = MeanValues.index(min(MeanValues))
            CorrespondingSize.append(SizeTest)
            BestCompositionsList.append(Compositions[indexBest])
            BestMeanValuesList.append(MeanValues[indexBest])
            BestMeanDerivativeValuesList.append(DerivativeValues[indexBest])
    Textbar.finish()
    # affichage de la courbe de moyenne
    print("Beginning Display")
    plt.plot(CorrespondingSize, BestMeanValuesList)
    
    
    # affichage de la bande d'écart-type
    plt.fill_between(CorrespondingSize,
                    np.subtract(BestMeanValuesList, BestMeanDerivativeValuesList), # borne haute
                    np.add(BestMeanValuesList, BestMeanDerivativeValuesList),      # borne basse
                    alpha=.5)                          # transparence
    plt.xlabel("Taille test")
    plt.ylabel("Distance de la borne en %")
    plt.title("Meilleurs qualité de solutions trouvé par taille de liste")
    plt.show()
    
    print("Beginning to send to DB")
    RowList = []
    for i in range(len(CorrespondingSize)):
        RowList.append((CorrespondingSize[i],BestCompositionsList[i][0],BestCompositionsList[i][1],BestCompositionsList[i][2],BestCompositionsList[i][3],BestCompositionsList[i][4],BestCompositionsList[i][5],BestCompositionsList[i][6]))
    connection = mysql.connector.connect(host='testrialpayapi.cokj0wfmdhfw.eu-west-3.rds.amazonaws.com',
                                         port=3315,
                                         database='AlgoAV',
                                         user='PortfolioUser')
    connection.start_transaction()
    c = connection.cursor()
    for i in RowList:
       c.execute("REPLACE INTO Param VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",i)
    connection.commit()
    c.close()
    connection.close()
    


                                
                                    
    
    