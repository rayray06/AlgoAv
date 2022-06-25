import pandas as pd
import os
import math

df = pd.read_csv ((os.getcwd()+'\\TestDataSet\\TestFourmi.csv'),delimiter=';',header=None)
print(df[0][0])
newarray = [[ math.sqrt((df[0][i]-df[0][j])**2 + (df[1][i]-df[1][j])**2) for j in range(len(df))] for i in range(len(df))]

sourceFile = open('testToPython.txt', 'w')
print(newarray, file = sourceFile)
sourceFile.close()