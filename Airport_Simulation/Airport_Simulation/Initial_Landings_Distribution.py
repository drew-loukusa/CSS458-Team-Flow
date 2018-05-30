#This is the Landings Distribution Method

#It uses a uniform random generator to come up with the distribution of thelandings
#There are different probabilities used at different points in times
#The time is counted at each minute
#There is a rush time probability, and a regular probability

import random

TYPE_P = "PASSANGER"
TYPE_C = "CARGO"

#FROM LEFT to RIGHT these are the runway numbers, no matter the direction from which a plane is landing
RUNWAYS = (1,2,3)

class Landing:	#Will be appended to the distribution list
    def __init__(timeIn, runwayIn, planeTypeIn, ):	
        self.time	= timeIn			# minutes the landing will take
        self.runway = runwayIn			# runway on which the plane will be landing
        self.planeType = planeTypeIn	# the type of plane can be "PASSENGER" or "CARGO"
		
class Gap: 		#Will be appended to the distribution list
    def __init__(timeIn, runwayIn):
        self.time = timeIn				#minutes the gap will take
        self.runway = runwayIn			#the runway on which this gap is available

		
def GeneratePlaneDistribution(hour_start=0, hour_end=24, plane_limit=100000, regular_plane_prob=0.6, high_plane_prob=0.8):
    """	- The hours parameter has to be given in Military Time:"
			MIN: 0
			MAX: 24
		
		- The probability should be given in decimal:
			MIN: 0
			MAX: 1
    """
	
    TIME_LANDING = 3				#in minutes
    TIME_LANDING_DEVIATION = 0.5
	
    MORNING_DENSITY_RANGE = ()		#these are the minutes.
	
    hs = hour_start
    he = hour_end
    pl = plane_limit
    RPP = regular_plane_prob
    HPP = high_plane_prob
	
    total_hours	= he - hs
    total_minutes = total_hours * 60
	
    planeCount = 0
    gapCount = 0
	
    distribution = []		#will keep track of Landings and Gaps
	
    while (len(distribution) < total_minutes):

        if (planeCount > pl):
            pass
		
		
	

def RandP():	
	return random.random()