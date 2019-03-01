import pandas as pd
import os
os.chdir(r'C:\Users\t_dw\Desktop\文本分析')
import numpy as np
import jieba
from matplotlib.font_manager import FontProperties
import networkx as nx  


# 社交网络图  共现矩阵
# 两个人物出现在同一段，说明有某种关系


def readData():
    # 读取数据
    words = open('all（校对版全本）.txt','r').readlines()
    words = pd.DataFrame(words,columns = ['text'],index = range(len(words)))
    words['wordnum'] = words.text.apply(lambda x:len(x.strip()))
    words = words.loc[words.wordnum>20,]
    wrods = words.reset_index(drop = True)

    nameall = open('所有人物.txt','r').read().split('\n')
    nameall = pd.DataFrame(nameall,columns = ['name'])
    # 创建关系pandas对象 行列都为姓名 矩阵初始值为0
    relationmat = pd.DataFrame(index = nameall.name.tolist(), columns = nameall.name.tolist()).fillna(0)
    print(relationmat)
    return relationmat, nameall


# 生成共现矩阵
def counter(relationmat, nameall)
    wordss = words.text.tolist()
    for k in range(len(wordss)):
        for i in nameall.name.tolist():
            for j in nameall.name.tolist():
                if i in wordss[k] and j in  wordss[k]:
                    relationmat.loc[i,j] += 1 
        if k%1000 == 0:
            print(k)

    print(relationmat)
    relationmat.to_excel('共现矩阵.xlsx')

# 网络图
# 边与权重矩阵
def netGraph()

    relationmat1 = {}
    for i in relationmat.columns.tolist():
        for j in relationmat.columns.tolist():
            relationmat1[i, j] = relationmat.loc[i,j]


    edgemat = pd.DataFrame(index = range(len(relationmat1)))
    node = pd.DataFrame(index = range(len(relationmat1)))

    edgemat['Source'] = 0
    edgemat['Target'] = 0
    edgemat['Weight'] = 0

    node['Id'] = 0
    node['Label'] = 0
    node['Weight'] = 0


    names = list(relationmat1.keys())
    weights = list(relationmat1.values())
    for i in range(edgemat.shape[0]):
        name1 = names[i][0]
        name2 = names[i][1]
        if name1!=name2:
            edgemat.loc[i,'Source'] = name1
            edgemat.loc[i,'Target'] = name2
            edgemat.loc[i,'Weight'] = weights[i]
        else:
            node.loc[i,'Id'] = name1
            node.loc[i,'Label'] = name2
            node.loc[i,'Weight'] = weights[i]        
        i+=1


    edgemat = edgemat.loc[edgemat.Weight!=0,]
    edgemat = edgemat.reset_index(drop = True)
    node = node.loc[node.Weight!=0,]
    node = node.reset_index(drop = True)



    edgemat.to_csv('边.csv',index = False)
    node.to_csv('节点.csv',index = False)
