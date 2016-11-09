#coding=utf-8
from xml.dom.minidom import Document
import datetime
class GenTmx(object):
	def __init__(self):
		tmp = str(datetime.datetime.now())
		self.time = tmp[0:4] + tmp[5:7] + tmp[8:10] + "T" + tmp[11:13] + tmp[14:16] + tmp[17:19] + "Z"

	def gentmx(self,adminlang,srclang,direction=[],sentences=[],splitmark="###T###"):
		doc = Document()
		tmx = doc.createElement("tmx")
		tmx.setAttribute("version","1.4")
		doc.appendChild(tmx)
		header =doc.createElement("header")
		header.setAttribute('segtype',"sentence")
		header.setAttribute('adminlang',adminlang)
		header.setAttribute("srclang",srclang)
		header.setAttribute("datatype","rtf")
		header.setAttribute("creationdate",self.time)
		header.setAttribute("creationid","TMXMALLTOOLS")

		tmx.appendChild(header)
		body = doc.createElement('body') #创建根元素
		tmx.appendChild(body)

		for sentence in sentences:
			tu_element = doc.createElement('tu')
			tu_element.setAttribute('creationdate', self.time)
			tu_element.setAttribute("creationid", "TMXMALLTOOLS")
			line = sentence.split(splitmark)
			# print line[0] + " " +  line[1]
			if len(line)<2:
				continue
			body.appendChild(tu_element)
			tuv1 = doc.createElement('tuv')
			tuv1.setAttribute("xml:lang",direction[0])
			tu_element.appendChild(tuv1)
			tuv1_sentence_element = doc.createElement('seg')
			tuv1_sentence = doc.createTextNode(line[0].replace("\n",''))
			tuv1.appendChild(tuv1_sentence_element)
			tuv1_sentence_element.appendChild(tuv1_sentence)
			tu_element.appendChild(tuv1)

			tuv2 = doc.createElement('tuv')
			tuv2.setAttribute("xml:lang", direction[1])
			tu_element.appendChild(tuv2)
			tuv2_sentence_element = doc.createElement('seg')
			tuv2_sentence = doc.createTextNode(line[1].replace("\n",''))
			tuv2.appendChild(tuv2_sentence_element)
			tuv2_sentence_element.appendChild(tuv2_sentence)
			tu_element.appendChild(tuv2)

		return doc

def txttotmx(size,srclang,tarlang,sen,tarfile,splitmark="###T###"):
	size = int(size)
	if size < 1:
		return
	if size >= 400000:
		size = 400000
	count = len(sen)/size
	for i in range(0,count+1):
		with open(tarfile + str(i) + ".tmx","w") as f:
			fin = sen[ i*size : i*size + size]
			gen = GenTmx()
			f.write(gen.gentmx(srclang,srclang,[srclang,tarlang],fin,splitmark).toprettyxml(indent = ''))
	return