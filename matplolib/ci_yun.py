import os
import re
import pandas as pd
import numpy as np
import jieba
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
font = FontProperties(fname=r'c:\windows\fonts\simsun.ttc')#,size=20指定本机的汉字字体位置
from wordcloud import WordCloud
from PIL import Image

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
	return AllChapters[:20]

# 数据载入pandas 返回pandas对象
def preprocessing(list_text):
	# pandas 对象 并添加列属性
	AllChapters = pd.DataFrame(list_text, columns = ['text'])
	# 对text属性列 实行分词操作 生成新的pandas对象result
	result = pd.DataFrame(AllChapters.text.apply(participel))
	# 对result对象添加列属性fenci
	result.columns = ['fenci']

	AllChapters = pd.DataFrame(list_text, columns = ['text'])
	textsall = ''.join(result.fenci.tolist())

	return textsall

# 分词
def participel(x):
	cut_text = " ".join([w for w in jieba.cut(x) if w not in stopwords])
	return cut_text

# 生成词云
def ciYun(cloud_text):
	#加载背景图片
	cloud_mask = np.array(Image.open("词云.jpg"))

	#忽略显示的词
	st=set(["东西","这是"])
	#生成wordcloud对象
	wc = WordCloud(
		background_color="white", 
	    mask=cloud_mask,
	    max_words=200,
	    font_path=r'c:\windows\fonts\simsun.ttc',
	    min_font_size=15,
	    max_font_size=50, 
	    width=400, 
	    stopwords=st
	    )
	wc.generate(cloud_text)
	# wc.to_file("pic.png")

	# 输出图片
	plt.axis('off')
	plt.imshow(wc)
	plt.show()


def main():
	textsall = preprocessing(readData())
	ciYun(textsall)

if __name__ == '__main__':
	main()


'''
wordcloud 参数说明
Parameters
 |  ----------
 |  font_path : string
 |       使用的字体库
 |  width : int (default=400)
 |      图片宽度
 |  height : int (default=200)
 |      图片高度
 |  mask : nd-array or None (default=None)
 |      图片背景参考形状  
 |  scale : float (default=1)
 |      图幅放大、缩小系数  
 |  min_font_size : int (default=4)
 |      最小的字符
 |  min_font_size : int (default=4)
 |      最大的字符
 |  max_words : number (default=200)
 |      最多显示的词数
 |  stopwords : set of strings or None
 |      不需要显示的词
 |  background_color : color value (default="black")
 |      背景颜色
 |  ......
'''