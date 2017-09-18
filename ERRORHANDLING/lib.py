def spl(asx):
	try:
		a,b,c=asx.split(" ")
		return 1
	except ValueError:
		return 0

def fungsi(jenis,x,y):
	try:
		if(jenis=='MUL'):
			return int(x)*int(y)
		elif(jenis=='ADD'):
			return int(x)+int(y)
		elif(jenis=='SUB'):
			return int(x)-int(y)
		else:
			return 'ERR'
	except ValueError:
		return 'ERROR'
