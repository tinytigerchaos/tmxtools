#coding=utf-8
import anltmx
import hashlib
import os
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

hello = "hello"

def getMd5(sentence):
	md5 = hashlib.md5()
	md5.update(sentence)
	return md5.hexdigest()

def rmInDupGetMd5(allsentences,md5dict,splitmark="###T###"):
	indup = []
	try:
		for sentence in allsentences:
			line1 = sentence.split(splitmark)[0]
			line2 = sentence.split(splitmark)[1]
			line1 = line1.strip()
			line2 = line2.strip()
			for i in line1,line2:
				md5 = getMd5(i)
				fist = md5[0]
				md5dict[fist].append(md5 + "\n")
		return md5dict
	except:
		pass


def writeMd5(md5dict,tarfile):
	for key in md5dict.keys():
		with open(  tarfile + "/" + key + '.txt','a') as wt:
			fin = list(set(md5dict[key]))
			wt.writelines(fin)

def reOutDupMd5(md5dict,md5repo):
	for key in md5dict.keys():

		totalmd5 = None
		dupmd5 = []
		with open( md5repo + "/" + key + ".txt" ,'r') as rd:
			totalmd5 =  set(rd.readlines())
		dupmd5 = list(set(md5dict[key]) & totalmd5)
		md5dict[key] = dupmd5

	return md5dict

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

def readtxt(filename):
	with open(filename,'r') as f:
		return f.readlines()


def redup(sentencelist,md5dict,splitmark="###T###"):
	dup = []
	tar = []
	for sentence in sentencelist:
		line1 = sentence.split(splitmark)[0]
		line2 = sentence.split(splitmark)[1]
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
	return [list(set(tar)),dup]


def writetxt(sentencelist,tarfile,size):
	size = int(size)
	if size < 1:
		size = 1
	if size > 400000:
		size = 400000
	count = len(sentencelist)/size
	for i in range(0,count+1):
		with open(tarfile + str(count) + ".txt") as f:
			f.writelines(sentencelist[count*size:count*size+size])
