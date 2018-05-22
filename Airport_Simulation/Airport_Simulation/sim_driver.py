#I have set the global contants at placeholder times untill we figure out
#average times for them. 
#We could also play with them to see how they affect throughput of the airport

#Feel free to add constants, just don't remove any without consulting the team.
#Basically, don't break it.
#============================ GLOBAL CONSTANTS ===============================#
TIME_TO_BOARD	= 60	#In minutes
TIME_TO_DEBOARD = 60	#In minutes
TIME_TO_REFUEL	= 60	#In minutes
TIME_TO_SERVICE = 60	#In minutes
MAX_PASSENGERS  = 150	
TIME_TICKS		= 1440  #In minutes 
NUM_JETS_TO_INITILIZE = 40	#We need to find out how many jets there are at time X. 
							#Time X being the time we start our simulation: 13:00 ? I think we should start at 00:00. 
							#Regardless, we need to know on average how many jets are at the airport at that time
							# 50 X by 120 Y ? 

#========================== END GLOBAL CONSTANTS =============================#


#================================ IMPORTS ====================================#
from classes import *
#============================== END IMPORTS ==================================#


#============================== SIMULATION ===================================#

# Misc Notes:
# We'll need some way of fast-forwarding through the sim.  Worry about that later.

def airport_sim():
	
	#Step 1: Initilize ATC
	tower = ATC()
	
	#Step 2: Initilize Terminals
	init_gates(tower)

	#Step 3: Initilize Jets - Passenger and Cargo	
	init_jets(tower)

	#Step 4: Initilize paths
	init_paths(tower)

	#Step 5: Start Time
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
		pass

#============================ END SIMULATION =================================#

#========================== SIMULATION METHODS ===============================#
def init_gates(atc_object):
	"""Create 80 Gates:
		- 14 A Gates: Numbered 1 - 14 
		- 11 B Gates: Numbered 3 - 14
		- 12 C Gates: Numbered 2 - 3, 9 - 12, 14 - 18, 20
		- 11 D Gates: Numbered 1 - 11
		- 23 Cargo "Gates" Not numbered 		

		All gates will be initilized with CUSTOM COORDINATES to match their
		real life location. 

		Each gate is added to the atc_objects' list of terminals
		"""

	# Passenger Terminals are initilized as P_Terminal
	# Cargo Terminals are initilized as C_Terminal
	# Each terminal will be added to the ATC objects list of terminals by appending it to the list
	#
	# Example: atc_object.terminals.append(terminal) 
	
	pass

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

	# Passenger jets are initilized as P_Jet, cargo jets as C_Jet.
	# Each jet will be added to the appropriate 
	# Just like with terminals
	pass

def init_paths(atc_object):
	""" TODO: Gridsize is 50 x 120
		Each runway, taxiway will have it's own defined path.
		Each path consists of a list of tuples where each tuple is an x,y pair and a slot for a jet:
		A point in a path will look like: [(x,y), jet, direction] 
		
		Basically, each point in a path has the ability to "hold" a jet object. All paths will be kept inside a list
		held by the ATC object. This is so the ATC object can look through a path and see if there are any jets on that 
		path before sending another jet down it. 

		These paths will be defined according to our grid, most will be hardcoded. 

		Most of these paths will have to be hand coded. We can generate some of the stricly vertical and 
		horizontal ones using numpy maybe? 
	
		An adjecency list will also need to be created to maintain what paths connect to what.
		See Example: 

										Path B
										  |
										  |
										  |
										  |
										  |
		Path A: ------------------------- + -------------------------------- Path C
										(2, 2)
		Paths A, B, and C intersect at (2, 2). All paths will have the point (2,2) in their list. 
		The adjency list will be like this:
			1. [(A, [B, C]), (B, [A, C]), (C, [B, A])]  
			2. Select path A, east end
			3. Path A, east end connects to: Path B South end, Path C west end.
				
	"""
	pass
#======================== END SIMULATION METHODS =============================#

#-jet variable with the name, coordinates, and the status(False-in air, true-on ground)
j1 = jet("CA111", 25, 50, False)
j = jet("AA302", 40, 10, True)

A = ATC()

A.land.append(j1)
A.take_off.append(j2)
r1 = runway()
r1.timestamp()
A.takeOff(r1)
r1.timestamp()
A.land(j1)
