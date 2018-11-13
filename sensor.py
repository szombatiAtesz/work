import RPi.GPIO as GPIO
import time

f = open('tmp.csv','a')
GPIO.setmode(GPIO.BOARD)
inpt = 13
GPIO.setup(inpt,GPIO.IN)
minutes = 0
constant = 0.1006
time_new = 0.0
global rate_cnt, tot_cnt
rate_cnt = 0
tot_cnt = 0

def Pulse_cnt(inpt_pin):
	global rate_cnt, tot_cnt
	rate_cnt += 1
	tot_cnt += 1

GPIO.add_event_detect(inpt,GPIO.FALLING,callback=Pulse_cnt,bouncetime=10)
rpt_int = 5
print('Reports every ', rpt_int, ' seconds')
print('Control C to exit')

def sensor():
	while True:
		time_new = time.time() + rpt_int
		rate_cnt = 0
		while time.time() <= time_new:
			try:
				None
				print(GPIO.input(inpt), end='')
			except KeyboardInterrupt:
				print('\nCTRL C - Exiting nicely')
				GPIO.cleanup()
		liter_per_min = round(rate_cnt * constant,2)
		total_liter = round(tot_cnt * constant,1)
		print(liter_per_min)
		print(total_liter)
		f.write(str(liter_per_min) + ' ')
		f.write(str(total_liter) + '\n')
		f.flush()
sensor()
