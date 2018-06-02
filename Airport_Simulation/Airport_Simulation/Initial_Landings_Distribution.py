#This is the Landings Distribution Method

#It uses a uniform random generator to come up with the distribution of thelandings
#There are different probabilities used at different points in times
#The time is counted at each minute
#There is a rush time probability, and a regular probability

#Average takeoff takes 30-35 seconds, without taking alignment with the runway time
#Average landing time at SEA-TAC = 1.2 minutes or 72 seconds

import random

TYPE_P = "PASSANGER"
TYPE_C = "CARGO"         

#FROM LEFT to RIGHT these are the runway numbers, no matter the direction from which a plane is landing
RUNWAYS = (0,1,2)   #Runway 2 is not in use

class Landing:	#Will be appended to the distribution list
    def __init__(self, timeIn, runwayIn, planeTypeIn):	
        self.time	= timeIn			# minutes the landing will take
        self.runway = runwayIn			# runway on which the plane will be landing
        self.planeType = planeTypeIn	# the type of plane can be "PASSENGER" or "CARGO"
		
class Gap: 		#Will be appended to the distribution list
    def __init__(self, timeIn, runwayIn):
        self.time = timeIn				#minutes the gap will take
        self.runway = runwayIn			#the runway on which this gap is available


def GeneratePlaneDistribution(hour_start=0, hour_end=24, landing_limit=1139, regular_plane_prob=0.45, high_plane_prob=0.7, landingTime=1.4, landingSigma=0.1, morning_R_S=360, morning_R_E=600, evening_R_S=840, evening_R_E=1200):
    """ - The hours parameters has to be given in Military Time:"
    		   MIN: 0
		      MAX: 24
		
		  - The probability should be given in decimal:
			   MIN: 0
			   MAX: 1
    """
    TIME_LANDING = landingTime             
    TIME_LANDING_DEVIATION = landingSigma 
    	
    MORNING_RUSH_RANGE = (morning_R_S, morning_R_E)    #these are the start and end in minutes of morning rush hour. 06:00 - 10:00 Military
    EVENING_RUSH_RANGE = (evening_R_S, evening_R_E)    #these are the start and end in minutes of evening rush hour. 14:00 - 20:00
    
    HS = hour_start
    HE = hour_end
    LL = landing_limit
    RPP = 1.0-regular_plane_prob
    HPP = 1.0-high_plane_prob
	
    total_hours	= HE - HS
    total_minutes = total_hours * 60
	
    landingCount = 0
    gapCount = 0
    totalOperations = landingCount + gapCount
    
    runwayLandings = [0,0,0]
	
    currentMinutes = 0.0
    distribution = []		#will keep track of Landings and Gaps
	
    while (currentMinutes < total_minutes):

        if (landingCount < LL):
            
            if ((currentMinutes >= MORNING_RUSH_RANGE[0]) and (currentMinutes <= MORNING_RUSH_RANGE[1])):
                
                LandingChance = RandP()
                if(LandingChance > HPP):                                       
                    rIndex, dT, tempLanding = generateLanding(TIME_LANDING, TIME_LANDING_DEVIATION) 
                    distribution.append(tempLanding)
                    landingCount += 1
                    currentMinutes += dT
                    runwayLandings[rIndex] += 1
                    
                else:  
                    dT, tempGap = generateGap()
                    distribution.append(tempGap)
                    gapCount += 1
                    currentMinutes += dT
                    
            if ((currentMinutes >= EVENING_RUSH_RANGE[0]) and (currentMinutes <= EVENING_RUSH_RANGE[1])):
                
                LandingChance = RandP()
                if(LandingChance > HPP):                                       
                    rIndex, dT, tempLanding = generateLanding(TIME_LANDING, TIME_LANDING_DEVIATION)  
                    distribution.append(tempLanding)
                    landingCount += 1
                    currentMinutes += dT
                    runwayLandings[rIndex] += 1
                    
                else:  
                    dT, tempGap = generateGap()
                    distribution.append(tempGap)
                    gapCount += 1
                    currentMinutes += dT
            
            else:
                LandingChance = RandP()
                if(LandingChance > RPP):                         #this is where the change is. RPP instead of HPP                     
                    rIndex, dT, tempLanding = generateLanding(TIME_LANDING, TIME_LANDING_DEVIATION)  
                    distribution.append(tempLanding)
                    
                    landingCount += 1
                    currentMinutes += dT                   
                    runwayLandings[rIndex] += 1
                    
                else:  
                    dT, tempGap = generateGap()
                    distribution.append(tempGap)
                    gapCount += 1
                    currentMinutes += dT
        else:
            tempRunway = random.randint(1,3)
            tempGapTime = total_minutes - currentMinutes
    
            currentMinutes += tempGapTime
            gapCount += 1
    
            tempGap = Gap(tempGapTime, tempRunway)
            distribution.append(tempGap)
    
    return (runwayLandings, landingCount, gapCount, currentMinutes, distribution)
		
		
	

def RandP():	
	return random.random()

def generateLanding(landingTime, landingDeviation):
    tempRunway = random.randint(0,1)
    if (tempRunway == 1):
        tempRunway = 2
                    
    tempTypeProb = RandP()
    #print(tempTypeProb)
    tempPlaneType = None
    if (tempTypeProb > 0.2):
        tempPlaneType = TYPE_P
    else:
        tempPlaneType = TYPE_C
                        
    qR = random.randint(1,2)
    tempTime = landingTime - landingDeviation 
    if (qR == 2):    
        tempTime = landingDeviation + landingTime  
        
    #print(tempTime)
                        
    retLanding = Landing(tempTime,tempRunway,tempPlaneType)
    return (tempRunway, tempTime, retLanding)


def generateGap():
    tempRunway = random.randint(1,3)
    tempGapTime = 1.112
          
    retGap = Gap(tempGapTime, tempRunway)
    return (tempGapTime, retGap)
    
#Test
def mainTest():
    runwayDist, lCount, gCount, CM, landings = GeneratePlaneDistribution(0, 24, 1139, 0.3, 0.7, 1.4, 0.1, 360, (600+300), 840, (1200+300))
    possibleAircraftOperations = gCount + lCount
    print("Runway 1 landings: " + str(runwayDist[0]))
    print("Runway 2 landings: " + str(runwayDist[1]))
    print("Runway 3 landings: " + str(runwayDist[2]))
    print("Landings: " + str(lCount))
    print("Gaps: " + str(gCount))
    print("Total (Landings + Potential Takeoffs): " + str(possibleAircraftOperations))
    print("Goal for total AircraftOperations: 1139 +- 20")
    print("TotalMinutes: " + str(CM))
    print()
    #print(landings)
    
    
mainTest()    