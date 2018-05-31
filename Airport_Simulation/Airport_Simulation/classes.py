
import time
import Runway as runway
import random as R
from threading import *
from sim_driver import *
#=========================== SIMULATION OBJECTS ==============================# 

# NOTE: I have commented out some Jet class variables so I can get some basic implemenation done. 
#		Will be added back in later as needed? 

class Jet:	#Base jet class
	def __init__(self, name, fuel, weight, apt, path, pathIndex):	
		self.name	= name		#AA302
		self.fuel	= fuel		#In gallons?		
		self.weight	= weight	#In pounds
		self.path	= path		#Index of the path in the PATHS list that the jet is on currently
		self.apt	= apt		#Process Status
		self.loc	= pathIndex #Index in the path that the jet is on
		self.history = []		#Stores each of the preceding variables for each time step of simulation
		#self.atc_status		#ATC Status
		#self.emg_status		#Emergency Status
		#self.heading			#In degrees (0 - 360)
		#self.speed				#Ground speed (MPH) ?
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
		self.GATES		= []		#List of all gates at the airport		

	def update_jets():
		""" Updates the state of all jets in the simulation. 
			Path switching when necessary is done in this method."""
		for jet in jets:
			
			# NOT CURRENTLY USING FIRST TWO STATUSES: Spawning jets directly 
			# onto runway using mostly uniform distribution. With the exception
			# of rushours which have a higher probability of a jet landing.
			
			#If jet is landing
			if(jet.apt == 2):
				#1. Move it down the runway to a spot where it stops and takes an open taxiway
				#	or a taxiway with room. 
				#2. Change status to TXG - 4 - Taxiing to gate
				pass

			#If jet is going to a runway:
			if(jet.apt == 3):
				#1. Move it from the terminal to the MAIN taxiway
				#2. Move it UP or DOWN the main taxiway untill it reaches the top or bottom of the airport
				#3. Move it LEFT untill it reaches the takeoff queue OR it reaches the runway				
				#4. IF TAKING OFF: Change status to TA - 6 - Taking off 
				#5. IF IN TAKEOFF QUEUE: No change to status
				pass

			#If jet is going to gate:
			if(jet.apt == 4):
				#1. Move jet RIGHT untill it reaches taxi-to-gate queue or reaches MAIN taxiway
				#2. Move jet UP or DOWN MAIN taxiway until it reaches the path for it's random assigned gate
				#3. Move jet onto gate path
				#4. Dock jet with the gate and change it's status to TG: 5 - At a gate
				pass
			
			#If jet is at a gate:
			if(jet.apt == 5):
				pass
			
			#If jet is taking off:
			if(jet.apt == 6):
				pass

			#If jet needs to be moved get moved
			#If jet needs to be path switched path switch
			#If jet needes to be gated, gate it
			#If jet needs to be 
			pass
			
	def pickGate(self):
		"""Picks an open gate at random for the jet to go to."""
		gate = GATES[R.randint(0, len(GATES))]
		while(gate.jet != False):
			index = R.randint(0, len(GATES))
			gate = GATES[index]
			
		pass

	def move_jet(jet):
		""" Method for moving a jet. This is done by changing which slot in a path list the jet occupies.
			This method does not switch paths, it only checks for jet collision and path ending
		"""
		jet = Jet("TEST 747", 1000, 398000, 0, 0, 0)
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

		#NOTE: Have to check for end of path
		# and handle path switching ? 
	
		if(path.dir == "East" or path.dir == "North"):
			changeListPosition(True)

		if(path.dir == "West" or path.dir == "South"):
			changeListPosition(False)

		if(path.dir == "South-East" or path.dir == "North-East"):						
			changeListPosition(True)

		if(path.dir == "North-West" or path.dir == "South-West"):
			changeListPosition(False)

	def landing(self, runway):
		#-if runway is locked, the jet can land in a timely fashion
		if(runway.lock.locked()):
			hold = Time(10, land, runway)
			hold.start()
			print("Jet in hold")
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


class Gate: #Base Terminal class
	def __init__(self, x,y):
		self.loc = (x,y)	#Location of terminal
		self.jet;			#Each terminal can hold a single jet
		
	def refuel(jet):
		pass


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

#

class atc_stat(Enum):	#Jet ATC Status
	AW = 0		#Awaiting instructions from ATC
	EX = 1		#Executing instructions from ATC
	IN = 2		#Inactive - not requesting clearance, not executing anything


class e_stat(Enum):	#Emergency Status
	n = 0		#Normal, no emergency
	e = 1		#Emergency 
#============================ END JET STATUSES ================================#
