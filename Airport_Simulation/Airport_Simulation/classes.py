
import time
import Runway as runway
from threading import *
from sim_driver import *
#=========================== SIMULATION OBJECTS ==============================# 

# NOTE: I have commented out some Jet class variables so I can get some basic implemenation done. 
#		Will be added back in later as needed? 

class Jet:	#Base jet class
	def __init__(self, name, fuel, weight, apt_status, path, pathIndex):	
		self.name	= name		#AA302
		self.fuel	= fuel		#In gallons?		
		self.weight	= weight	#In pounds
		self.path = path		#Index of the path in the PATHS list that the jet is on currently
		#self.emg_status			#Emergency Status
		self.apt_status	 = apt_status  #Process Status
		#self.atc_status			#ATC Status
		self.location	= pathIndex #Index in the path that the jet is on
		#self.heading			#In degrees (0 - 360)
		#self.speed				#Ground speed (MPH) ?
		#self.altitude			#In Feet
		#self.burn_rate			#Gallons per hour? 
		#self.history = []		#Stores each of the preceding variables for each time step of simulation
		
class P_Jet(Jet): #Passenger jet
	def __init__(self, name, fuel, weight, x, y):
		self.passengers		#Number of passengers. Avg weight will be 150 Lb per passenger
		self.ploy = TIME_TO_BOARD


class C_Jet(Jet): #Cargo jet 
	def __init__(self, name, fuel, weight, x, y):
		super(C_Jet, self).__init__(name, fuel, weight, x,y)		
		self.cargo			#In pounds


class ATC:					#Air Traffic Control: Serves as main logic controller of simulation
	def __init__(self):		
		#We don't NEED a seperate list for each Airport process status but I'm leaving them here for now:
		#It might make it easier later to do it this way.
		self.jets = []			#List of all jets in simulation
		self.jets_air  = []
		self.jets_hold = []		#This should be treated as a queue: FIFO
		self.jets_land = []		
		self.jets_taxi = []		
		self.jets_term = []
		self.jets_take = []
		self.gates = []			#List of all gates at the airport		

	def update_jets():
		for jet in jets:
			#if( not emergmency):
			move(jet)

	def move(jet):
		jet = Jet("TEST 747", 1000, 398000, 0, 0, 0)
		#path = PATHS[jet.path]		

		#NOTE: Have to check for end of path
			  # and handle path switching ? 

		path = Path("T1", "East", [[(0,1), False], [(0,2), False]])
		if(path.dir == "East" or path.dir == "North"):						
			path.p[jet.loc][1] = False
			path.p[jet.loc + 1 ][1] = jet
			jet.loc += 1
		if(path.dir == "West" or path.dir == "South"):
			path.p[jet.loc][1] = False
			path.p[jet.loc - 1 ][1] = jet		
			jet.loc -= 1

		#Need 4 more cases for each diagonal direction: MAYBE NOT?

			


	def landing(self, runway):
		#-if runway is locked, the jet can land in a timely fashion. 
		if runway.lock.loced():
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
		if runway.lock.locked():
			pass
		else:
			pass
		#- it will be listed as the first jet on the runway

class Path:
	def __init__(self, label, dir = "None", list = []):
		self.label = label
		self.dir = dir
		self.p = list

class Gate: #Base Terminal class
	def __init__(self, x,y):
		self.loc = (x,y)	#Location of terminal
		self.jet;			#Each terminal can hold a single jet		
		self.has_jet;		#Bool for if terminal is occupied or not

	def refuel(jet):
		pass


class P_Gate(Gate): #Passenger Terminal
	def __init__(self):
		pass

	def deboard_passengers(self, jet): 
		pass

	def service(self, jet):		#After deboarding, the jet must be made ready for the next trip
		pass				#This process takes TIME_TO_SERVICE amount of time

	def board_passengers(self, jet):	#After being serviced, board passengers
		pass					#This takes TIME_TO_BOARD amount of time
	
	
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
	TX = 3		#Taxiing			
	TE = 4		#At a terminal
	TA = 5		#Taking off
	

class atc_stat(Enum):	#Jet ATC Status
	AW = 0		#Awaiting instructions from ATC
	EX = 1		#Executing instructions from ATC
	IN = 2		#Inactive - not requesting clearance, not executing anything


class e_stat(Enum):	#Emergency Status
	n = 0		#Normal, no emergency
	e = 1		#Emergency 
#============================ END JET STATUSES ================================#
