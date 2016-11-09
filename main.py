#coding=utf-8
import tornado.web
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from simple_tools import logger
import datetime
import os

from tools import anltmx
from tools import gentmx
from tools import merge
from tools import test
from tools import checkport
from tools import changedirect

mylogger = logger("TmxmallTools","TmxmallTools.log").log()
# http://localhost:8888/tmxtotxt
# params:
# 	size:单个目标文件大小（1到400000条
# 	srcpath:源文件路径
#	tgtpath：目标路径
#	srclang：源语言
#	tarlang：目标语言
#	splitmark：txt文件分隔符
#   将源文件生成tmx文件存放在目标目录
# Example 将tab键分割的文本数据转存为tmx文件，txt按行存储，每行以tab键分割
# res：null
class TxtToTmx(tornado.web.RequestHandler):
	def get(self):
		try:
			size = self.get_argument("size")
			tgtpath = self.get_argument("tgtpath")
			srclang = self.get_argument("srclang")
			tarlang = self.get_argument("tarlang")
			srcpath = self.get_argument("srcpath")
			splitmark = self.get_argument("splitmark")
			# splitmark = "\t"
			gentmx.txttotmx(size,srclang,tarlang,test.readtxt(srcpath),tgtpath,splitmark)
		except EOFError, e:

			mylogger.warning("[TxtToTmx] : " + e.message)
		return
#parm：size:单个目标文件大小（1到400000条） srcpath:源文件路径 tgtpath：目标路径 splitmark：txt文件分隔符null
#将源tmx文件生成txt文件存放到目标路径
#res：
class TmxToTxt(tornado.web.RequestHandler):
	def get(self):
		try:
			size = self.get_argument("size")
			srcpath = self.get_argument("srcpath")
			tgtpath = self.get_argument("tgtpath")
			splitmark = None
			try:
				splitmark = self.get_argument("splitmark")
			except:
				pass
			if splitmark == None:
				anltmx.tmxtotxt(size,srcpath,tgtpath)
				return
			anltmx.tmxtotxt(size,srcpath,tgtpath,splitmark)
			return
		except EOFError, e:
			mylogger.warning("[TmxToTxt] : " + e.message)
		return

#parm：srcpath:源文件路径 tgtpath：目标路径
#从源文件生成一个MD5仓库到目标文件
#res：null
class GenMd5Repo(tornado.web.RequestHandler):
	def get(self):
		try:
			srcpath = self.get_argument("srcpath")
			tgtpath = self.get_argument("tgtpath")
			if srcpath.endswith(".txt"):
				test.writeMd5(test.rmInDupGetMd5(test.readtxt(srcpath), test.md5dict),tgtpath)
				return
			test.writeMd5(test.rmInDupGetMd5(anltmx.anltmx(srcpath)[0],test.md5dict),tgtpath)
			return
		except EOFError,e:
			mylogger.warning("[GenMd5Repo] : " + e.message)
		return

# parm：tmpmdrepo：临时MD5存放仓库 localmd5repo：本地md5仓库
# 讲临时仓库与本地仓库的MD5合并并存放在本地MD5仓库
# res：
class MergeMd5(tornado.web.RequestHandler):
	def get(self):
		try:
			tmpmd5repo = self.get_argument("tmpmd5repo")
			localmd5repo = self.get_argument("localmd5repo")
			merge.mergemd5(tmpmd5repo,localmd5repo)
		except EOFError, e:
			mylogger.warning("[MergeMd5] : " + e.message)
		return

#parm：filename：目标文件 filetype：生成文件类型（tmx/txt） size：单个文件句对数 localmd5repo：本地MD5仓库 tmpmd5repo：临时MD5存放仓库 tgtpath：去重文件存放路径
#parm：duppath：重复文件存放处   当文件为txt时需要  （splitmark：txt文件分隔符)   当文件为txt并生成文件为tmx时需要 srclang：txt文件源语言方向 tarlang：txt文件目标语言方向）
#将目标文件内与本地仓库重复部分剔除后存放在tgtpath 重复部分存放在duppath 并生成MD5值存放在临时MD5仓库 供以后操作
#resnull
class FileReOutDup(tornado.web.RequestHandler):
	def get(self):
		try:
			filetype = self.get_argument("filetype")
			filename = self.get_argument("filename")
			tgtpath = self.get_argument("tgtpath")
			duppath = self.get_argument("duppath")
			size = self.get_argument("size")
			localmd5repo = self.get_argument("localmd5repo")
			tmpmd5repo = self.get_argument("tmpmd5repo")
			sentencelist = None
			srclang = ""
			tarlang = ""
			splitmark = ""
			if filename.endswith(".txt"):
				sentencelist = test.readtxt(filename)
				splitmark = self.get_argument("splitmark")
			else:
				anlresult = anltmx.anltmx(filename)
				sentencelist = anlresult[0]
				srclang = anlresult[1][0]
				tarlang = anlresult[1][1]
				splitmark = "###T###"
			tmpmd5 = test.rmInDupGetMd5(sentencelist,test.md5dictsplitmark,)
			dupmd5 = test.reOutDupMd5(tmpmd5,localmd5repo)
			dupmd5path = tmpmd5repo + "\dupmd5"
			if os.path.exists(dupmd5path):
				os.makedirs(dupmd5path)
			tgtmd5path = tmpmd5repo + "\tgtmd5"
			if os.path.exists(tgtmd5path):
				os.makedirs(tgtmd5path)
			test.writeMd5(list(set(tmpmd5)-set(dupmd5)), tgtmd5path)
			test.writeMd5(dupmd5,dupmd5path)
			result = test.redup(sentencelist,dupmd5,splitmark)
			if filetype == "txt":
				test.writetxt(result[0],tgtpath,size)
				test.writetxt(result[1],duppath,size)
				return
			if srclang == "" or tarlang == "" :
				srclang = self.get_argument("srclang")
				tarlang = self.get_argument("tarlang")

			gentmx.txttotmx(size, srclang, tarlang, result[0], tgtpath, splitmark)
			gentmx.txttotmx(size, srclang, tarlang, result[1], duppath, splitmark)
			return


		except EOFError,e:
			mylogger.warning("[FileReOutDup] : " + e.message)
		return

class Test(tornado.web.RequestHandler):
	def get(self):
		self.write(test.hello)
		return

class Quit(tornado.web.RequestHandler):
	def get(self):
		mylogger.info("[process stop :] " + str(datetime.datetime.now()))
		IOLoop.current().stop()
		IOLoop.current().close()
		return
# parm:
#		filename:需要方向互换的文件
#		filetype：文件类型（tmx：1，txt：0）
#		splitmark：分隔符（仅txt文件需要）
# res：null
class FileRedirect(tornado.web.RequestHandler):
	def get(self):
		filename = self.get_argument("filename")
		filetype = int(self.get_argument("filetype"))
		if filetype == 1:
			changedirect.changeDirect(filename,filetype)
			return
		splitmark = self.get_argument("splitmark")
		changedirect.changeDirect(filename,filetype,splitmark)
		return
app = tornado.web.Application({
	(r"/tmxtotxt",TmxToTxt),
	(r"/txttotmx",TxtToTmx),
	(r"/mergemd5",MergeMd5),
	(r"/genmd5repo",GenMd5Repo),
	(r"/filereoutdup",FileReOutDup),
	(r"/fileredirect",FileRedirect),
	(r"/",Test),
	(r"/quit",Quit)
})

def run(server,port):
	server.listen(port)
	with open("port.txt",'w') as f:
		print port
		f.write(str(port))
	IOLoop.current().start()
	return

if __name__ == '__main__':
	server = HTTPServer(app)
	for port in range(12121,21212,30):
		if checkport.IsOpen("127.0.0.1",port):
			run(server,port)
			break