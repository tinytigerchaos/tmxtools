#coding=utf-8
import chardet
with open("C:\\data\\456.tmx",'r') as f:
	print chardet.detect(f.read())