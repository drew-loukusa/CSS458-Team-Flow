
import time
import Runway as runway
import random as R
from threading import *
from sim_driver import *
#=========================== SIMULATION OBJECTS ==============================# 

# NOTE: I have commented out some Jet class variables so I can get some basic implemenation done. 
#		Will be added back in later as needed? 

class Jet:	#Base jet class
	def __init__(self, name, fuel, weight, apt, path, pathIndex, speed, gate = None, tag = 0):	
		self.name	= name		#AA302
		self.fuel	= fuel		#In gallons?		
		self.weight	= weight	#In pounds
		self.apt	= apt		#Process Status
		self.path	= path		#Index of the path in the PATHS list that the jet is on currently
		self.loc	= pathIndex #Index in the path that the jet is on
		self.history = []		#Stores each of the preceding variables for each time step of simulation
		self.speed = speed		#Ground speed (MPH) ?
		self.target_gate =	gate 
		self.time_at_gate = tag #Tracks how long the jet has to be at the gate. Time gets added by boarding, refueling
		#self.atc_status		#ATC Status
		#self.emg_status		#Emergency Status
		#self.heading			#In degrees (0 - 360)
		#self.altitude			#In Feet
		#self.burn_rate			#Gallons per hour? 

	def logData(self):
		"""	Store all class variables' state in the current time step in the jets' history.
			History is a list of lists. Each list in the list represents one time step of the simulation
		"""
		history.apppend([fuel, weight, path, apt_status, loc])
		
class P_Jet(Jet): #Passenger jet
	def __init__(self, name, fuel, weight, x, y):
		self.passengers		#Number of passengers. Avg weight will be 150 Lb per passenger
		self.ploy = TIME_TO_BOARD

class C_Jet(Jet): #Cargo jet 
	def __init__(self, name, fuel, weight, x, y):
		super(C_Jet, self).__init__(name, fuel, weight, x,y)		
		self.cargo			#In pounds

class ATC:	#Air Traffic Control: Serves as main logic controller of simulation
	def __init__(self):				
		self.jets = []				#List of all jets in simulation
		self.jets_in_air = []
		self.holding_q	= []		#This should be treated as a queue: FIFO		
		self.takeoff_q	= []			
		self.gates		= []		#List of all gates at the airport		

	def update_jets():
		""" Updates the state of all jets in the simulation. 
			Path switching when necessary is done in this method."""
		for jet in jets:
			
			# NOT CURRENTLY USING FIRST TWO STATUSES: Spawning jets directly 
			# onto runway using mostly uniform distribution. With the exception
			# of rushours which have a higher probability of a jet landing.

			
			#----------------- ! IMPORTANT ! -------------------------#

			#Need to add in the spawning of NEW jets RIGHT HERE
			#New jets get added to the sim at this point

			#----------------- ! IMPORTANT ! -------------------------#

			

			#If jet is landing
			if(jet.apt == 2):
				
				#1. Move it down the runway to a spot where it stops and takes an open taxiway
				#	or a taxiway with room. 
				#2. Change status to TXG - 4 - Taxiing to gate

				# If slowing down - Keep moving jet
				if(jet.speed > TAXI_SPEED):
					move(jet)
					reduceSpeed(jet)

				# If jet has reached taxiing speed after most recent 
				# reduceSpeed() call, look for taxiways
				if(jet.speed == TAXI_SPEED):				
					jet.apt = 4				  # Change Status to TXG - Taxiing to gate
					switch_paths(jet)		  # Switch paths e.g. move onto taxiway if any available
					move(jet)			  # Move it either way: If it didn't move onto a path, keep moving
											  #		If it found a path it it wasn't valid, keep moving
											  #		If it it found a path and switched to it, still move it.
			#If jet is going to a runway:
			elif(jet.apt == 3):
				#1. Move it from the terminal to the MAIN taxiway
				switch_paths(jet) #If available, switch to the path
				
				#2. Move it UP or DOWN the main taxiway untill it reaches the top or bottom of the airport
				move(jet)		

				#3. Move it LEFT untill it reaches the takeoff queue OR it reaches the runway				
				#4. IF TAKING OFF: Change status to TA - 6 - Taking off 
				#5. IF IN TAKEOFF QUEUE: No change to status
				pass

			#If jet is going to gate:
			elif(jet.apt == 4):
				#1a. Pick a random gate for the jet to go to if it hasn't been given one:
				if(jet.target_gate == None):
					jet.target_gate = pickGate() #target_gate is an integer index of the gate picked in the gates [] list.
				
				#1b. Move jet east generally until it reaches taxi-to-gate queue or reaches MAIN taxiway
				#2. Move jet UP or DOWN MAIN taxiway until it reaches the path for it's random assigned gate
				#3. Move jet onto gate path
				#4. Move jet down gate path to gate
				# 1b, 2, and 4 are done just by calling move(jet). 
				#5. Dock jet with the gate and change it's status to TG: 5 - At a gate				

				# Check if gate path is next to us:
				# If yes, then switch paths to that path
				if(check_for_intersection(jet, jet.target_gate)):
					switch_paths(jet)

				#Set status of jet or move it:
				if(gates[jet.target_gate].jet != False):
					jet.apt = 5 #Set status of jet
				else:
					move_jet(jet)
				
		
				pass
			
			#If jet is at a gate:
			elif(jet.apt == 5):
				# If the jet hasn't started the gate process, do so:
				if(jet.time_at_gate > 0):					
					index = jet.target_gate
					gates[index].deboard(jet)	#1. Deboard passengers
					gates[index].refuel(jet)	#2. Refuel and service
					gates[index].service(jet)
					gates[index].board(jet)		#3. Board Passengers					
				
				# Decrease time at gate by one time tick
				else: 
					jet.time_at_gate -= 1 
				
				# If a jet is done with the gate process:
				# change it's status to TXR - Taxiing to runway
				# and undock the jet from the gate.
				if(jet.time_at_gate == 0):
					jet.apt = 3
					gates[jet.target_gate].jet = False
			
			#If jet is taking off:
			elif(jet.apt == 6):				
				#Move the jet down the runway:
				not_at_end = move(jet)

				# If we arn't moving anymore then we're at the end of the runway:
				# Remove the jet from the simuation and increment the NUM_JETS_TOOK_OFF 
				if(not not_at_end):
					NUM_JETS_TOOK_OFF += 1
					jets.remove(jet)

	def check_for_intersection(self, jet, target_path = None):
		"""	Checks the current location of the jet to see if the jet is on an intersection.
			Can be made to check for a specific path by passing in an index for a path for 
			the PATHS list. 

			Returns True if the jet is on an intersection.
			Returns True if the jet is on the intesection specified by target_path
			Returns False if it's not either of the above.
		"""

		#Current location in a single path in PATHS
		cur_loc = PATHS[jet.path][jet.loc] 

		#If on an intersection:
		if(cur_loc.label != False and target_path == None):
			return True
		
		#If on a specified intersection:
		elif(cur_loc.label != False and target_path == PATHS[cur_loc.label[0]]):
			return True	
		
		return False		

	def switch_paths(self, jet, directions = None):
		"""	Method for moving a jet from one path to another. Method checks for
			paths that intersect the jets current location and will switch a jet 
			to a path depending on the apt_status of the jet and if a potential path is open.
			
			Can override the direction of paths that the method switches to by passing in a list
			through the direction parameter. Ex: ["North", "South"]
			"""

		path = PATHS[jet.path] 				
		if(path[jet.loc][2] != False):

			tup = PATHS[path[jet.loc][2]]	 #Grab tuple with info from the path point where jet is.
			Nextpath = PATHS[tup[0]]		 #Grab potential path
			correct_path_dir = False		
			clear_ahead = False					

			#Set valid_dirs to the directons based on apt_status of the jet. 
			valid_dirs = [] 
			if(direction != None):
				valid_dirs = directions
			elif(jet.apt == 3): #TXR 
				valid_dirs = [ "East", "North-East", "South-East","None"]
			elif(jet.apt == 4): #TXG
				valid_dirs = [ "West", "North-West", "South-West", "None"]

			# Check if the path has a valid direction and is not blocked
			if(NextPath.dir in valid_dirs):
				correct_path_dir = True
			if(checkAhead(jet)): #Not implemented 
				clear_ahead = True

			# If path has valid direction and is clear:
			# Switch jet to that path 
			if(correct_path_dir and clear_ahead):						
				jet.path = tup[0]
				jet.loc	 = tup[1]
		
	def checkAhead(self, jet):
		pass
			
	def pickGate(self):
		"""	Picks an open gate at random for the jet to go to.
			Returns an int which is the index of the gate selected. """ 
		gate = gates[R.randint(0, len(gates))]
		while(gate.jet != False):
			index = R.randint(0, len(gates))
			gate = gates[index]		

		return index

	def reduceSpeed(self, jet):
		""" Reduces the speed of the jet by a calulated amount based on the jets weight, and current speed.
			Currently reduces the jets speed by a constant
		"""
		jet.speed -= jet.speed - DELTA_SPEED #TALK TO SEAN, GET THIS FIXED

	def move(jet):
		""" Method for moving a jet. This is done by changing which slot in a path list the jet occupies.
			This method does not switch paths, it only checks for jet collision and path ending.

			Returns true if the jet was moved, false if it wasn't moved. 
		"""		
		dD = 1	#Change in distance of the jet calculated by it's speed. Most jets will have the same speed: TAXI_SPEED
		path = PATHS[jet.path]
		
		def changeListPosition(positive): 
			"""Nested function for changing the position of a jet in a list """
			if(positive == False):
				dD = dD - 2*dD

			#Check the slot imediately ahead of this jet. 
			clear_ahead = False
			if(path.p[jet.loc + dD ][1] != False):
				clear_ahead = True
			
			#Check if the path ends
			end_path = False
			if(jet.loc + dD >= path.size() or jet.loc + dD < 0):
				end_path = True

			if(clear_ahead and not end_path):
				path.p[jet.loc + dD ][1] = jet
				path.p[jet.loc][1] = False
				jet.loc += dD 
			else:
				return False
	
		if(path.dir == "East" or path.dir == "North"):
			return changeListPosition(True)

		if(path.dir == "West" or path.dir == "South"):
			return changeListPosition(False)

		if(path.dir == "South-East" or path.dir == "North-East"):						
			return changeListPosition(True)

		if(path.dir == "North-West" or path.dir == "South-West"):
			return changeListPosition(False)

	def landing(self, runway):
		#-if runway is locked, the jet can land in a timely fashion
		if(runway.lock.locked()):
			hold = Time(10, land, runway)
			hold.start()
			#print("Jet in hold")
		else:
		#-else, the current jet will be listed into the first one in the queue
			#[current]jets = cur
			cur = self.jets_land.enqueue(0)
			time.sleep(10)
			runway.landingComplete(cur)

	def taking_off(self, runway):
		if(runway.lock.locked()):
			pass
		else:
			pass
		#- it will be listed as the first jet on the runway

class Path:
	def __init__(self, dir = "None", list = []):		
		self.dir = dir
		self.p = list
	#Note:	Tuple: (Index of path in PATHS which intersects THIS path, index of point in path which intersects this path)						
	#
	#		After you've created this path, you may create other paths which intersect this path. 
	#		If you do this, you must access THIS list and label the spots which got intersected.	
	#									Path B
	#									 |
	#		Path A ----------------------|--------------------------- Path A End
	#									 |
	#									 |
	#									Path B
	#
	#		Path A is intersected at (1, 1) by path B. So Path A = [[ (1, 0), jet, empty label] 
	#															    [ (1, 1), jet, (index of intersecting path, index of point in intersecting path)
																 
	#Accessing the label:	PATHS[path index][point index][2][ pick 0 or 1 ] ^^^^^^^^^


class Gate: #Base Terminal class
	def __init__(self, x,y):
		self.loc = (x,y)	#Location of terminal
		self.jet = False;	#Each terminal can hold a single jet		
		
	def refuel(self, jet):		
		jet.fuel = FUEL_MAX
		jet.time_at_gate += TIME_TO_REFUEL

	def deboard(self, jet): 		
		jet.time_at_gate += TIME_TO_DEBOARD
	
	def service(self, jet):		
		jet.time_at_gate += TIME_TO_SERVICE					

	def board(self, jet):					#After being serviced, board passengers
		jet.time_at_gate += TIME_TO_BOARD   #This takes TIME_TO_BOARD amount of time	

class P_Gate(Gate): #Passenger Terminal
	def __init__(self):
		pass

	def deboard_passengers(self, jet): 
		pass

	def service(self, jet):		#After deboarding, the jet must be made ready for the next trip
		pass					#This process takes TIME_TO_SERVICE amount of time

	def board_passengers(self, jet):	#After being serviced, board passengers
		pass							#This takes TIME_TO_BOARD amount of time	
	
class C_Gate(Gate): #Cargo Terminal
	def __init__(self, x, y):
		self.loc = (x,y)

	def unload_cargo(self, jet):
		pass

	def service(self, jet):
		pass

	def load_cargo(self, jet):
		pass

#=========================== SIMULATION OBJECTS ==============================#

#============================== JET STATUSES =================================#
from enum import Enum
class ap_stat(Enum):	#Airport Process Status
	A = 0		#In the air
	H = 1		#In holding pattern
	L = 2		#Landing
	TXR = 3		#Taxiing to runway
	TXG = 4		#Taxiing to gate
	TG = 5		#At a gate
	TA = 6		#Taking off

class atc_stat(Enum):	#Jet ATC Status
	AW = 0		#Awaiting instructions from ATC
	EX = 1		#Executing instructions from ATC
	IN = 2		#Inactive - not requesting clearance, not executing anything

class e_stat(Enum):	#Emergency Status
	n = 0		#Normal, no emergency
	e = 1		#Emergency 
#============================ END JET STATUSES ================================#
