from AlgoAV.Generation.GraphGen import GraphGen , WeigthSet
from AlgoAV.Modelisation.InitPheromon import Colony
from AlgoAV.Modelisation.Fourmi import Fourmi
from AlgoAV.Modelisation.FullGraph import SetFullGraph
from AlgoAV.Processing.ExperiencePlan import Borne
from ipywidgets import IntProgress
from IPython.display import display
import progressbar
import matplotlib as plt
import numpy as np
import random
import math

if __name__ == "__main__":
    

    widgets = [' [',
            progressbar.Timer(format= 'elapsed time: %(elapsed)s'),
            '] ',
            progressbar.Bar('*'),' (',
            progressbar.ETA(), ') ',
            ]
    Textbar = progressbar.ProgressBar(max_value=200, 
                              widgets=widgets).start()
    NbTest = 15

    seed = 20
    random.seed(a=seed)

    nb_steps_bar = 1
    SizeEnumerate = range(10,50,10)
    nb_steps_bar *= len(SizeEnumerate)

    IteRange = range(20,50,10)
    nb_steps_bar *= len(IteRange)
    
    AlphaRange = range(0,100,45)
    nb_steps_bar *= len(AlphaRange)
    
    BetaRange = range(0,100,45)
    nb_steps_bar *= len(BetaRange)
    
    EvapRange = range(10,25,5)
    nb_steps_bar *= len(EvapRange)
    
    DepRange = range(90,100,3)
    nb_steps_bar *= len(DepRange)

    StartRange = range(100,120,10)
    nb_steps_bar *= len(StartRange)

    ColonySIzeRange = range(100,150,20)
    nb_steps_bar *= len(ColonySIzeRange)
    

    print(nb_steps_bar)
    bar = IntProgress(min=0, max=nb_steps_bar, layout={"width" : "100%"})
    display(bar)

    #Nombre Ville
    CorrespondingSize = []
    BestCompositionsList = []
    BestMeanValuesList = []
    BestMeanDerivativeValuesList = []
    for SizeTest in SizeEnumerate:

        Compositions = []
        MeanValues = []
        DerivativeValues = []
        maxWeigth = 50
        
        startingVertice = random.choice(range(SizeTest))
        ListDeliveries = random.choices(range(SizeTest),k=(math.floor(SizeTest*0.6)+1))
        
        ListDeliveries.append(startingVertice)
        ListDeliverieTreated = tuple(np.unique(ListDeliveries).tolist())

        Graph = GraphGen(SizeTest)
        WGraph = WeigthSet(Graph,SizeTest,seed,maxWeigth)
        
        
        EquivArray, WFullGraph = SetFullGraph(ListDeliverieTreated,SizeTest,WGraph)
        
        borne = Borne(len(ListDeliverieTreated),WFullGraph)

         
        IteEnumerate = enumerate(IteRange)
        for ItIndex,ItterationUsed in IteEnumerate:
        #NIteration

            AlphaEnumerate = enumerate(AlphaRange)
            for AlphaIndex,Alpha in AlphaEnumerate:
            #Alpha
                Fourmi.Alpha = Alpha/10

                BetaEnumerate = enumerate(BetaRange)
                for BetaIndex,Beta in BetaEnumerate:
                #Beta
                    Fourmi.Beta: float = Beta/10

                    EvapEnumerate = enumerate(EvapRange)
                    for EvapIndex,Evap in EvapEnumerate:
                    #Evap
                        Colony.Evap = Evap/100

                        DepEnumerate = enumerate(DepRange)
                        for DepIndex,Deposit in DepEnumerate:    
                        #Deposit
                            Fourmi.Deposit = Deposit

                            StartValueEnumerate = enumerate(StartRange)
                            for StartValueIndex,StartValue in StartValueEnumerate:
                            #StartValue
                                Colony.StartValue = StartValue

                                ColonySIzeEnumerate = enumerate(ColonySIzeRange)
                                for ColonySIzeIndex,ColonySize in ColonySIzeEnumerate:
                                #ColonySize

                                    random.seed()
                                    CurValues = []
                                    Compo = (ItIndex,AlphaIndex,BetaIndex,EvapIndex,DepIndex,StartValueIndex,ColonySIzeIndex)
                                    print(str(SizeTest)+": "+str(Compo))
                                    for _ in range(NbTest):
                                        ColonyO = Colony(WFullGraph,len(ListDeliverieTreated),ListDeliverieTreated.index(startingVertice))
                                        MinWeigth = 0
                                        BestPath = None
                                        for i in range(ItterationUsed):
                                            ColonyO.MoveAnts()
                                            if(i < ItterationUsed-1):
                                                ColonyO.SetNextStep()
                                        MinWeigth, BestPath = ColonyO.BestAnts()
                                        if(BestPath is not None) :
                                            CurValues.append((MinWeigth/borne)*100)
                                        bar.value += 1
                                        Textbar.update(bar.value)
                                    if len(CurValues) > 0:
                                        Compositions.append(Compo)
                                        MeanValues.append(np.mean(CurValues))
                                        DerivativeValues.append(np.nanstd(CurValues))
        if len(MeanValues) > 0:
            indexBest = MeanValues.index(min(MeanValues))
            CorrespondingSize.append(SizeTest)
            BestCompositionsList.append(Compositions[indexBest])
            BestMeanValuesList.append(MeanValues[indexBest])
            BestMeanDerivativeValuesList.append(DerivativeValues[indexBest])
    # affichage de la courbe de moyenne
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


                                    
                                    
    
    