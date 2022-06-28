from AlgoAV.Generation.GraphGen import GraphGen , WeigthSet, ObjectAttribution
from AlgoAV.Modelisation.FullGraph import SetFullGraph
from AlgoAV.Processing.ExperiencePlan import Borne
from AlgoAV.Processing.FourmiOpti import FourmiOpti
import mysql.connector
import progressbar
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
    seed = None
    if seed is not None:
        random.seed(seed)
    else:
        random.seed()

    nb_steps_bar = NbTest
    SizeEnumerate = [10]
    nb_steps_bar *= len(SizeEnumerate)
    
    IterationRange = range(math.floor(SizeEnumerate[0]/4),(SizeEnumerate[0]*2),math.floor(SizeEnumerate[0]/4))
    nb_steps_bar *= len(IterationRange)


    ProportionRange = range(10,100,50)
    nb_steps_bar *= len(ProportionRange)
    # AlphaRange = range(30,40,5)
    # nb_steps_bar *= len(AlphaRange)
    
    # BetaRange = range(30,40,5)
    # nb_steps_bar *= len(BetaRange)
    
    EvapRange = range(40,65,5)
    nb_steps_bar *= len(EvapRange)
    
    DepRange = range(100,110,10)
    nb_steps_bar *= len(DepRange)

    StartRange = range(100,110,10)
    nb_steps_bar *= len(StartRange)

    ColonySIzeRange = range(math.floor(SizeEnumerate[0]/4),(SizeEnumerate[0]*2),math.floor(SizeEnumerate[0]/4))
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
            ListDeliveries = list(range(SizeTest))

            ListDeliverieInt = tuple(np.unique(ListDeliveries).tolist())
            ListDeliverieTreated, ObjectGetPoint = ObjectAttribution(startingVertice,ListDeliverieInt,SizeTest)

            CityTotreat = len(ListDeliverieTreated)
            Graph = GraphGen(SizeTest)
            WGraph = WeigthSet(Graph,SizeTest,seed,maxWeigth)
            
            
            EquivArray, WFullGraph = SetFullGraph(ListDeliverieTreated,SizeTest,WGraph)
            
            ListTest.append((WFullGraph,startingVertice,CityTotreat))
            borne = Borne(CityTotreat,WFullGraph)
            ListBorne.append(borne)
        ListTest = tuple(ListTest)
        ListBorne = tuple(ListBorne)
        Sufficient = False

        for ItterationUsed in IterationRange:
        #NIteration

            for Prop in ProportionRange:
            #Alpha
                Beta = 5

                Alpha: float = Beta*(Prop/100)

                for Evap in EvapRange:
                #Evap
                    Evap /= 100

                    for Deposit in DepRange:    
                    #Deposit


                        for StartValue in StartRange:


                            for ColonySize in ColonySIzeRange :
                            #ColonySize

                                random.seed()
                                CurValues = []
                                Compo = (ItterationUsed,Alpha,Beta,Evap,Deposit,StartValue,ColonySize)
                                Textbar.update(value)
                                print(str(SizeTest)+" : "+str(Compo))
                                for test in range(NbTest):
                                        value += 1
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
            # BestCompositionsList.append(Compositions[indexBest])
            BestMeanValuesList.append(np.mean(MeanValues))
            BestMeanDerivativeValuesList.append(np.nanstd(MeanValues))
    Textbar.finish()
    # affichage de la courbe de moyenne
    print("Beginning Display")
    print(str(CorrespondingSize[0]))
    print("Borne Sup = " +str(BestMeanValuesList[0] + 1.96 * (BestMeanDerivativeValuesList[0]/math.sqrt(nb_steps_bar/NbTest))))
    print("Moyenne = " +str(BestMeanValuesList[0]))
    print("Borne Inf = " +str(BestMeanValuesList[0] - 1.96 * (BestMeanDerivativeValuesList[0]/math.sqrt(nb_steps_bar/NbTest))))
    


                                
                                    
    
    