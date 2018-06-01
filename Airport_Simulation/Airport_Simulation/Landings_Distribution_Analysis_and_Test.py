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


#========================== ADJUSTABLES (begin) ==========================
NUMBER_OF_TESTS = 1   
N_STEPS = 1400           #in minutes
#=========================== ADJUSTABLES (end) ===========================


def effectOfShiftingRushHour():
    avg_runwayLandings = []
    avg_landingsCount = []
    avg_gapsCount  = []
    #avg_operations = []
    
    shiftingInMin = 100
    
    for i in range(shiftingInMin): 
        landingsCount = []
        gapsCount = []
        #operationsCount = []
                                             #hour_start=0, hour_end=24, landing_limit=1139, regular_plane_prob=0.45, high_plane_prob=0.7
        for j in range(NUMBER_OF_TESTS):          
            runwayDist, lCount, gCount, CM, landings = ILD.GeneratePlaneDistribution(0, 24, 1139, 0.45, 0.6)
            landingsCount.append(lCount)
            gapsCount.append(gCount)
            
        np_lCount = np.asarray(landingsCount)        
        np_gCount = np.asarray(gapsCount) 
        #np_totalOps = np_lCount + np_gCount
        
        avg_landingsCount.append(np.average(np_lCount))
        avg_gapsCount.append(np.average(np_gCount))
        #avg_operations.append(np.average(np_totalOps))
    
    
    np_avg_lCount = np.asarray(avg_landingsCount)        
    np_avg_gCount = np.asarray(avg_gapsCount) 
    #np_avg_totalOps = np.asarray(avg_operations)
    
    fig, ax = plt.subplots()
    plt.ylim(400, 700)
    ax.plot(range(np.size(np_avg_lCount)), np_avg_lCount, 'g', label='Landings') 
    ax.plot(range(np.size(np_avg_gCount)), np_avg_gCount, 'b', label='Gaps')
    
    legend = ax.legend(loc='upper left', shadow=False, fontsize='medium')
    legend.get_frame().set_facecolor('#FFFFFF')
    
    plt.title('Plot of landings vs gaps over rush hour shift')
    plt.xlabel('Shift Amount (in minutes)')
    plt.ylabel('Landings and Gaps')
    plt.show()
    
    
def effectOfExpanding_ShrinkingRushHour():
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
    plt.title('Plot of total operations')
    plt.xlabel('Test Number')
    plt.ylabel('Gaps')
    plt.show()
    
def effectOfProbabilities():
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
    
def effectOfGapTimeDeviation():
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
    
def effectOfLandingTimeDeviation():
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
effectOfShiftingRushHour() 
#effectOfExpanding_ShrinkingRushHour() 
#effectOfProbabilities()
#effectOfGapTimeDeviation()
#effectOfLandingTimeDeviation()