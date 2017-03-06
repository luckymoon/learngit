#!/usr/bin/env python
#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
'''
	python search.py name
 	查找该目录和子目录下包含name的文件
'''
def search(kw,dir=os.path.abspath('.')):
	for i in os.listdir(dir):
		path=os.path.join(dir,i)
		if os.path.isfile(path) and kw in i:
			print path
		elif os.path.isdir(path):
			search(kw,path)
	

if __name__=="__main__":
	search(sys.argv[1])
