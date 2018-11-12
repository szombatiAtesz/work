import RPi.GPIO as GPIO
import time, sys

#pinNumber13, constant = 0.0019157088
def get_sensor_data():
	GPIO.setmode(GPIO.BOARD)
	inpt = 13
	GPIO.setup(inpt,GPIO.IN)
	rate_cnt = 0
	tot_cnt = 0
	minutes = 0
	constant = 0.0019157088
	time_new = 0
	while True:
		time_new = time.time() + 5
		rate_cnt = 0
		while time.time() <= time_new:
			if GPIO.input(inpt) != 0:
				rate_cnt += 1
			try:
				None
#				print(GPIO.input(inpt), end=" ")
			except KeyboardInterrupt:
				GPIO.cleanup()
		minutes += 1
		liter_per_min = round(rate_cnt * constant,4)
		yield liter_per_min

valami = get_sensor_data()


