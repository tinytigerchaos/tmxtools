from tools import anltmx
from tools import gentmx
from tools import test
def changeDirect(filename,filetype,splitmark="###T###"):
	tgtname = filename.split(".")[0] + "_redirect"
	if filetype == 1:
		res = anltmx.anltmx(filename,1)
		gentmx.txttotmx(400000,res[1][1],res[1][0],res[0],tgtname)
		return
	res = test.readtxt(filename)
	fin = []
	for sentence in res:
		tmp = ""
		line = sentence.split(splitmark)
		tmp = line[1].replace("\n",'') + splitmark + line[0] + "\n"
		fin.append(tmp)
	print len(fin)
	test.writetxt(fin,tgtname,400000)
