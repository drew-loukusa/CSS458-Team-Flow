
#============================ GLOBAL CONSTANTS ===============================#
TIME_TO_BOARD	= 60	#In minutes
TIME_TO_DEBOARD = 60	#In minutes
TIME_TO_REFUEL	= 60	#In minutes
TIME_TO_SERVICE = 60	#In minutes
MAX_PASSENGERS  = 150	
TIME_TICKS		= 30  #In minutes 
TICK = 1				#One minute 
NUM_JETS_TO_INITILIZE = 40	#We need to find out how many jets there are at time X. 
							#Time X being the time we start our simulation: 13:00 ? I think we should start at 00:00. 
							#Regardless, we need to know on average how many jets are at the airport at that time
							# 100 X by 240 Y 

FUEL_MAX = 6000 #In pounds NEED TO FIND HOW MUCH FUEL JETS CARRY but this is close
DELTA_SPEED = 2
TAXI_SPEED = 1
#Initilize paths now to use later
init_paths(PATHS)
label_paths(PATHS)
PATHS  = []				#List of all paths at the airport

NUM_JETS = 0
NUM_JETS_TOOK_OFF = 0
NUM_JETS_LANDED   = 0
TOTAL_JETS_IN_SIM = 0

RUNWAY_L = 0
RUNWAY_M = 1
RUNWAY_R = 2
MAIN_TAXIWAY_SOUTH = 46
MAIN_TAXIWAY_CENTER = 47
MAIN_TAXIWAY_NORTH = 48

TAKEOFF_Q_TAXIWAY = 45

RWL_OPEN = True
RWM_OPEN = True
RWR_OPEN = True

RUNWAYS = {RUNWAY_L: RWL_OPEN, RUNWAY_M: RWM_OPEN, RUNWAY_R: RWR_OPEN}


from classes import *

def genSeg(st, ed, label = False, dir = "None"):
	"""	Method for generateing individual sections of a path.		
		Args: 
		* st	: A tuple (x,y), the start location of the segment
		* ed	: A tuple (x,y), the end location of the segment
		* dir	: A string, the direction of travel for that segment if appliciable (some paths don't have that restriction)

		! NOTE ! : This should only be used to create segments that are horizontal, vertical and paths that have a slope of 1:1. 
					This method cannot handle creating segments which have a slope of say, 5:1 (Not yet anyways).		

		RETURNS:	An object with list of points (and a label and a direction) that can be taken and put into a path. The points that are returned in the list from this 
					method are the points that are described in init_paths: [(x,y), jet]
		
		! NOTE  ! : This method will return an empty list if you try to use it to generate a segment that has a slope other than 0, OO, or 1.
		
	"""
	dif_x = ed[0] - st[0]
	dif_y = ed[1] - st[1]
	jet = False
	seg = []
	dt = 1

	abs_x = abs(dif_x)
	abs_y = abs(dif_y)

	#If generating horizontal segment:
	if(abs_x > 0 and abs_y == 0):
		seg.append([st,jet, label])
		if(dif_x < 0):
			dt = - 1
		for i in range(abs_x):
			last = seg[i][0]
			seg.append([(last[0] + dt, last[1]), jet, label])		

	#If generating vertical segment:
	elif(abs_y > 0 and abs_x == 0):
		seg.append([st,jet, label])
		if(dif_y < 0):
			dt = -1
		for i in range(abs_y):
			last = seg[i][0]
			seg.append([(last[0], last[1] + dt), jet, label])		
	
	#If generating diagonal segment: Currently this creates actual diagonal paths not sudo-diagonal (jagged)
	elif(abs_x > 0 and abs_y > 0):
		dt_x, dt_y = 1,1
		if(dif_x < 0):
			dt_x = -1
		if(dif_y < 0):
			dt_y = -1
		if(abs_x == abs_y):
			seg.append([st,jet, label])
			for i in range(abs_x):
				seg.append([(st[0]+ dt_x, st[1] + dt_y), jet, label])

	path = Path(dir, seg)
	return path

def init_paths(all_paths): 
	""" ARGS: PATHS, the global list that holds paths
	
	TODO: Gridsize is 120 x 240
	Each runway, taxiway will have it's own defined path.
	Each path consists of a list of tuples where each tuple is an x,y pair and a slot for a jet:
	A point in a path will look like: 

	PATH LIST FORMAT:

	PATHS ARE NOW OBJECTS AGAIN
		
	Format: [[(x,y), jet],[(x,y), jet],[(x,y), jet]]
	[[ (1, 0), jet, empty label] 
	[ (1, 1), jet, (index of intersecting path, index of point in intersecting path) 
				
	FORMAT OF ENTRY FOR EACH POINT:	[(x,y), jet] 
		
	Basically, each point in a path has the ability to "hold" a jet object. All paths will be kept inside a list
	held by the ATC object. This is so the ATC object can look through a path and see if there are any jets on that 
	path before sending another jet down it. 	
	"""

	# NOTE:	Diagonal paths need to be handeled slightly differently than horizontal paths or vertical paths 
	#		Moving 1 left then 1 up is not the same as moving diagonally to the same end loc. The diagonal path is "faster".

	#		THE SOLUTION: Once a jet reaches the end of a diagonal segment it will wait a calculated amount of time.
	#					  Because a jet is technically moving faster than it's supposed to, we'll just make it wait a little bit once it stops to balance it out

	#		A possible solution: Don't have diagonal paths, kinda. If you have to curve or do a diagonal path, you just break it up into up down left right movements.
	#		This way we don't have to deal with this weird case of a diagonal being "faster". We'll talk.

	#120x50
	#x2 240x100
#Paths are written from grids (x1,y1) - (x1, y12) and than (x2, y1) (x2, y12)

	#Create the Three Main Runways:
	all_paths.append(genSeg((1,70), (1,235), dir = "North"))	#0
	RUNWAY_L = 0	
	all_paths.append(genSeg((36, 55), (36, 235), dir="North"))  #1
	RUNWAY_M = 1
	all_paths.append(genSeg((45, 4), (45, 235), dir = "North"))	#2
	RUNWAY_R = 2
	all_paths.append(genSeg((60, 1), (60, 235), dir="North-East")) #3
	Terminal_path = 3

	#Paths are written from grids (x1,y1) - (x1, y12) and than (x2, y1) (x2, y2)

	#Paths Connected to Runway Left <-> Center Taxiway
	#See Airport_Grid_WithLabels png for labels
	all_paths.append(genSeg((1, 70), (16, 70), dir	= "East"))			#1E		#4	
	all_paths.append(genSeg((16, 70), (31, 55), dir = "South-East"))	#2SE	#5
	all_paths.append(genSeg((26, 55), (60, 55), dir = "East"))			#3E		#6
	all_paths.append(genSeg((45, 34), (60, 34), dir = "East"))			#9E	    #7 Connects to 5T	
	all_paths.append(genSeg((55, 1), (60, 1), dir	= "North-East"))	#6E		#8
	all_paths.append(genSeg((1, 235), (60, 235), dir = "South-East"))	#10E	#9

def label_paths(PATHS):
	"""Method for labeling each intersection on every path. """

	PATHS[0].p[0][2] = (4, 0)	 #
	PATHS[0].p[144][2] = (9, 0) #

	PATHS[1].p[0][2] = (6, 5)    #
	PATHS[1].p[179][2] = (9, 35) #

	PATHS[2].p[0][2] = (8, 0)	#
	PATHS[2].p[33][2] = (7, 0) #
	PATHS[2].p[54][2] = (6, 18) # 
	PATHS[2].p[230][2] = (9, 44) #

	PATHS[3].p[0][2] = (6, 4) # 10E
	PATHS[3].p[33][2] = (6, 34) #3E
	PATHS[3].p[54][2] = (7, 14) #9E
	PATHS[3].p[232][2] = (9, 59) #6E
	
	PATHS[4].p[0][2] = (0, 0) #
	PATHS[4].p[14][2] = (5, 0) #

	PATHS[5].p[0][2] = (4, 14) #
	PATHS[5].p[14][2] = (6, 0) #

	PATHS[6].p[0][2] = (5, 14) #
	PATHS[6].p[9][2] = (1,0) #
	PATHS[6].p[17][2] = (2,0) #
	PATHS[6].p[33][2] = (7, 53) #
	
	PATHS[7].p[0][2] = (2, 33) #
	PATHS[7].p[14][2] = (3, 33) #

	PATHS[8].p[0][2] = (2, 0) #
	PATHS[8].p[0][2] = (3, 0) #

	PATHS[9].p[0][2] = (0, 144) #
	PATHS[9].p[35][2] = (1, 179) #
	PATHS[9].p[0][2] = (2, 230) #
	PATHS[9].p[0][2] = (3, 233) #
init_paths(PATHS)
label_paths(PATHS)

#========================== END GLOBAL CONSTANTS =============================#


#================================ IMPORTS ====================================#
from classes import *

#============================== SIMULATION ===================================#

# Misc Notes:
# We'll need some way of fast-forwarding through the sim.  Worry about that later.

def airport_sim():
	
	#Step 1: Initilize ATC
	tower = GTC()

	#Step 3: Initilize Jets - Passenger and Cargo	
	init_jets(tower)
	
	#Step 5: Start Time	
	global TIME_TICKS
	for i in range(TIME_TICKS):
		# For each plane in the sim:
			# For planes in the air:
				# Location will be updated based on heading and speed
				# Fuel will be updated based on weight, speed and altitude, and burn rate 
				# Heading will be updated based on path needed to align with runway or holding pattern or avoid other jets -- NOT ANYMORE? Since we arne't simulating this
				# Weight will be updated based on remaining fuel, cargo on board or num passengers, 
			# If a plane in the air is in range to request landing, it will send a landing request ATC
			# If the plane is at a terminal and is ready to taxi it will send a taxi request to ATC
			# If a plane is on the taxiway and is ready to takeoff it will send a takeoff request to ATC
			# If a plane is on the taxiway and is ready to go to terminal it will send a go-to terminal request to ATC
		# The ATC will:
			# Take in requests from planes in the sim
			# Issue the appropriate instructions for planes based on known factors 
			# Instruct the plane or planes with the highest landing priority to land
			# Instruct planes requesting to land to enter holding pattern or land
			# Instruct planes requesting to taxi to runway to hold or begin taxiing
			# Instruct planes requesting to taxi to terminal to hold or begin taxiing
			# Update landing priorities for each plane in sim
		# The terminals will:
			# For planes that are at a terminal:
			# Refuel the plane: Planes fuel will be updated
			# Board passengers or cargo 	
		print("Before update")
		tower.update_jets()		
		print("After update")
		print(TIME_TICKS)
		TIME_TICKS -= 1

#============================ END SIMULATION =================================#

#========================== SIMULATION METHODS ===============================#

def init_jets(atc_object):
	"""	Create NUM_JETS_TO_INITILIZE and place them at terminals.
		A few jets will be placed on taxiways, and a few will be 
		initilized in the air. 
		
		Of the jets in the air there will be three places they can 
		be initilized: 
			1. Landing
			2. In a holding pattern waiting to land
			3. Incoming to the airport

		These are not shown on screen and are only simulated in name 
		only. Depending on where they get initilized, they'll get 
		placed in different ATC lists. The ATC object has a list for
		each place a jet can get created. 

		Most will be passenger jets, some will be cargo jets.
	"""
	test_jet = Jet("TEST 747", 1000, 398000, 2, 0, 0, TAXI_SPEED)
	atc_object.jets.append(test_jet)
	
	# Passenger jets are initilized as P_Jet, cargo jets as C_Jet.
	# Each jet will be added to the appropriate 
	# Just like with terminals

def init_paths(all_paths): 
	""" ARGS: PATHS, the global list that holds paths
	
	TODO: Gridsize is 50 x 120
		Each runway, taxiway will have it's own defined path.
		Each path consists of a list of tuples where each tuple is an x,y pair and a slot for a jet:
		A point in a path will look like: 

		PATH LIST FORMAT:

		PATHS ARE NOW OBJECTS AGAIN
		
		Format: [[(x,y), jet],[(x,y), jet],[(x,y), jet]]
		[[ (1, 0), jet, empty label] 
        #[ (1, 1), jet, (index of intersecting path, index of point in intersecting path) 
				
		FORMAT OF ENTRY FOR EACH POINT:	[(x,y), jet] 
		
		Basically, each point in a path has the ability to "hold" a jet object. All paths will be kept inside a list
		held by the ATC object. This is so the ATC object can look through a path and see if there are any jets on that 
		path before sending another jet down it. 

		These paths will be defined according to our grid, most will be hardcoded. 

		Most of these paths will have to be hand coded. We can generate some of the stricly vertical and 
		horizontal ones using numpy maybe? 
	

		#NOT DOING INTERSECTIONS: INSTEAD WE ARE DOING LABELS TO "LABEL" INTERSECTIONS:

		ASK DREW ABOUT IT IF IT HASN'T BEEN DONE YET
		
	"""

	# NOTE:	Diagonal paths need to be handeled slightly differently than horizontal paths or vertical paths 
	#		Moving 1 left then 1 up is not the same as moving diagonally to the same end loc. The diagonal path is "faster".

	#		THE SOLUTION: Once a jet reaches the end of a diagonal segment it will wait a calculated amount of time.
	#					  Because a jet is technically moving faster than it's supposed to, we'll just make it wait a little bit once it stops to balance it out

	#		A possible solution: Don't have diagonal paths, kinda. If you have to curve or do a diagonal path, you just break it up into up down left right movements.
	#		This way we don't have to deal with this weird case of a diagonal being "faster". We'll talk.

	#120x50
	#x2 240x100

		#Create the Three Main Runways:
	all_paths.append(genSeg((1,70), (1,235), dir = "North"))	#0
	RUNWAY_L = 0	
	all_paths.append(genSeg((36, 55), (36, 235), dir="North"))  #1
	RUNWAY_M = 1
	all_paths.append(genSeg((45, 4), (45, 235), dir = "North"))	#2
	RUNWAY_R = 2
	all_paths.append(genSeg((60, 1), (60, 235), dir="North-East")) #3
	Terminal_path = 3

	#Paths are written from grids (x1,y1) - (x1, y12) and than (x2, y1) (x2, y2)

	#Paths Connected to Runway Left <-> Center Taxiway
	#See Airport_Grid_WithLabels png for labels
	all_paths.append(genSeg((1, 70), (16, 70), dir	= "East"))			#1E		#4	
	all_paths.append(genSeg((16, 70), (31, 55), dir = "South-East"))	#2SE	#5
	all_paths.append(genSeg((26, 55), (60, 55), dir = "East"))			#3E		#6
	all_paths.append(genSeg((45, 34), (60, 34), dir = "East"))			#9E	    #7 Connects to 5T	
	all_paths.append(genSeg((55, 1), (60, 1), dir	= "North-East"))	#6E		#8
	all_paths.append(genSeg((1, 235), (60, 235), dir = "South-East"))	#10E	#9

def genSeg(st, ed, label = False, dir = "None"):
	"""	Method for generateing individual sections of a path.		
		Args: 
		* st	: A tuple (x,y), the start location of the segment
		* ed	: A tuple (x,y), the end location of the segment
		* dir	: A string, the direction of travel for that segment if appliciable (some paths don't have that restriction)

		! NOTE ! : This should only be used to create segments that are horizontal, vertical and paths that have a slope of 1:1. 
					This method cannot handle creating segments which have a slope of say, 5:1 (Not yet anyways).		

		RETURNS:	An object with list of points (and a label and a direction) that can be taken and put into a path. The points that are returned in the list from this 
					method are the points that are described in init_paths: [(x,y), jet]
		
		! NOTE  ! : This method will return an empty list if you try to use it to generate a segment that has a slope other than 0, OO, or 1.
		
	"""
	dif_x = ed[0] - st[0]
	dif_y = ed[1] - st[1]
	jet = False
	seg = []
	dt = 1

	abs_x = abs(dif_x)
	abs_y = abs(dif_y)

	#If generating horizontal segment:
	if(abs_x > 0 and abs_y == 0):
		seg.append([st,jet, label])
		if(dif_x < 0):
			dt = - 1
		for i in range(abs_x):
			last = seg[i][0]
			seg.append([(last[0] + dt, last[1]), jet, label])		

	#If generating vertical segment:
	elif(abs_y > 0 and abs_x == 0):
		seg.append([st,jet, label])
		if(dif_y < 0):
			dt = -1
		for i in range(abs_y):
			last = seg[i][0]
			seg.append([(last[0], last[1] + dt), jet, label])		
	
	#If generating diagonal segment: Currently this creates actual diagonal paths not sudo-diagonal (jagged)
	elif(abs_x > 0 and abs_y > 0):
		dt_x, dt_y = 1,1
		if(dif_x < 0):
			dt_x = -1
		if(dif_y < 0):
			dt_y = -1
		if(abs_x == abs_y):
			seg.append([st,jet, label])
			for i in range(abs_x):
				seg.append([(st[0]+ dt_x, st[1] + dt_y), jet, label])
	#call Path method-parameter dir and seg to generate the path
	path = Path(dir, seg)
	return path

def updatePathDirection(PATHS):
	"""	Update the direction of directed paths that change when runways switch direction. 
		ARS: PATHS = Global list of paths
	"""
	#path loop gives 8 possible directions of a jet on a path
	for path in PATHS:
		if(path.dir == "North"):
			path.dir = "South"

		if(path.dir == "South"): 
			path.dir = "North"

		if(path.dir == "East"): 
			path.dir = "West"

		if(path.dir == "West"): 
			path.dir = "East"

		if(path.dir == "North-East"): 
			path.dir = "South-West"

		if(path.dir == "South-West"): 
			path.dir = "North-East"

		if(path.dir == "South-East"): 
			path.dir = "North-West"

		if(path.dir == "South-West"): 
			path.dir = "North-East"	
	
#======================== END SIMULATION METHODS =============================#

airport_sim()