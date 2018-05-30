#This is the Runway class

#Take off and landing process takes 5-15min, based on the real-time ground traffic
from classes import *
import threading
import time
import datetime

class Runway(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
		self.lock = threading.Lock()

	def clearRunway(self):
		self.lock.release()
		print("Runway cleared\n")
		self.timestamp()
		
	def taking_Off(self, ATC):
		self.lock.acquire()
		time.sleep(10)
		print("Plane %s has taken off\n" %jet.name)
		self.timestamp()
		self.clearRunway()

	def landing(self, ATC):
		self.lock.acquire()
		time.sleep(5)
		print("Jet %s has landed\n" %jet.name)
		self.timestamp()
		self.clearRunway()
		
	def timestamp(self):
		print(datetime.datetime.fromtimestamp(time.time()).strftime(''))


