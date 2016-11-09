#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


filenames = ["0",'1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
def mergemd5(newrepo,localrepo):
	for filename in filenames:
		newmd5 = []
		oldmd5 = []
		with open(newrepo + "/" + filename + '.txt','r') as inf:
			newmd5 = inf.readlines()
		with open(localrepo + "/" +  filename + '.txt', 'r') as inf:
			oldmd5 = inf.readlines() + newmd5
		md5 = list(set(oldmd5))
		with open(localrepo + "/" + filename + '.txt', 'w') as outf:
			outf.writelines(md5)
