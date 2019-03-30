#coding:utf-8
import jieba
import sys
import time
sys.path.append("../../")
import codecs
import os
import re 
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def FenCi(readfile,outfile):
	line = readfile.readline()
	while line:
		# 更高效的字符串替换
		# line.encode("utf-8")
		print line.encode('gb2312','ignore')
		lines=filter(lambda ch:ch not in '0123456789 ',line)
		newline =jieba.cut(lines,cut_all=False)
		str_out=' '.join(newline).encode('utf-8').replace('，',' ').replace('。',' ').replace('？',' ').replace('！',' ')\
					.replace('（',' ').replace('）',' ')\
					.replace('=',' ').replace('-',' ')\
					.replace('+',' ').replace(';',' ')\
					.replace(')',' ').replace(')',' ')\
					.replace('◣',' ').replace('◢',' ')\
					.replace('@',' ').replace('|',' ')\
					.replace('~',' ').replace(']',' ')\
					.replace('●',' ').replace('★',' ')\
					.replace('/',' ').replace('■',' ')\
					.replace('╪',' ').replace('☆',' ')\
					.replace('└',' ').replace('┘',' ')\
					.replace('─',' ').replace('┬',' ')\
					.replace('：',' ').replace('‘',' ')\
					.replace(':',' ').replace('-',' ')\
					.replace('、',' ').replace('.',' ')\
					.replace('...',' ').replace('?',' ')\
					.replace('“',' ').replace('”',' ')\
					.replace('《',' ').replace('》',' ')\
					.replace('!',' ').replace(',',' ')\
					.replace('】',' ').replace('【',' ')\
					.replace('·',' ')
		print str_out.encode('gb2312','ignore'),
		print >>outfile,str_out,
		line=readfile.readline()


	

if __name__ == '__main__':
	fromdir="./data"
	todir="./fenci1/"
	# 一次只能对一个文档进行分词
	file = u"计算机202.txt"
	file = u"交通214.txt"
	outfile = open(os.path.join(todir,file),'w+')   
	infile = open(os.path.join(fromdir,file),'r')
	FenCi(infile, outfile)
	infile.close()
	outfile.close()

