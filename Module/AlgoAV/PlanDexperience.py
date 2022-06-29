from AlgoAV.Generation.GraphGen import GraphGen , WeigthSetFixed
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
    NbTest = 5
    PourcentageCible = 111.59236667394259
    seed = None
    minSize = 5
    maxSize = 16
    stepSize = 1
    if seed is not None:
        random.seed(seed)
    else:
        random.seed()

    nb_steps_bar = NbTest
    SizeEnumerate = range(minSize,maxSize,stepSize)
    nb_steps_bar *= len(SizeEnumerate)

    IteRange = range(2,30**2,10)
    nb_steps_bar *= len(IteRange)


    ColonySIzeRange = range(2,30**2,10)
    nb_steps_bar *= len(ColonySIzeRange)
    
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
    maxWeigth = 1000
    
    for SizeTest in SizeEnumerate:
        
        
        Compositions = []
        MeanValues = []
        DerivativeValues = []

        MaxTime = 10

        IteRange = range(math.ceil(SizeTest/4),2*SizeTest,math.ceil(SizeTest/10))
        ColonySIzeRange = range(math.ceil(SizeTest/4),2*SizeTest,math.ceil(SizeTest/10))
        
        ListTest = []
        print("Generating graph of size : " + str(SizeTest))
        for _ in range(NbTest):
            borne = None
            while borne is None:
                print("New Generation test")
                startingVertice = random.choice(range(SizeTest))

                ListDeliverieTreated = tuple(range(SizeTest))

                CityTotreat = len(ListDeliverieTreated)
                Graph = GraphGen(SizeTest)

                WGraph = WeigthSetFixed(Graph,SizeTest,seed,maxWeigth,MaxTime)
                
                
                EquivArray, WFullGraph = SetFullGraph(ListDeliverieTreated,SizeTest,WGraph,MaxTime)

                borne = Borne(len(ListDeliverieTreated),WFullGraph,MaxTime,startingVertice)
            
            ListTest.append((WFullGraph,startingVertice,CityTotreat,borne))


        print("Starting Calculation for size of : "+str(SizeTest))
        Sufficient = False

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
                        for ItterationUsed in IteRange:
                        #NIteration
                        
                            for ColonySize in ColonySIzeRange :
                            #ColonySize

                                random.seed()
                                CurValues = []
                                Textbar.update(value)
                                if not(Sufficient):
                                    Compo = (ItterationUsed,Alpha,Beta,Evap,Deposit,StartValue,ColonySize)
                                    print(str(SizeTest)+": "+str(Compo))
                                for test in range(NbTest):
                                    if not(Sufficient):
                                        MinWeigth, BestPath, StepList = \
                                        FourmiOpti(ListTest[test][0],
                                                ListTest[test][2],
                                                Evap,
                                                Alpha,
                                                Beta,
                                                ItterationUsed,
                                                Deposit,
                                                ListTest[test][1],
                                                ColonySize,
                                                StartValue,
                                                MaxTime
                                                )
                                        if(BestPath is not None) :
                                            CurValues.append((MinWeigth/ListTest[test][3])*100)
                                    value += 1
                                if len(CurValues) > 0:
                                    meanValue = np.mean(CurValues)
                                    print(meanValue)
                                    Compositions.append(Compo)
                                    MeanValues.append(np.mean(CurValues))
                                    DerivativeValues.append(1.96 * (np.nanstd(CurValues)/math.sqrt(NbTest)))
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
       c.execute("REPLACE INTO Param_2_1 VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",i)
    connection.commit()
    c.close()
    connection.close()
    plt.show()
    


                                
                                    
    
    