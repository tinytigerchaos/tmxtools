#coding=utf-8
import anltmx
from lxml import etree
import hashlib
import os
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

def getMd5(sentence):
	md5 = hashlib.md5()
	md5.update(sentence)
	return md5.hexdigest()

def rmInDupGetMd5(allsentences,md5dict):
	indup = []
	try:
		for sentence in allsentences:
			line1 = sentence.split("###T###")[0]
			line2 = sentence.split("###T###")[1]
			line1 = line1.strip()
			line2 = line2.strip()
			for i in line1,line2:
				md5 = getMd5(i)
				fist = md5[0]
				md5dict[fist].append(md5 + "\n")
		return md5dict
	except:
		pass


def writeMd5(md5dict):
	for key in md5dict.keys():
		with open("../tmpmd5/" + key + '.txt','w') as wt:
			fin = list(set(md5dict[key]))
			wt.writelines(fin)

def reOutDupMd5(md5dict):
	for key in md5dict.keys():

		totalmd5 = None
		dupmd5 = []
		with open("../allMd5/" + key ,'r') as rd:
			totalmd5 =  set(rd.readlines())
		dupmd5 = list(set(md5dict[key]) & totalmd5)
		md5dict[key] = dupmd5

	return md5dict
		# with open("../tmpmd5/" + key + ".txt",'w') as wt:
		# 	wt.writelines(dupmd5)

md5dict = {"0":[],
		   "1":[],
		   "2":[],
		   "3":[],
		   "4":[],
		   "5":[],
		   "6":[],
		   "7":[],
		   "8":[],
		   "9":[],
		   "a":[],
		   "b":[],
		   "c":[],
		   "d":[],
		   "e":[],
		   "f":[]
		   }

if __name__ == '__main__':
	allsentences = []
	dir = []
	for p,c,filenames in os.walk("../soufile"):
		for filename in filenames:
			if filename.endswith(".tmx"):
				dir.append(os.path.join(p,filename))
	for filename in dir:
		print "doing : " + filename
		allsentences += anltmx.anltmx(filename)
	allsentences = list(set(allsentences))
	rmInDupGetMd5(allsentences,md5dict)
	writeMd5(md5dict)
	reOutDupMd5(md5dict)

	for filename in dir:
		art = anltmx.anltmx(filename)
		dup = []
		tar = []
		for sentence in art:
			line1 = sentence.split("###T###")[0]
			line2 = sentence.split("###T###")[1]
			line1 = line1.strip()
			line2 = line2.strip()
			md5 = getMd5(line1) + "\n"
			if md5 in md5dict[md5[0]]:
				dup.append(sentence)
				continue
			md5 = getMd5(line2)
			if md5 in md5dict[md5[0]]:
				dup.append(sentence)
				continue

			tar.append(sentence)

		with open(filename.replace("soufile","tarfile").replace(".tmx",".txt"),'w') as wt:
			wt.writelines(list(set(tar)))

		with open(filename.replace("soufile","dupfile").replace(".tmx",".txt"),'w') as wt:
			wt.writelines(dup)
