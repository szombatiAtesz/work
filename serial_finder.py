import sys
import glob
import serial
import time


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
		print(portok)
		try:
			device = 'ttyUSB'
			str_serial = str(serial.Serial(portok,rtscts=True,dsrdtr=True))
			if serial.Serial(portok,rtscts=True,dsrdtr=True).isOpen() == True and str_serial.find(device) > 0:
				resoult.append(portok)
				serial.Serial(portok,rtscts=True,dsrdtr=True).close()
		except (OSError, serial.SerialException):
			continue
	print(resoult)
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
		try:
			ser = serial.Serial(portok,baudrate=115200,rtscts=True,dsrdtr=True)
			ser.write(("AT\r").encode())


if __name__ == '__main__':
	portok = serial_ports()
	at_ports = find_ports_for_AT(portok)
	print(at_ports)
	AT_PORT = select_port_for_use(at_ports)
	print(AT_PORT)
