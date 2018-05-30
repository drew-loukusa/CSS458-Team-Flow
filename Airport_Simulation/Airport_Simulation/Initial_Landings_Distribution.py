#This is the Landings Distribution Method

#It uses a uniform random generator to come up with the distribution of thelandings
#There are different probabilities used at different points in times
#The time is counted at each minute
#There is a rush time probability, and a regular probability

import random

TYPE_P = "PASSANGER"
TYPE_C = "CARGO"
TIME_LANDING = 3				#in minutes
TIME_LANDING_DEVIATION = 1	

#FROM LEFT to RIGHT these are the runway numbers, no matter the direction from which a plane is landing
RUNWAYS = (1,2,3)

class Landing:	#Will be appended to the distribution list
    def __init__(self, timeIn, runwayIn, planeTypeIn):	
        self.time	= timeIn			# minutes the landing will take
        self.runway = runwayIn			# runway on which the plane will be landing
        self.planeType = planeTypeIn	# the type of plane can be "PASSENGER" or "CARGO"
		
class Gap: 		#Will be appended to the distribution list
    def __init__(self, timeIn, runwayIn):
        self.time = timeIn				#minutes the gap will take
        self.runway = runwayIn			#the runway on which this gap is available

		
def GeneratePlaneDistribution(hour_start=0, hour_end=24, landing_limit=100000, regular_plane_prob=0.6, high_plane_prob=0.8):
    """ - The hours parameters has to be given in Military Time:"
    		   MIN: 0
		      MAX: 24
		
		  - The probability should be given in decimal:
			   MIN: 0
			   MAX: 1
    """
	
    TIME_LANDING = 2				#in minutes
    TIME_LANDING_DEVIATION = 1	
    MORNING_RUSH_RANGE = (360, 600)		#these are the start and end in minutes of morning rush hour. 06:00 - 10:00 Military
    EVENING_RUSH_RANGE = (840, 1200)  #these are the start and end in minutes of evening rush hour. 14:00 - 20:00
    
    HS = hour_start
    HE = hour_end
    LL = landing_limit
    RPP = 1.0-regular_plane_prob
    HPP = 1.0-high_plane_prob
	
    total_hours	= HE - HS
    total_minutes = total_hours * 60
	
    landingCount = 0
    gapCount = 0
	
    currentMinutes = 0
    distribution = []		#will keep track of Landings and Gaps
	
    while (currentMinutes < total_minutes):

        if (landingCount < LL):
            
            if ((currentMinutes >= MORNING_RUSH_RANGE[0]) and (currentMinutes <= MORNING_RUSH_RANGE[1])):
                
                LandingChance = RandP()
                if(LandingChance > HPP):                                       
                    dT, tempLanding = generateLanding() 
                    distribution.append(tempLanding)
                    landingCount += 1
                    currentMinutes += dT
                    
                else:  
                    dT, tempGap = generateGap()
                    distribution.append(tempGap)
                    gapCount += 1
                    currentMinutes += dT
                    
            if ((currentMinutes >= EVENING_RUSH_RANGE[0]) and (currentMinutes <= EVENING_RUSH_RANGE[1])):
                
                LandingChance = RandP()
                if(LandingChance > HPP):                                       
                    dT, tempLanding = generateLanding() 
                    distribution.append(tempLanding)
                    landingCount += 1
                    currentMinutes += dT
                    
                else:  
                    dT, tempGap = generateGap()
                    distribution.append(tempGap)
                    gapCount += 1
                    currentMinutes += dT
            
            else:
                LandingChance = RandP()
                if(LandingChance > RPP):                         #this is where the change is. RPP instead of HPP                     
                    dT, tempLanding = generateLanding() 
                    distribution.append(tempLanding)
                    landingCount += 1
                    currentMinutes += dT
                    
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
    
    return (landingCount, gapCount, currentMinutes, distribution)
		
		
	

def RandP():	
	return random.random()

def generateLanding():
    tempRunway = random.randint(1,3)
                    
    tempTypeProb = RandP()
    #print(tempTypeProb)
    tempPlaneType = None
    if (tempTypeProb > 0.2):
        tempPlaneType = TYPE_P
    else:
        tempPlaneType = TYPE_C
                        
    tempTime = round(RandP()) + TIME_LANDING   
    #print(tempTime)
                        
    retLanding = Landing(tempTime,tempRunway,tempPlaneType)
    return (tempTime, retLanding)


def generateGap():
    tempRunway = random.randint(1,3)
    tempGapTime = random.randint(1,2)
          
    retGap = Gap(tempGapTime, tempRunway)
    return (tempGapTime, retGap)
    
#Test
lCount, gCount, CM, landings = GeneratePlaneDistribution()
print("Landings:" + str(lCount))
print("Gaps:" + str(gCount))
print("TotalMinutes:" + str(CM))
print()
#print(landings)