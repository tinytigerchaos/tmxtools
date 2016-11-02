import tornado.web
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tools import gentmx
from tools import anltmx
from tools import merge
from tools import test

class TxtToTmx(tornado.web.RequestHandler):
	def get(self):
		try:
			size = self.get_argument("size")
			tarpath = self.get_argument("tarpath")
			srclang = self.get_argument("srclang")
			tarlang = self.get_argument("tarlang")
			sourcepath = self.get_argument("sourcepath")
			splitmark = self.get_argument("splitmark")
			print splitmark
			gentmx.txttotmx(size,srclang,tarlang,sourcepath,tarpath,splitmark)
		except EOFError, e:
			print e.message

class TmxToTxt(tornado.web.RequestHandler):
	def get(self):
		try:
			size = self.get_argument("size")
			sourcepath = self.get_argument("sourcepath")
			tarpath = self.get_argument("tarpath")
			splitmark = None
			try:
				splitmark = self.get_argument("splitmark")
			except:
				pass
			if splitmark == None:
				anltmx.tmxtotxt(size,sourcepath,tarpath)
				return
			anltmx.tmxtotxt(size,sourcepath,tarpath,splitmark)
			return
		except EOFError, e:
			print e.message
			return

class GenMd5Repo(tornado.web.RequestHandler):
	def get(self):
		try:
			sourcepath = self.get_argument("sourcepath")
			tarpath = self.get_argument("tarpath")
			if sourcepath.endswith(".txt"):
				test.writeMd5(test.rmInDupGetMd5(test.readtxt(sourcepath), test.md5dict),tarpath)
				self.write("it`s a txt file")
				return
			test.writeMd5(test.rmInDupGetMd5(anltmx.anltmx(sourcepath),test.md5dict),tarpath)
			self.write("it`s a tmx file")
			return
		except EOFError,e:
			print e.message

class MergeMd5(tornado.web.RequestHandler):
	def get(self):
		try:
			tmpmd5repo = self.get_argument("tmpmd5repo")
			localmd5repo = self.get_argument("localmd5repo")
			merge.mergemd5(tmpmd5repo,localmd5repo)
		except EOFError, e:
			print e.message



class FileReOutDup(tornado.web.RequestHandler):
	def get(self):
		try:
			filetype = self.get_argument("filetype")
			filename = self.get_argument("filename")
			tarpath = self.get_argument("tarpath")
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
			test.writeMd5(tmpmd5,tmpmd5repo)
			dupmd5 = test.reOutDupMd5(tmpmd5,localmd5repo)
			result = test.redup(sentencelist,dupmd5,splitmark)
			if filetype == "txt":
				test.writetxt(result[0],tarpath,size)
				test.writetxt(result[1],tarpath,size)
				return
			if srclang == "" or tarlang == "" :
				srclang = self.get_argument("srclang")
				tarlang = self.get_argument("tarlang")

			gentmx.txttotmx(size, srclang, tarlang, result[0], tarpath, splitmark)
			gentmx.txttotmx(size, srclang, tarlang, result[1], tarpath, splitmark)
			return


		except EOFError,e:
			print e.message

app = tornado.web.Application({
	(r"/tmxtotxt",TmxToTxt),
	(r"/txttotmx",TxtToTmx),
	(r"/mergemd5",MergeMd5),
	(r"/genmd5repo",GenMd5Repo),
	(r"/filereoutdup",FileReOutDup)

})

if __name__ == '__main__':
	server = HTTPServer(app)
	server.listen(8888)
	IOLoop.current().start()