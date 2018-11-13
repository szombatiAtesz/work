
def read_data():
	with open('tmp.csv','r') as f:
		lastline = ""
		for line in f:
			lastline = line
		print(lastline)

read_data()
