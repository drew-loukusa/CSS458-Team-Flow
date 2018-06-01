# -*- coding: utf-8 -*-
"""
Created on Wed May 30 18:52:20 2018

@author: DanWorks
"""

import Initial_Landings_Distribution as ILD
import numpy as np
import matplotlib.pyplot as plt
import warnings
import matplotlib.cbook
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)


NUMBER_OF_TESTS = 1000

def affectOfRushHour():
    runwayLandings = [0,0,0]
    landingsCount = []
    gapsCount  = []
    
    
    for i in range(NUMBER_OF_TESTS):        
        runwayDist, lCount, gCount, CM, landings = ILD.GeneratePlaneDistribution()
        landingsCount.append(lCount)
        gapsCount.append(gCount)
    
    np_lCount = np.asarray(landingsCount)        
    np_gCount = np.asarray(gapsCount)       
    
    plt.figure(1)
    plt.plot(range(np.size(np_lCount)), np_lCount) 
    plt.title('Plot of landings variation')
    plt.xlabel('Test Number')
    plt.ylabel('Landings')
    plt.show()
    
    plt.figure(2)
    plt.plot(range(np.size(np_gCount)), np_gCount) 
    plt.title('Plot of gaps variation')
    plt.xlabel('Test Number')
    plt.ylabel('Gaps')
    plt.show()
    
    
def affectOfProbabilities():
    plt.figure(1)
    plt.plot(range(np.size(np_regular)), np_regular) 
    plt.title('Plot of mean temperatures using regular diffusion')
    plt.xlabel('Test Index')
    plt.ylabel('Temperature')
    plt.show()
    
    plt.figure(2)
    plt.plot(range(np.size(np_regular)), np_stochastic) 
    plt.title('Plot of mean temperatures using stochastic diffusion')
    plt.xlabel('Test Index')
    plt.ylabel('Temperature')
    plt.show()
    
def affectOfGapTimeDeviation():
    plt.figure(1)
    plt.plot(range(np.size(np_regular)), np_regular) 
    plt.title('Plot of mean temperatures using regular diffusion')
    plt.xlabel('Test Index')
    plt.ylabel('Temperature')
    plt.show()
    
    plt.figure(2)
    plt.plot(range(np.size(np_regular)), np_stochastic) 
    plt.title('Plot of mean temperatures using stochastic diffusion')
    plt.xlabel('Test Index')
    plt.ylabel('Temperature')
    plt.show()
    
def affectOfLandingTimeDeviation():
    plt.figure(1)
    plt.plot(range(np.size(np_regular)), np_regular) 
    plt.title('Plot of mean temperatures using regular diffusion')
    plt.xlabel('Test Index')
    plt.ylabel('Temperature')
    plt.show()
    
    plt.figure(2)
    plt.plot(range(np.size(np_regular)), np_stochastic) 
    plt.title('Plot of mean temperatures using stochastic diffusion')
    plt.xlabel('Test Index')
    plt.ylabel('Temperature')
    plt.show()
    
#Choose the analysis to run...
affectOfRushHour() 