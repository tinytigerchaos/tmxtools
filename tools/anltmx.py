#coding=utf-8
import xml.sax
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
senlist = []


class TuHandler(xml.sax.ContentHandler):
    def __init__(self):
		self.CurrentData = ""
		self.lang = ""
		self.headlang = ""
		self.sentence = {}

    def startElement(self, tag, attrs):
		self.CurrentData = tag
		if tag == "tu":
			if self.sentence != {}:
				senlist.append(str(self.sentence["zh-CN"]) + "###T###" + str(self.sentence['es-ES']) + "\n")
		if tag == "tuv":
			# self.headlang = self.lang
			self.lang = attrs['xml:lang']

    def endElement(self, tag):
		self.CurrentData = ""

    def characters(self, content):
        if self.CurrentData == "seg":
			self.sentence[self.lang] = content

def anltmx(filename):
	parser = xml.sax.make_parser()
	parser.setFeature(xml.sax.handler.feature_namespaces, 0)
	Handler = TuHandler()
	parser.setContentHandler(Handler)
	parser.parse(filename)
	return senlist
