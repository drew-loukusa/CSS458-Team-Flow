

#==================================== NOTE ========================================#

	# Biggest thing we have to figure out is how big is each grid cell going to be.
	# We need to overlay a grid onto our image so we can start assigning coords to 
	# the terminals. 

	#Will do this tommorrow: 5/21/18
#==================================== NOTE ========================================#

import turtle as T
import time 

def main():
	turt = T.Turtle()
	screen = T.Screen()
	screen.setup(800, 1000)
	screen.bgpic("airport.png")

	move_speed = 10
	turn_speed = 10

	# these defs control the movement of our "turtle"
	def forward():
	  T.forward(move_speed)

	def backward():
	  T.backward(move_speed)

	def left():
	  T.left(turn_speed)

	def right():
	  T.right(turn_speed)

	turt.fd(10)

	time.sleep(30)
	T.speed(0)
	T.home()

	# now associate the defs from above with certain keyboard events
	screen.onkey(forward, "Up")
	screen.onkey(backward, "Down")
	screen.onkey(left, "Left")
	screen.onkey(right, "Right")

	screen.listen()

main()