with open('tmp.csv','r') as f:
	last_line = f.readlines()[-1]
	print(last_line)
