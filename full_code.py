import sys
import glob
import serial
import time
import RPi.GPIO as GPIO

#pinNumber13, constant = 0.0019157088
def get_senzor_data_every_60_min(pinNumber,constant):

	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(input,GPIO.IN)
	rate_cnt = 0
	time_begin = time.time()
	while GPIO.input(pinNumber) == 0 or GPIO.input(pinNumber) == 1:
		time_now = time.time()
		time_total = time.time()
		if GPIO.input(pinNumber) == 1:
			rate_cnt += 1
		if time_total - time_begin == 10:
			total_liter = round(rate_cnt * constant,4)
		if time_now - time_begin == 60:
			liters_per_min = round(rate_cnt * constant,4)
		try:
			None
		except KeyboardInterrupt:
			GPIO.cleanup()
			sys.exit()
	return total_liter,liters_per_min


def serial_ports():
	if sys.platform.startswith('win'):
		ports = ['COM%s' % (i + 1) for i in range(256)]
	elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
	# this excludes your current terminal "/dev/tty"
		ports = glob.glob('/dev/tty[A-Za-z]*')
	elif sys.platform.startswith('darwin'):
		ports = glob.glob('/dev/tty.*')
	else:
		raise EnvironmentError('Unsupported platform')
	resoult = []
	for portok in ports:
		try:
			device = 'ttyUSB'
			str_serial = str(serial.Serial(portok,rtscts=True,dsrdtr=True))
			if serial.Serial(portok,rtscts=True,dsrdtr=True).isOpen() == True and str_serial.find(device) > 0:
				resoult.append(portok)
				serial.Serial(portok,rtscts=True,dsrdtr=True).close()
		except (OSError, serial.SerialException):
			continue
	return resoult

def find_ports_for_AT(portlist):
	msg1 = "AT\r"
	msg2 = "AT+CFUN?\r"
	ok = "OK"
	AT_port = []
	for i in portlist:
		ser = serial.Serial(i,baudrate=115200,timeout=1,xonxoff=True,rtscts=True,dsrdtr=True)
		ser.write(msg1.encode())
		ser.write(msg2.encode())
		if str(ser.read(64)).find(ok) > 0:
			AT_port.append(i)
	return AT_port

def select_port_for_use(ATports):
	max = 0
	for i in ATports:
		number = (i[len(i)-1])
		if number > max:
			max = number
	for j in ATports:
		j = str(j)
		if j.find(max) > 0:
			return j

def attach_to_network(port):
	if serial.Serial(port,rtscts=True,dsrdtr=True).isOpen() == True:
		out = []
		try:
			ser = serial.Serial(port,baudrate=115200,rtscts=True,dsrdtr=True)
			ser.write(('AT+QCFG="nbsibscramble",0\r').encode())
			time.sleep(1)
			while ser.inWaiting() > 0:
				out.append(ser.read(ser.inWaiting()))
			ser.write(('AT+CPSMS=0,,,"00000100","00001111"\r').encode())
			time.sleep(1)
			while ser.inWaiting() > 0:
				out.append(ser.read(ser.inWaiting()))
			ser.write(('AT+QCFG="band",0,80000,80000,1\r').encode())
			time.sleep(1)
			while ser.inWaiting() > 0:
                                out.append(ser.read(ser.inWaiting()))
			ser.write(('AT+QCFG="nwscanmode",1\r').encode())
			time.sleep(1)
			while ser.inWaiting() > 0:
                                out.append(ser.read(ser.inWaiting()))
			ser.write(('AT+QCFG="nwscanseq",020301\r').encode())
			time.sleep(1)
			while ser.inWaiting() > 0:
                                out.append(ser.read(ser.inWaiting()))
			ser.write(('AT+QCFG="iotopmode",1\r').encode())
			time.sleep(1)
			while ser.inWaiting() > 0:
                                out.append(ser.read(ser.inWaiting()))
			ser.write(('AT+QCFG="servicedomain",1,0\r').encode())
			time.sleep(1)
			while ser.inWaiting() > 0:
                                out.append(ser.read(ser.inWaiting()))
			ser.write(('AT+CGDCONT=1,"IP","internet.telekom"\r').encode())
			time.sleep(1)
			while ser.inWaiting() > 0:
                                out.append(ser.read(ser.inWaiting()))
			ser.write(('AT+COPS=1,2,"21630",8\r').encode())
			time.sleep(1)
			while ser.inWaiting() > 0:
                                out.append(ser.read(ser.inWaiting()))
			ser.write(('AT+CGPADDR=1\r').encode())
			time.sleep(1)
			while ser.inWaiting() > 0:
				out.append(ser.read(ser.inWaiting()))
			if ser.inWaiting() == 0:
				return out
		except KeyboardInterrupt:
			sys.exit()

def send_data_tcp():
	data = craete_data_for_ubidots()
	if serial.Serial(port,rtscts=True,dsrdtr=True).isOpen() == True:
		out = []
		error = "ERROR"
		try:
			ser.write(('AT+QIACT=1\r').encode())
                        time.sleep(2)
			while ser.inWaiting > 0:
				out.append(ser.read(ser.inWaiting()))
			ser.write(('AT+QICLOSE=0\r').encode())
			time.sleep(2)
			while ser.inWaiting > 0:
                                out.append(ser.read(ser.inWaiting()))
			ser.write(('AT+QIOPEN=1,0,"TCP","50.23.124.66",9012\r').encode())
			time.sleep(2)
			while ser.inWaiting > 0:
                                out.append(ser.read(ser.inWaiting()))
			ser.write(('AT+QISENDEX=0,' + '"' + data + '"' + '\r').encode())
			time.sleep(2)
			while ser.inWaiting > 0:
                                out.append(ser.read(ser.inWaiting()))
			ser.write(('AT+QIRD=0\r').encode())
			time.sleep(2)
			while ser.inWaiting > 0:
                                out.append(ser.read(ser.inWaiting()))
		except:
			None
		if error in out[3]:
			return True
		else:
			return False

def craete_data_for_ubidots():
	data1, data2 = get_senzor_data_every_60_min(13,0.0019157088)
	token = "BBFF-aStyrZ84Id5yovR5YpYs5kQo0UKfq5"
	port = 9012
	domain_name = "translate.ubidots.com"
	tmp = "microchip/1.0|POST|" + str(token) + "|bg96=>catm:" + str(data1) + ",humidity:" + str(data2) + "|end"
	to_hex = tmp.encode("utf-8").hex()
	return to_hex

if __name__ == '__main__':
	portok = serial_ports()
	at_ports = find_ports_for_AT(portok)
	print(at_ports)
	AT_PORT = select_port_for_use(at_ports)
	print(AT_PORT)
	network = attach_to_network(AT_PORT)
	print(network)
	if send_data_tcp():
		print("jee")
