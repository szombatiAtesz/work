import RPi.GPIO as GPIO
import time, sys

#pinNumber13, constant = 0.0019157088
def get_senzor_data_every_60_sec(pinNumber,constant):

	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(input,GPIO.IN)
	rate_cnt = 0
	resoult = []
	while GPIO.input(pinNumber) != 0:
		time_begin = time.time()
		gpio_cur = GPIO.input(input)
		rate_cnt += 1
		try:
			None
		except KeyboardInterrupt:
			GPIO.cleanup()
			sys.exit()
	time_end = time.time
	time_diff = time_end - time_begin
	liters_per_time = round(rate_cnt *constant,4)
	liters_per_min = 60 // time_diff * liters_per_time 
	resoult.append(liters_per_min)
	return resoult






