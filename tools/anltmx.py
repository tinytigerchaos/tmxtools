#coding=utf-8
import xml.sax
import sys
from xml.sax import SAXParseException

reload(sys)
sys.setdefaultencoding( "utf-8" )
senlist = []
direction = []

class TuHandler(xml.sax.ContentHandler):
    def __init__(self,splitmark):
		self.CurrentData = ""
		self.lang = ""
		self.headlang = ""
		self.sentence = {}
		self.splitmark = splitmark
		self.dirt = []

    def startElement(self, tag, attrs):
		self.CurrentData = tag
		if tag == "tu":
			if self.sentence != {}:
				if self.dirt == []:
					self.dirt = [self.headlang,self.lang]
					direction = self.dirt
				senlist.append(str(self.sentence[self.headlang]) + self.splitmark + str(self.sentence[self.lang]) + "\n")
		if tag == "tuv":
			self.headlang = self.lang
			self.lang = attrs['xml:lang']

    def endElement(self, tag):
		self.CurrentData = ""

    def characters(self, content):
        if self.CurrentData == "seg":
			self.sentence[self.lang] = content


def anltmx(sourcefile):
	parser = xml.sax.make_parser()
	parser.setFeature(xml.sax.handler.feature_namespaces, 0)
	Handler = TuHandler("###T###")
	parser.setContentHandler(Handler)
	parser.parse(sourcefile)
	return [senlist,direction]


def tmxtotxt(size, sourcefile, tarfile,splitmark="###T###"):
	parser = xml.sax.make_parser()
	parser.setFeature(xml.sax.handler.feature_namespaces, 0)
	Handler = TuHandler(splitmark)
	parser.setContentHandler(Handler)
	parser.parse(sourcefile)
	size = int(size)
	if size<1:
		size = 1
	if size>400000:
		size = 400000
	count = len(senlist)/size
	for i in range(0,count + 1):
		with open(tarfile + str(i) + ".txt",'w') as f:
			f.writelines(senlist[count*size:count*size + size])

