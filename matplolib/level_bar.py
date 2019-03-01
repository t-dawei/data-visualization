import os
import re
import pandas as pd
import numpy as np
import jieba
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
font = FontProperties(fname=r'c:\windows\fonts\simsun.ttc')#,size=20指定本机的汉字字体位置

# 返回文章列表
def readData():
	os.chdir(r'C:\Users\t_dw\Desktop\文本分析')
	texts = open('all（校对版全本）.txt',"r")
	texts = texts.read()
	AllChapters = re.split('第[0-9]*章',texts)[1:]

	nameall = open('所有人物.txt','r').read().split('\n')

	
	return AllChapters, nameall

# 数据载入pandas 返回pandas对象
def preprocessing(list_text, nameall):
	# pandas 对象 并添加列属性
	AllChapters = pd.DataFrame(list_text, columns = ['text'])
	textsall = ''.join(AllChapters.text.tolist())
	# pandas 对象
	nameall = pd.DataFrame(nameall,columns = ['name'])
	return textsall, nameall

def counter(textsall, nameall):
	nameall['num'] = nameall.name.apply(lambda x:textsall.count(x))
	nameall.loc[nameall.name=='熏儿','num'] = nameall.loc[nameall.name=='熏儿','num'].values[0] + nameall.loc[nameall.name=='薰儿','num'].values[0]
	nameall.loc[nameall.name=='彩鳞','num'] = nameall.loc[nameall.name=='彩鳞','num'].values[0] + nameall.loc[nameall.name=='美杜莎','num'].values[0]
	nameall = nameall[(~nameall['name'].isin(['薰儿','美杜莎']))]
	# ascending=False 降序
	nameall = nameall.sort_values('num', ascending=False)
	print(nameall)
	return nameall

def drawLBar(nameall):
	n = 50
	plt.figure(figsize=(8,10))
	plt.barh(range(len(nameall.num[:n][::-1])),nameall.num[:n][::-1], color = 'darkred')

	fig = plt.axes()
	fig.set_yticks(np.arange(len(nameall.name[:n][::-1])))
	fig.set_yticklabels(nameall.name[:n][::-1], fontproperties=font)
	plt.xlabel('人物出场次数', fontproperties = font)
	plt.show()

def main():
	AllChapters, nameall = readData()
	textsall,nameall = preprocessing(AllChapters, nameall)
	nameall = counter(textsall, nameall)
	drawLBar(nameall)

if __name__ == '__main__':
	main()

	
	