import time
import Runway as runway
import random as R
from threading import *
from sim_driver import *
#=========================== SIMULATION OBJECTS ==============================# 

# NOTE: I have commented out some Jet class variables so I can get some basic implemenation done. 
#		Will be added back in later as needed? 

class Jet:	#Base jet class
	def __init__(self, name, fuel, weight, apt, path, pathIndex, speed, gate = None, tag = 0, runway_picked = None):	
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
		self.runway_picked = 2	#Tracks which runway the jet is going to
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

class GTC:	#Ground Traffic Control: Serves as main logic controller of simulation
	def __init__(self):				
		self.jets = []				#List of all jets in simulation
		self.jets_in_air = []
		self.holding_q	= []		#This should be treated as a queue: FIFO		
		self.takeoff_q	= []			
		self.gates		= []		#List of indexs in the main taxiway that have "gates"	
		self.gates_in_use = []		#Gate indexs get moved from gates to this when in use

	def update_jets(self):
		""" Updates the state of all jets in the simulation. 
			Path switching when necessary is done in this method."""
		print("update Called")
		for jet in self.jets:
			
			# NOT CURRENTLY USING FIRST TWO STATUSES: Spawning jets directly 
			# onto runway using mostly uniform distribution. With the exception
			# of rushours which have a higher probability of a jet landing.

			
			#----------------- ! IMPORTANT ! -------------------------#

			#Need to add in the spawning of NEW jets RIGHT HERE
			#New jets get added to the sim at this point

			#----------------- ! IMPORTANT ! -------------------------#


			if(TIME_TICKS % 5 == 0):
				
				#Pick a random OPEN runway, left middle right.
				#If there are no open runways, then do not spawn a new jet
				
				if(RWL_OPEN or RWM_OPEN or RWR_OPEN):
					picked = R.randint(0,2)
					print("Before picking runway")
					while(RUNWAYS[picked] == False):
						picked = R.randint(0,2)					
					print("After picking runway")

					path = PATHS[picked]
					loc = len(PATHS[picked].p) - 1
					new_jet = Jet("Testy Boi", 6000, 300000, 2, path, loc, 5000)
					
					self.jets.append(jet)
					global NUM_JETS_LANDED
					NUM_JETS_LANDED += 1
					global NUM_JETS
					NUM_JETS += 1
					global TOTAL_JETS_IN_SIM
					TOTAL_JETS_IN_SIM += 1
					

			#-------------------------- If jet is landing --------------------------#
			if(jet.apt == 2):
				print("Case 2")
				#Change status of ruway to closed if not already changed:				
				if(RWL_OPEN and RWM_OPEN and RWR_OPEN):
					self.change_runway_status(jet, False)
				#1. Move it down the runway to a spot where it stops and takes an open taxiway
				#	or a taxiway with room. 
				#2. Change status to TXG - 4 - Taxiing to gate

				# If slowing down - Keep moving jet
				#if(jet.speed > TAXI_SPEED):
				#	move(jet)
				#	reduceSpeed(jet)

				# If jet has reached taxiing speed after most recent 
				# reduceSpeed() call, look for taxiways
				if(jet.speed == TAXI_SPEED):	
					self.change_runway_status(jet, True)
					jet.apt = 4				  # Change Status to TXG - Taxiing to gate
					self.switch_paths(jet)		  # Switch paths e.g. move onto taxiway if any available
					self.move(jet)			  # Move it either way: If it didn't move onto a path, keep moving
											  #		If it found a path it it wasn't valid, keep moving
											  #		If it it found a path and switched to it, still move it.

			#-------------------------- If jet is going to a runway: ---------------#
			elif(jet.apt == 3):						
				print("Case 3")
				# 1. Move the jet to the main taxiway
				# 2. Move the jet up and down the main taxiway
				#3. Move it LEFT untill it reaches the takeoff queue OR it reaches the runway				
				#4. IF TAKING OFF: Change status to TA - 6 - Taking off 
				#5. IF IN TAKEOFF QUEUE: No change to status
				Moved = self.move(jet)
				#If the jet cannot be moved:
				if(not Moved):				
					# Move it from the terminal to the MAIN taxiway
					if(check_for_intersection(jet, MAIN_TAXIWAY_SOUTH)):
						self.switch_paths(jet, ["North", "South"]) #If available, switch to the main taxiway
					
					#If it's already on the main taxiway, check for the taxiway that will take it to the runways:
					elif(check_for_intersection(jet, 45)):
						self.switch_paths(jet, ["West"])					
					
					 #Do nothing if there's a jet ahead of this jet
					elif(P[jet.loc + 1].jet != False):
						pass
					
					#If this jet isn't in one of the other situations, then it's next to runway right read to pick a runway:
					elif(True):																	
						
						#If a runway hasn't been picked yet, pick one.
						if(jet.runway_picked == None):
							jet.runway_picked = R.randint(0,1)
							if(jet.runway_picked == 1):
								jet.runway_picked +=1 

						#If we picked runway right:
						elif(runway_picked == 2):
							if(RWR_OPEN):								
								#Change status so we can move it onto the runway
								jet.apt = 6		
								
								#Move it onto the runway
								self.move(jet)		
								
								#Switch the path of the jet to the runway
								self.switch_paths()	
						
						#If we picked runway left
						if(runway_picked == 0):										

							#If crossing runway right:
							if(PATHS[jet.path][jet.loc - 1]  == 2):							
								jet.apt = 6								
								# Move the jet across the runway onto the other taxiway
								# Switch paths if necessary
								if(not move(jet)):
									self.switch_paths(jet, ["West"])
							
								#Change the status 
								jet.apt = 3
							
							#If next to runway left: 
							elif(PATHS[jet.path][jet.loc - 1] == 2):
								if(RWL_OPEN):
									jet.apt = 6
									self.move(jet)
									self.switch_paths(jet, ["South"])
						
			#-------------------------- If jet is going to gate: -------------------#
			elif(jet.apt == 4):
				print("Case 4")
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
				if(jet.loc == jet.target_gate):
					#"Move" jet to gate 
					PATHS[jet.loc].p[jet.loc][3] = jet						
					PATHS[jet.loc].p[jet.loc][1] = False
					
					#Set status of jet
					jet.apt = 5	
				else:
					self.move_jet(jet)
			
			#-------------------------- If jet is at a gate: ------------------#
			elif(jet.apt == 5):
				print("Case 5")
				# If the jet hasn't started the gate process, do so:
				if(jet.time_at_gate > 0):					
					index = jet.target_gate
					self.deboard(jet)	#1. Deboard passengers
					self.refuel(jet)	    #2. Refuel and service
					self.service(jet)
					self.board(jet)		#3. Board Passengers					
				
				# Decrease time at gate by one time tick
				else: 
					jet.time_at_gate -= 1 
				
				# If a jet is done with the gate process:
				# change it's status to TXR - Taxiing to runway
				# Undock it from the gate and move it back on the path if the path is clear.
				# We are not simulating the path to the gate beacuse we are pressed for time.
				# We'll just add a little time the jet is at the gate to simulate the jet moving to and from the terminal. 
				if(jet.time_at_gate == 0):
					jet.apt = 3
					PATH[jet.path].p[jet.loc].gate = False
					PATH[jet.path].p[jet.loc].jet = jet

			
			#-------------------------- If jet is taking off: -----------------#
			elif(jet.apt == 6):				
				print("Case 2")
				#Move the jet down the runway:
				not_at_end = move(jet)

				# If we arn't moving anymore then we're at the end of the runway:
				# Remove the jet from the simuation and increment the NUM_JETS_TOOK_OFF 
				if(not not_at_end):
					NUM_JETS_TOOK_OFF += 1
					jets.remove(jet)
		print("End of update")

	def change_runway_status(self, jet, open_or_closed):
		"""	Method for changing the status of a runway
			Args: - open_or_closed : True or False
				    Used to open or close the runway

			! NOTE ! :	If opening a runway this must be called before jet is moved off the runway.
						This method uses the jets current location to open the correct runway
		"""
		if(jet.path == 0):
			RWL_OPEN = open_or_closed
		if(jet.path == 1):
			RWM_OPEN = open_or_closed
		if(jet.path == 2):
			RWR_OPEN = open_or_closed

	def check_for_intersection(self, jet, target_path = None):
		"""	Checks the current location of the jet to see if the jet is on an intersection.
			Can be made to check for a specific path by passing in an index for a path for 
			the PATHS list. 

			Returns True if the jet is on an intersection.
			Returns True if the jet is on the intesection specified by target_path
			Returns False if it's not either of the above.
		"""

		#Current location in a single path in PATHS
		cur_loc = PATHS[jet.path].p[jet.loc] 

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
		if(path.p[jet.loc][2] != False):

			tup = path.p[jet.loc][2]		#Grab tuple with info from the path point where jet is.
			NextPath = PATHS[tup[0]]		#Grab potential path
			correct_path_dir = False		
			clear_ahead = False					

			#Set valid_dirs to the directons based on apt_status of the jet. 
			valid_dirs = [] 
			if(directions != None):
				valid_dirs = directions
			elif(jet.apt == 3): #TXR 
				valid_dirs = [ "East", "North-East", "South-East","None"]
			elif(jet.apt == 4): #TXG
				valid_dirs = [ "West", "North-West", "South-West", "None"]

			# Check if the path has a valid direction and is not blocked

			def jetAhead(jet):
				return False

			if(NextPath.dir in valid_dirs):
				correct_path_dir = True
			if(not jetAhead(jet)): #Not implemented 
				clear_ahead = True

			# If path has valid direction and is clear:
			# Switch jet to that path 
			if(correct_path_dir and clear_ahead):						
				jet.path = tup[0]
				jet.loc	 = tup[1]
		
	def jetAhead(self, jet):
		return false
			
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
		jet.speed -= jet.speed - DELTA_SPEED #May not even need this really. 

	def move(self, jet):
		""" Method for moving a jet. This is done by changing which slot in a path list the jet occupies.
			This method does not switch paths, it only checks for jet collision and path ending.

			Returns true if the jet was moved, false if it wasn't moved. 
		"""		
		dD = 1	#Change in distance of the jet calculated by it's speed. Most jets will have the same speed: TAXI_SPEED
		path = PATHS[jet.path]
		
		def changeListPosition(positive, dD): 
			"""Nested function for changing the position of a jet in a list """			
			if(not positive):
				dD = dD - 2*dD

			#Check the slot imediately ahead of this jet for other jets: 
			clear_ahead = False
			if(path.p[jet.loc + dD ][1] != False):
				clear_ahead = True

			#Check that we arn't crossing an active runway:
			for i in range(1, dD + 1):
				j = i
				if(not positive):
					j = -i 
				temp = PATHS[jet.path].p[jet.loc + j][2] 
				if(temp != False):
					index = PATHS[jet.path].p[jet.loc + j][2][0] 
					if(index == 0 or 1 or 2):
						if(index == 0):
							if(not RWL_OPEN):
								return False
						
							#If the jet is taxiing to a runway it should not step onto the runway.
							elif(jet.apt == 3): 
								return False

						elif(index == 1):
							if(not RWM_OPEN):
								return False
							elif(jet.apt == 3):
								return False

						elif(index == 2):
							if(not RWR_OPEN):
								return False		
							elif(jet.apt == 3):
								return False
			
			#Check if the path ends:
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
			return changeListPosition(True, dD)

		if(path.dir == "West" or path.dir == "South"):
			return changeListPosition(False, dD)

		if(path.dir == "South-East" or path.dir == "North-East"):						
			return changeListPosition(True, dD)

		if(path.dir == "North-West" or path.dir == "South-West"):
			return changeListPosition(False, dD)


	#May not need these? vvvvvvvv 
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


	#================= Gate Methods =========================#
	def refuel(self, jet):		
		jet.fuel = FUEL_MAX
		jet.time_at_gate += TIME_TO_REFUEL

	def deboard(self, jet): 		
		jet.time_at_gate += TIME_TO_DEBOARD
	
	def service(self, jet):		
		jet.time_at_gate += TIME_TO_SERVICE					

	def board(self, jet):					#After being serviced, board passengers
		jet.time_at_gate += TIME_TO_BOARD   #This takes TIME_TO_BOARD amount of time	

class Path:
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
	def __init__(self, dir = "None", list = []):		
		self.dir = dir
		self.p = list
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