from numpy import array
from matplotlib import pyplot
from Read_data import read_text_length, read_text_frequence
from itertools import groupby
from Save_to_json import save_to_json


# 字体设置
pyplot.rcParams['pdf.fonttype'] = 42
pyplot.rcParams['ps.fonttype'] = 42
# 默认为600&400
pyplot.rcParams['figure.figsize'] = (8.0, 6.0)
# 默认分辨率为100
# 指定dpi=300，图片尺寸为 1800*1200
# 设置figsize可以在不改变分辨率情况下改变比例
# plt.rcParams['savefig.dpi'] = 300 #图片像素
# plt.rcParams['figure.dpi'] = 300 #分辨率



# 画直方图
def draw_hist(name, value):

	# print(pyplot.rcParams['pdf.fonttype'])

	pyplot.bar(x=name, height=value, width=0.8, color='#696969')
	pyplot.title('length of text')
	pyplot.xlabel('text length group')
	pyplot.ylabel('number')

	# 获取当前的坐标轴
	ax = pyplot.gca()

	# 横坐标标签隔一显示
	xs = [name[i] for i in range(len(name)) if i%2 == 0]
	ax.axes.set_xticks(xs)

	# 设置坐标轴取值范围
	# pyplot.xlim(min_, max_)
	# pyplot.ylim(min_, max_)

	# 设置x坐标轴为下边框
	ax.xaxis.set_ticks_position('bottom')
	# 设置y坐标轴为左边框
	ax.yaxis.set_ticks_position('left')

	# 设置刻度标签倾斜程度
	pyplot.xticks(rotation=45)

	# 避免显示不全
	pyplot.tight_layout()

	# 显示
	pyplot.show()
	
	# 保存
	# pyplot.savefig("length_of_text.pdf")
	pass


# 统计区间频数
def count_frequence(list_data, interval):
	list_res = []
	for k, g in groupby(sorted(list_data), key=lambda x: x//interval):
		string = '{}-{}'.format(k*interval, (k+1)*interval-1)
		dict_data = {}
		dict_data[string] = len(list(g))
		print(dict_data[string])
		list_res.append(dict_data)
	save_to_json('length_frequence_1000.json', list_res)


# 数据标准化
def formatting(list_data):
	list_name = []
	list_value = []
	for data in list_data:
		# print(type(data))
		key = list(data.keys())[0]
		value = data[key]
		list_name.append(key)
		list_value.append(value)
	return list_name, list_value
		

# 主函数
def main():

	# list_data = read_text_length('counter_text_length.json')
	# count_frequence(list_data, 1000)

	data = read_text_frequence('length_frequence_1000.json')
	# print(data)

	list_name, list_value = formatting(data)
	draw_hist(array(list_name), array(list_value))
	

if __name__ == '__main__':
	main()