import os
import re
import pandas as pd
import numpy as np
import jieba
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
font = FontProperties(fname=r'c:\windows\fonts\simsun.ttc')#,size=20指定本机的汉字字体位置

jieba.load_userdict('斗破苍穹.txt')
jieba.load_userdict('斗破苍穹异火.txt')
stopwords = open('中文停用词表（比较全面，有1208个停用词）.txt','r').read()
stopwords = stopwords.split('\n')

# 返回文章列表
def readData():
	os.chdir(r'C:\Users\t_dw\Desktop\文本分析')
	texts = open('all（校对版全本）.txt',"r")
	texts = texts.read()
	AllChapters = re.split('第[0-9]*章',texts)[1:]
	return AllChapters

# 数据载入pandas 返回pandas对象
def preprocessing(list_text):
	# pandas 对象 并添加列属性
	AllChapters = pd.DataFrame(list_text, columns = ['text'])
	# 对text属性列 实行分词操作 生成新的pandas对象result
	result = pd.DataFrame(AllChapters.text.apply(participel))
	# 对result对象添加列属性fenci
	result.columns = ['fenci']
	# print(result)
	return result

# 分词
def participel(x):
	cut_text = " ".join([w for w in jieba.cut(x) if w not in stopwords])
	return cut_text

# 统计个数
def counter(result):
	# pandas对象添加列属性
	result['熏儿'] = result.fenci.apply(lambda x:x.count('熏儿') + x.count('薰儿'))
	result['云韵'] = result.fenci.apply(lambda x:x.count('云韵'))
	result['小医仙'] = result.fenci.apply(lambda x:x.count('小医仙'))
	result['彩鳞'] = result.fenci.apply(lambda x:x.count('彩鳞') + x.count('美杜莎'))
	# print(result)
	return result

# 画长图
def drawLGraph(result):

	plt.figure(figsize=(15,5))
	# plot(x轴坐标列表， y轴坐标列表，color， 标签)
	plt.plot(np.arange(1,result.shape[0]+1), result['熏儿'], color="r", label = u'熏儿')
	# plt.plot(np.arange(1,result.shape[0]+1), result['云韵'], color="lime", label = u'云韵')
	# plt.plot(np.arange(1,result.shape[0]+1), result['小医仙'], color="gray", label = u'小医仙')
	plt.plot(np.arange(1,result.shape[0]+1), result['彩鳞'], color="orange", label = u'彩鳞')
	plt.legend(prop=font)
	plt.xlabel(u'章节',fontproperties=font)
	plt.ylabel(u'出现次数',fontproperties=font)
	plt.show()

#功能： 女主每章出现次数统计【熏儿，云韵，小医仙，美杜莎】
def main():
	list_text = readData()
	result = preprocessing(list_text)
	result = counter(result)
	drawLGraph(result)

if __name__ == '__main__':
	main()