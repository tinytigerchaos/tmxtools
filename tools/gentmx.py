#coding=utf-8
from xml.dom.minidom import Document
import datetime
class GenTmx(object):
	def __init__(self):
		tmp = str(datetime.datetime.now())
		self.time = tmp[0:4] + tmp[5:7] + tmp[8:10] + "T" + tmp[11:13] + tmp[14:16] + tmp[17:19] + "Z"

	def gentmx(self,adminlang,srclang,direction=[],sentences=[]):
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
		header.setAttribute("creationid","TM STUDIO")
		tmx.appendChild(header)



		body = doc.createElement('body') #创建根元素
		tmx.appendChild(body)



		for sentence in sentences:
			tu_element = doc.createElement('tu')
			tu_element.setAttribute('creationdate', self.time)
			tu_element.setAttribute("creationid", "TM STUDIO")
			line = sentence.split("###T###")
			body.appendChild(tu_element)

			tuv1 = doc.createElement('tuv')
			tuv1.setAttribute("xml:lang",direction[0])
			tu_element.appendChild(tuv1)
			tuv1_sentence_element = doc.createElement('seg')
			tuv1_sentence = doc.createTextNode(line[0])
			tuv1.appendChild(tuv1_sentence_element)
			tuv1_sentence_element.appendChild(tuv1_sentence)
			tu_element.appendChild(tuv1)

			tuv2 = doc.createElement('tuv')
			tuv2.setAttribute("xml:lang", direction[1])
			tu_element.appendChild(tuv2)
			tuv2_sentence_element = doc.createElement('seg')
			tuv2_sentence = doc.createTextNode(line[1])
			tuv2.appendChild(tuv2_sentence_element)
			tuv2_sentence_element.appendChild(tuv2_sentence)
			tu_element.appendChild(tuv2)

		return doc

########### 将DOM对象doc写入文件

if __name__ == '__main__':
	size = 400000
	sen = []
	with open("../tarfile/234txt","r") as f:
		sen = f.readlines()
	count = len(sen)/size

	for i in range(0,count+1):
		with open("../tmx/" + str(i) + ".tmx","w") as f:
			fin = sen[ count*size : count*size + size]
			gen = GenTmx()
			f.write(gen.gentmx("1","2",["ZH-CN","EN-US"],fin).toprettyxml(indent = ''))