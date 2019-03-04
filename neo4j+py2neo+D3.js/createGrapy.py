#!/usr/bin/python
# -*- coding: utf-8 -*-

# py2noe 
# 库用法：官方文档：http://py2neo.org/
# GitHub：https://github.com/technige/py2neo

# 安装：	pip install py2neo

# 从py2neo 库中导入 Graph, Node, Relationship 三个主要模块
from py2neo import Graph, Node, Relationship, RelationshipMatcher
# 导入pandas库
import pandas as pd
# 导入numpy库
import numpy as np
import json

# 读取 excel 数据
def readExcel():
    path = r'漏洞整理.xlsx'
    pd_data = pd.read_excel(io=path, sheet_name='Sheet2', header=0)
    # 查看原始数据
    # print(pd_data)
    # 转化为np对象
    np_data = np.array(pd_data)
    # print(np_data.shape)
    # print(np_data[:,0:3])
    return np_data[:,1:4]

def Grapy(np_data, graph):


	graph.delete_all()
	# tx = graph.begin()
	# 创建Node结点对象
	# 结点对象有lable 标签 和 属性
	# person 是其lable 标签， 有一个属性name
	
	for row in np_data:
		device, vul, patch = row[0], row[1], row[2]
		
		# 设备
		if not len(graph.nodes.match("device", name=device)):
			denode = Node('device', name=device)
			graph.create(denode)
		res_device = graph.nodes.match('device', name=device).first()

	
		# 漏洞
		if not len(graph.nodes.match("vul", name=vul)):
			vulnode = Node('vul', name=vul)
			graph.create(vulnode)
		res_vul = graph.nodes.match('vul', name=vul).first()

		# 设备-漏洞
		dv = Relationship.type("device-vul")
		graph.merge(dv(res_device, res_vul))

		# 补丁
		if not len(graph.nodes.match("patch", name=patch)):
			patchnode = Node('patch', name=patch)
			graph.create(patchnode)
		res_patch = graph.nodes.match('patch', name=patch).first()

		# 漏洞-补丁
		vp = Relationship.type("vul-patch")
		graph.merge(vp(res_vul, res_patch))

		# 补丁-设备
		pd = Relationship.type("patch-device")
		graph.merge(pd(res_patch, res_device))

def readGrapy(graph):

	nodes = []
	for i in graph.nodes.match('device'):
		print(i['name'])
		node_device = {}
		node_device['id'] = i['name']
		node_device['group'] = 1
		nodes.append(node_device)

	for i in graph.nodes.match('vul'):
		print(i['name'])
		node_vul = {}
		node_vul['id'] = i['name']
		node_vul['group'] = 2
		nodes.append(node_vul)

	for i in graph.nodes.match('patch'):
		print(i['name'])
		node_patch = {}
		node_patch['id'] = i['name']
		node_patch['group'] = 3
		nodes.append(node_patch)

	links = []
	matcher = RelationshipMatcher(graph)
	for i in matcher.match():
		source = i.start_node['name']
		target = i.end_node['name']

		dict_link = {}
		dict_link['source'] = source
		dict_link['target'] = target
		dict_link['value'] = 1
		links.append(dict_link)
	dict_json = {}
	dict_json["nodes"] = nodes
	dict_json["links"] = links
	saveToJson(dict_json)

def saveToJson(dict_json):
	with open('graphD3.json', 'a', encoding='utf-8') as fw:
		json.dump(dict_json, fw, indent=4, ensure_ascii=False)

def main():
	np_data = readExcel()
	graph = Graph(password='graph')
	Grapy(np_data, graph)
	readGrapy(graph)

if __name__ == '__main__':
	main()
