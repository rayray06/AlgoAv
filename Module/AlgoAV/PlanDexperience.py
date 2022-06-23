from AlgoAV.Generation.GraphGen import GraphGen , WeigthSet
from AlgoAV.Processing.FourmiOpti import FourmiOpti
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
    

    widgets = ['\n['
               , progressbar.Timer(),
            '] ',
            progressbar.Bar('*'),' ',
            progressbar.Percentage(),' | (',
            progressbar.ETA(), ')\n',
            ]
    NbTest = 30
    PourcentageCible = 210
    seed = 20
    minSize = 10
    maxSize = 110
    stepSize = 10
    if seed is not None:
        random.seed(seed)
    else:
        random.seed()

    nb_steps_bar = NbTest
    SizeEnumerate = range(minSize,maxSize,stepSize)
    nb_steps_bar *= len(SizeEnumerate)

    # Iteration range(Ceil(Size/2),Size*3,Ceil(Size/10))
    MaxCeiled = maxSize - ((maxSize-minSize)%stepSize)
    nb_steps_bar *= (10/2)*(MaxCeiled-minSize)/stepSize

    # ColonySize range(Ceil(Size/2),Size*3,Ceil(Size/10))
    nb_steps_bar *= (10/2)*(MaxCeiled-minSize)/stepSize

    
    ProportionRange = range(10,170,50)
    nb_steps_bar *= len(ProportionRange)
    
    EvapRange = range(25,55,5)
    nb_steps_bar *= len(EvapRange)
    
    DepRange = range(90,106,3)
    nb_steps_bar *= len(DepRange)

    StartRange = range(90,120,10)
    nb_steps_bar *= len(StartRange)
    
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
        IteRange = range(math.ceil(SizeTest/2),3*SizeTest,math.ceil(SizeTest/10))
        ColonySIzeRange = range(math.ceil(SizeTest/2),3*SizeTest,math.ceil(SizeTest/10))
        
        
        Compositions = []
        MeanValues = []
        DerivativeValues = []
        maxWeigth = 1000
        
        ListTest = []
        for _ in range(NbTest):

            startingVertice = random.choice(range(SizeTest))

            ListDeliverieTreated = tuple(range(SizeTest))

            CityTotreat = len(ListDeliverieTreated)
            Graph = GraphGen(SizeTest)
            WGraph = WeigthSet(Graph,SizeTest,seed,maxWeigth)
            
            
            EquivArray, WFullGraph = SetFullGraph(ListDeliverieTreated,SizeTest,WGraph)

            borne = Borne(len(ListDeliverieTreated),WFullGraph)

            ListTest.append((WFullGraph,startingVertice,CityTotreat,borne))


        
        Sufficient = False
        for ItterationUsed in IteRange:
        #NIteration
        
            for ColonySize in ColonySIzeRange :
            #ColonySize

                for Prop in ProportionRange :
                    Alpha = 5
                    Beta = Alpha*(Prop/100)

                    for Evap in EvapRange:
                    #Evap
                        Evap /= 100

                        for Deposit in DepRange:    
                        #Deposit

                            for StartValue in StartRange:
                            #StartValue

                                random.seed()
                                CurValues = []
                                if not(Sufficient):
                                    Compo = (ItterationUsed,Alpha,Beta,Evap,Deposit,StartValue,ColonySize)
                                    Textbar.update(value)
                                    print(str(SizeTest)+": "+str(Compo))
                                for test in range(NbTest):
                                    if not(Sufficient):
                                        MinWeigth, BestPath = \
                                        FourmiOpti(ListTest[test][0],
                                                ListTest[test][2],
                                                Evap,
                                                Alpha,
                                                Beta,
                                                ItterationUsed,
                                                Deposit,
                                                ListTest[test][1],
                                                ColonySize,
                                                StartValue
                                                )
                                        value += 1
                                        if(BestPath is not None) :
                                            CurValues.append((MinWeigth/ListTest[test][3])*100)
                                    else:
                                        value += 1
                                if len(CurValues) > 0:
                                    meanValue = np.mean(CurValues)
                                    print(meanValue)
                                    Compositions.append(Compo)
                                    MeanValues.append(np.mean(CurValues))
                                    DerivativeValues.append(np.nanstd(CurValues))
                                    if meanValue < PourcentageCible:
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
    plt.show()
    


                                
                                    
    
    