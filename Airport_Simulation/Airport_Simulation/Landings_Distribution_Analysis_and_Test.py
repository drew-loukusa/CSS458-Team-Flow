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
NUMBER_OF_TESTS = 10   
N_STEPS = 1400           #in minutes
#=========================== ADJUSTABLES (end) ===========================


def effectOfShiftingRushHour():
    avg_runwayLandings = []
    avg_landingsCount = []
    avg_gapsCount  = []
    avg_operations = []
    
    shiftingInMin = 120
    
    for i in range(shiftingInMin): 
        landingsCount = []
        gapsCount = []
        #operationsCount = []   
                                             #hour_start=0, hour_end=24, landing_limit=1139, regular_plane_prob=0.45, high_plane_prob=0.6, ...
                                             #...landingTime=1.4, landingSigma=0.1, morning_R_S=360, morning_R_E=600, evening_R_S=840, evening_R_E=1200
        for j in range(NUMBER_OF_TESTS):          
            runwayDist, lCount, gCount, CM, landings = ILD.GeneratePlaneDistribution(0, 24, 1139, 0.45, 0.6, 1.4, 0.1, 360+i, 600+i, 840+i, 1200+i)
            landingsCount.append(lCount)
            gapsCount.append(gCount)
            
        np_lCount = np.asarray(landingsCount)        
        np_gCount = np.asarray(gapsCount) 
        np_totalOps = np_lCount + np_gCount
        
        avg_landingsCount.append(np.average(np_lCount))
        avg_gapsCount.append(np.average(np_gCount))
        avg_operations.append(np.average(np_totalOps))
    
    
    np_avg_lCount = np.asarray(avg_landingsCount)        
    np_avg_gCount = np.asarray(avg_gapsCount) 
    np_avg_totalOps = np.asarray(avg_operations)
    
    fig, ax = plt.subplots()
    #plt.ylim(540, 620)
    ax.plot(range(np.size(np_avg_lCount)), np_avg_lCount, 'g', label='Landings') 
    ax.plot(range(np.size(np_avg_gCount)), np_avg_gCount, 'b', label='Gaps')
    
    legend = ax.legend(loc='upper left', shadow=False, fontsize='medium')
    legend.get_frame().set_facecolor('#FFFFFF')
    
    plt.title('Plot of landings over rush hour shift')
    plt.xlabel('Shift Amount (in minutes)')
    plt.ylabel('Operations')
    plt.show()
    
    
def effectOfExpanding_RushHour():
    avg_runwayLandings = []
    avg_landingsCount = []
    avg_gapsCount  = []
    avg_operations = []
    
    shiftingInMin = [20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300]
    
    for i in range(len(shiftingInMin)): 
        landingsCount = []
        gapsCount = []
        operationsCount = []   
                                             #hour_start=0, hour_end=24, landing_limit=1139, regular_plane_prob=0.45, high_plane_prob=0.6, ...
                                             #...landingTime=1.4, landingSigma=0.1, morning_R_S=360, morning_R_E=600, evening_R_S=840, evening_R_E=1200
        for j in range(NUMBER_OF_TESTS):          
            runwayDist, lCount, gCount, CM, landings = ILD.GeneratePlaneDistribution(0, 24, 1139, 0.45, 0.6, 1.4, 0.1, 360, (600+shiftingInMin[i]), 840, (1200+shiftingInMin[i]))
            landingsCount.append(lCount)
            gapsCount.append(gCount)
            
        np_lCount = np.asarray(landingsCount)        
        np_gCount = np.asarray(gapsCount) 
        np_totalOps = np_lCount + np_gCount
        
        avg_landingsCount.append(np.average(np_lCount))
        avg_gapsCount.append(np.average(np_gCount))
        avg_operations.append(np.average(np_totalOps))
    
    
    np_avg_lCount = np.asarray(avg_landingsCount)        
    np_avg_gCount = np.asarray(avg_gapsCount) 
    np_avg_totalOps = np.asarray(avg_operations)
    
    fig, ax = plt.subplots()
    #plt.ylim(540, 620)
    ax.plot(shiftingInMin, np_avg_lCount, 'g', label='Landings') 
    ax.plot(shiftingInMin, np_avg_gCount, 'b', label='Gaps')
    #ax.plot(shiftingInMin, np_avg_totalOps, 'g', label='Landings+Gaps') 
    
    legend = ax.legend(loc='upper left', shadow=False, fontsize='medium')
    legend.get_frame().set_facecolor('#FFFFFF')
    
    plt.title('Plot of landings vs gaps over rush hour expansion')
    plt.xlabel('Expansion Amount (in minutes) to end time of rush hour')
    plt.ylabel('Operations')
    plt.show()
    
    
def effectOfProbabilities():
    avg_runwayLandings = []
    avg_landingsCount = []
    avg_gapsCount  = []
    #avg_operations = []
    
    increaseProb = [0.1, 0.125, 0.15, 0.175, 0.2, 0.225, 0.25, 0.275, 0.3, 0.325, 0.35, 0.375, 0.4, 0.425, 0.45, 0.475, 0.5]
    
    for i in range(len(increaseProb)): 
        landingsCount = []
        gapsCount = []
        #operationsCount = []   
                                             #hour_start=0, hour_end=24, landing_limit=1139, regular_plane_prob=0.45, high_plane_prob=0.6, ...
                                             #...landingTime=1.4, landingSigma=0.1, morning_R_S=360, morning_R_E=600, evening_R_S=840, evening_R_E=1200
        for j in range(NUMBER_OF_TESTS):          
            runwayDist, lCount, gCount, CM, landings = ILD.GeneratePlaneDistribution(0, 24, 1139, 0.45, 0.45+increaseProb[i], 1.4, 0.1, 360, 600, 840, 1200)
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
    #plt.ylim(540, 620)
    ax.plot(increaseProb, np_avg_lCount, 'g', label='Landings') 
    ax.plot(increaseProb, np_avg_gCount, 'b', label='Gaps')
    
    legend = ax.legend(loc='upper left', shadow=False, fontsize='medium')
    legend.get_frame().set_facecolor('#FFFFFF')
    
    plt.title('Plot of landings vs gaps as a result in increased landing probability')
    plt.xlabel('Probability increase of a landing during rush hour')
    plt.ylabel('Operations')
    plt.show()
    

def effectOfLandingTimeDeviation():
    avg_runwayLandings = []
    avg_landingsCount = []
    avg_gapsCount  = []
    #avg_operations = []
    
    increaseSigma = [0.1, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
    
    for i in range(len(increaseSigma)): 
        landingsCount = []
        gapsCount = []
        #operationsCount = []   
                                             #hour_start=0, hour_end=24, landing_limit=1139, regular_plane_prob=0.45, high_plane_prob=0.6, ...
                                             #...landingTime=1.4, landingSigma=0.1, morning_R_S=360, morning_R_E=600, evening_R_S=840, evening_R_E=1200
        for j in range(NUMBER_OF_TESTS):          
            runwayDist, lCount, gCount, CM, landings = ILD.GeneratePlaneDistribution(0, 24, 1139, 0.45, 0.6, 1, 1+increaseSigma[i], 360, 600, 840, 1200)
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
    #plt.ylim(540, 620)
    ax.plot(increaseSigma, np_avg_lCount, 'g', label='Landings') 
    ax.plot(increaseSigma, np_avg_gCount, 'b', label='Gaps')
    
    legend = ax.legend(loc='upper left', shadow=False, fontsize='medium')
    legend.get_frame().set_facecolor('#FFFFFF')
    
    plt.title('Plot of landings vs gaps as a result of landing time deviation')
    plt.xlabel('Deviation (in minutes) from average landing time of 1.4')
    plt.ylabel('Operations')
    plt.show()
    
    
#Choose the analysis to run...
#effectOfShiftingRushHour() 
#effectOfExpanding_RushHour() 
effectOfProbabilities()
#effectOfLandingTimeDeviation()