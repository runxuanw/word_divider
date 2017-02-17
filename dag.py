# -*- coding: utf-8 -*-
import codecs 
import sys
import re
from langconv import *
from mySeg import *
reload(sys)
sys.setdefaultencoding('utf-8')
f=codecs.open("test_utf8.seg","r","utf-8")
f3=codecs.open("result.txt","w","utf-8")
t=0


wds=[]

root=trie()
index_node=''

from fractions import Fraction
import math
'''
for i in range(0,len(freq)):
	freq[i]=Fraction(freq[i],60101967)
	'''
for eachline in f:
	line=eachline
	i=0
	if t==0:
		i=1
	k=0
	temp=k
	A=[]
	print len(line)
	print line[-2]=='\r'
	print line[0]
	p=re.compile(ur'[^\u4e00-\u9fa5]')
	zh="".join(p.split(line)).strip()
	#print len(zh)
	print line
	print zh
	for j in range(i,len(line)-2):
		if line[j]==zh[k]:
			k+=1
			if k>=len(zh):
				A.append(zh[temp:k])
				break
		elif temp<k:
			A.append(zh[temp:k])
			temp=k
	#st = Converter('zh-hans').convert(zh.decode('utf-8'))
	#st = st.encode('utf-8')
	AA=[]
	for i in range(0,len(A)):
		E=[[0 for col in range(len(A[i])+1)] for row in range(len(A[i])+1)]
		#print E
		for h in range(0,len(A[i])+1):
			'''wrx'''
			index_node=root
			'''wrx end'''
			for l in range(h+1,len(A[i])+1):
				F = Converter('zh-hans').convert(A[i][h:l].decode('utf-8'))
				F = F.encode('utf-8')
				#print F
				'''wrx'''
				temp_node=index_node.iterSearchChild(F,len(F))
				if temp_node!=-1:
					E[h][l]=Fraction(temp_node.frequence,60101967)
					index_node=temp_node
				else:
					'''should end the F search here and start a new H search'''
					for laterIdx in range(l,len(A[i])+1):
						E[h][laterIdx]=0
					break
				'''wrx end'''
		#print E
		G=[[0,0] for col in range(len(A[i])+1)]
		#print G
		for ii in range(1,len(G)):
			md=1000000000000
			for ij in range(0,ii):
				if E[ij][ii]!=0 and E[ij][ii]+G[ij][0]<md:
					md=E[ij][ii]+G[ij][0]
					ind=ij
			G[ii][0]=md
			G[ii][1]=ind
		#print G
		H0=[]
		H=[]
		pre=G[len(G)-1][1]
		while pre!=0:
			H0.append(pre)
			pre=G[pre][1]
		for ii in range(0,len(H0)):
			H.append(H0[len(H0)-ii-1])
		H.append(len(G)-1)
		#H.append(len(G))
		print H
		temp=0
		for ii in range(0,len(H)):
			AA.append(A[i][temp:H[ii]])
			temp=H[ii]
		print AA
	#zi = Converter('zh-hans').convert(zh[4].decode('utf-8'))
	#zi = zi.encode('utf-8')
	#print zi

#print line1[0]==line[0]
f.close()
exit(0)