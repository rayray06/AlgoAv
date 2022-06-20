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
    NbTest = 5
    seed = 20
    if seed is not None:
        random.seed(seed)
    else:
        random.seed()

    nb_steps_bar = NbTest
    SizeEnumerate = [10]
    nb_steps_bar *= len(SizeEnumerate)
    
    IterationRange = range((2*SizeEnumerate[0]),(SizeEnumerate[0]**2),SizeEnumerate[0]*2)
    nb_steps_bar *= len(IterationRange)


    ProportionRange = range(10,150,50)
    nb_steps_bar *= len(ProportionRange)
    # AlphaRange = range(30,40,5)
    # nb_steps_bar *= len(AlphaRange)
    
    # BetaRange = range(30,40,5)
    # nb_steps_bar *= len(BetaRange)
    
    EvapRange = range(40,60,5)
    nb_steps_bar *= len(EvapRange)
    
    DepRange = range(100,110,10)
    nb_steps_bar *= len(DepRange)

    StartRange = range(100,110,10)
    nb_steps_bar *= len(StartRange)

    ColonySIzeRange = range(2*SizeEnumerate[0],SizeEnumerate[0]**2,math.floor(SizeEnumerate[0]/5))
    nb_steps_bar *= len(ColonySIzeRange)

    print(nb_steps_bar)
    
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
        
        ListTest = []
        ListBorne = []
        for _ in range(NbTest):

            startingVertice = random.choice(range(SizeTest))
            ListDeliveries = random.choices(range(SizeTest),k=(5))
            
            ListDeliveries.append(startingVertice)
            ListDeliverieTreated = tuple(np.unique(ListDeliveries).tolist())

            Graph = GraphGen(SizeTest)
            WGraph = WeigthSet(Graph,SizeTest,seed,maxWeigth)
            
            
            EquivArray, WFullGraph = SetFullGraph(ListDeliverieTreated,SizeTest,WGraph)

            ListTest.append((WFullGraph,ListDeliverieTreated,startingVertice))
            borne = Borne(len(ListDeliverieTreated),WFullGraph)
            ListBorne.append(borne)
        ListTest = tuple(ListTest)
        ListBorne = tuple(ListBorne)
        Sufficient = False

        for ItterationUsed in IterationRange:
        #NIteration

            for Prop in ProportionRange:
            #Alpha
                Fourmi.Alpha = 5

                Fourmi.Beta: float = Fourmi.Alpha*(Prop/100)

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
                                Compo = (ItterationUsed,Fourmi.Alpha,Fourmi.Beta,Evap,Deposit,StartValue,ColonySize)
                                Textbar.update(value)
                                print(str(SizeTest)+": "+str(Compo))
                                for test in range(NbTest):
                                        ColonyO = Colony(ListTest[test][0],len(ListTest[test][1]),(ListTest[test][1]).index(ListTest[test][2]))
                                        MinWeigth = 0
                                        BestPath = None
                                        value += 1
                                        for i in range(ItterationUsed):
                                            ColonyO.MoveAnts()
                                            if(i < ItterationUsed-1):
                                                ColonyO.SetNextStep()
                                        MinWeigth, BestPath = ColonyO.BestAnts()
                                        if(BestPath is not None) :
                                            CurValues.append((MinWeigth/ListBorne[test])*100)
                                if len(CurValues) > 0:
                                    meanValue = np.mean(CurValues)
                                    print(meanValue)
                                    Compositions.append(Compo)
                                    MeanValues.append(np.mean(CurValues))
                                    DerivativeValues.append(np.nanstd(CurValues))
        if len(MeanValues) > 0:
            indexBest = MeanValues.index(min(MeanValues))
            CorrespondingSize.append(SizeTest)
            BestCompositionsList.append(Compositions[indexBest])
            BestMeanValuesList.append(MeanValues[indexBest])
            BestMeanDerivativeValuesList.append(DerivativeValues[indexBest])
    Textbar.finish()
    # affichage de la courbe de moyenne
    print("Beginning Display")
    print(str(CorrespondingSize[0])+" "+str(BestCompositionsList[0]))
    print("Borne Sup = " +str(BestMeanValuesList[0]+BestMeanDerivativeValuesList[0]))
    print("Moyenne = " +str(BestMeanValuesList[0]))
    print("Borne Inf = " +str(BestMeanValuesList[0]-BestMeanDerivativeValuesList[0]))
    
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
    


                                
                                    
    
    