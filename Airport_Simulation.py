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
#========================== END GLOBAL CONSTANTS =============================#

#=========================== SIMULATION OBJECTS ==============================#
class Jet:
	def __init__(self):
		self.fuel;			#In gallons?		
		self.weight;		#In pounds
		self.emg_status;	#Emergency Status
		self.apt_status;	#Process Status
		self.atc_status;	#ATC Status
		self.location;		#Tuple (x,y)
		self.heading;		#In degrees (0 - 360)
		self.speed;			#Ground speed (MPH) ?
		self.altitude;		#In Feet
		self.burn_rate;		#Gallons per hour?
		self.history = []	#Stores each of the preceding variables for each time step of simulation

class P_Jet(Jet):			#Passenger jet
	def __init__(self):
		self.passengers;	#Number of passengers. Avg weight will be 150 Lb per passenger
		self.ploy = TIME_TO_BOARD

class C_Jet(Jet):			#Cargo jet 
	def __init__(self):
		self.cargo;			#In pounds

class ATC:					#Air Traffic Control: Serves as main logic controller of simulation
	def __init__(self):
		self.jets = []		#List of all jets in simulation
		self.terminals = []	#List of all terminals at the airport

class Terminal:
	def __init__(self):
		self.jet;		#Each terminal can hold a single jet		

	def deboard_passengers(self): 
		pass

	def service(self):		#After deboarding, the jet must be made ready for the next trip
		pass				#This process takes TIME_TO_SERVICE amount of time

	def board_passengers(self):	#After being serviced, board passengers
		pass					#This takes TIME_TO_BOARD amount of time
	
	def refuel(jet):
		pass
#=========================== SIMULATION OBJECTS ==============================#

#============================== JET STATUSES =================================#
from enum import Enum
class apt_stat(Enum):	#Airport Process Status
	A = 0		#In the air
	L = 1		#Landing
	TX = 2		#Taxiing		
	G = 3		#On the ground
	TE = 4		#At a terminal
	TA = 5		#Taking off

class atc_stat(Enum):	#Jet ATC Status
	AW = 0		#Awaiting instructions from ATC
	EX = 1		#Executing instructions from ATC
	IN = 2		#Inactive - not requesting clearance, not executing anything


class e_stat(Enum):
	n = 0	#Normal, no emergency
	e = 1	#Emergency 
#============================ END JET STATUSES ================================#