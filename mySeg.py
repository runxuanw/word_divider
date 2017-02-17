# -*- coding: utf-8 -*-
import codecs 
import sys
import re
from langconv import *

class Node:
    
    parent=''
    def __init__(self,value,frequence):
        self.value=value
        self.frequence=frequence
        self.length=len(value)
        self.children=[]
        
    def searchChild(self,string):
        for idx,i in enumerate(self.children):
            if string == i.value:
                return idx
        return -1
    
    '''because chinese characters could take multi bytes, it will return the node with its value of exactly equals the string,
    -1 means not found node, and the search should stop'''
    def iterSearchChild(self,string,length):
        if string[0:self.length]!=self.value:
            return -1
        for i in self.children:
            if i.length==length:
                if i.value==string:
                    return i
            elif string[0:i.length] == i.value:
                return i.iterSearchChild(string,length)
        return -1
    
    '''add the node as this node's child or as it's child's child node'''
    '''do check possible repeat same node'''
    def AddNode(self,node):
        if self.length<node.length:
            if node.value[0:self.length]!=self.value:
                #print "add node error: char does not match"
                '''this is probably due to a wrong guess from changing parent node'''
                return False
            
            '''if the node is one more char longer, directly add to it's child, check repeat child'''
            if (self.length+1)==node.length:
                match_idx=self.searchChild(node.value)
                if match_idx==-1:
                    self.children.append(node)
                    node.parent=self
                    return True
                else:
                    self.children[match_idx].frequence+=node.frequence
                    node.parent=self
                    return True
                    
            else:
                '''first check whether the node can be a child node for it's child, if
                it can, then let that child handle this node'''
                for i in self.children:
                    if node.value[0:i.length]==i.value:
                            i.AddNode(node)
                            return True
                '''if there is no child can habdle the node, create intermediate node as it's child'''
                intermediate = Node(node.value[0:self.length+1],0)
                self.children.append(intermediate)
                intermediate.parent=self
                intermediate.AddNode(node)
                return True
        else:
            #print "add node error: should be added to higher level node"
            '''this is probably due to a wrong guess from changing parent node'''
            return False

def trie():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    f=codecs.open("train_utf8.seg","r","utf-8")
#f3=codecs.open("train_utf8.seg","w","utf_8")
    f2=codecs.open("dict.txt","r")
    dic=[]
    wds=[]
    root=Node("",0)
#root.parent=root
    parent_node=root



    for idx,line in enumerate(f2):
        print idx 
        i=0
        new_node=Node("",0)
        for k in range(0,len(line)):
            if line[k]==' ':
                if i==0:
                    simp=line[0:k]
                    new_node.value=simp
                    new_node.length=len(simp)
                    i=1
                    j=k+1
                else:
                    new_node.frequence=int(line[j:k])
                    break
        while parent_node.AddNode(new_node)==False:
            parent_node=parent_node.parent
        parent_node=new_node.parent


    for idx,eachline in enumerate(f):
        print idx
        line=eachline

        for i in range(1,len(line)):
            if line[i]=='。':
                break
            if line[i]==' ':
                if j<=i-1:
                    wd=line[j:i]
                    wd = Converter('zh-hans').convert(wd.decode('utf-8'))
                    wd = wd.encode('utf-8')
                    wds.append(wd)
                #print wd
                    wd_node=Node(wd,1)
                    root.AddNode(wd_node)
                    j=i+1
        del line

    f.close()
    f2.close()
    return root

