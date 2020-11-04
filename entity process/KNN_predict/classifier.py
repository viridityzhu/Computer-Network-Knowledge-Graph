# coding: utf-8

from hudong_class import HudongItem
from neo_models import Neo4j
from pyfasttext import FastText
from functools import cmp_to_key
from math import log
from math import sqrt


class Node:
    simi = None
    label = None
    title = None

    def __init__(self, s, l, t):
        self.simi = s
        self.label = l
        self.title = t


class Classifier:
    model = None
    labeled_hudongList = None
    mean = None  # 各分量的均值
    var = None  # 各分量的方差
    title_simi = None
    detail_simi = None

    # 相似度权值，分别为：title，openTypeList，baseInfoKeyList，baseInfoValueList，detail
    weight = [0.3, 1]
    # knn的k值
    k = 10

    def __init__(self, model_path):  # 传入模型路径
        self.model = FastText(model_path)
        print('classifier load over...')

    def load_trainSet(self, HudongList):  # 传入已经标注过的hudongItem列表
        self.labeled_hudongList = HudongList

    def set_parameter(self, weight, k):  # 设置超参数
        self.weight = weight
        self.k = k

    # 返回2个item的titles相似度
    def get_title_simi(self, item1, item2):
        title_simi = self.model.similarity(item1.title, item2.title)
        return title_simi

    # 返回2个item的detail相似度
    def get_detail_simi(self, item1, item2):
        try:
            detail_simi = self.model.similarity(
                item1.detail[:60], item2.detail[:60])
        except TypeError:
            detail_simi = 0.0
        return detail_simi

    def KNN_predict(self, item):  # 预测互动页面的类别
        curList = []  # 用于存储和item相似度的临时列表

        mean = [0., 0.]  # 各分量的均值
        var = [0., 0.]  # 各分量的方差
        stand = [0., 0.]  # 各分量的标准差
        maxx = [-2333.3, -2333.3]
        minn = [2333.3, 2333.3]
        title_simi = []
        detail_simi = []

        i = 0
        for p in self.labeled_hudongList:  # 预先计算存储各分量相似度
            if p.title == item.title:  # 如果训练集已经有，直接返回label
                return p.label
            title_simi.append(self.get_title_simi(p, item))
            # print(item.title, p.title)
            detail_simi.append(self.get_detail_simi(p, item))
            mean[0] += title_simi[i]
            mean[1] += detail_simi[i]
            i += 1

        for i in range(2):
            mean[i] /= len(self.labeled_hudongList)

        for p in self.labeled_hudongList:  # 计算方差
            var[0] += (title_simi[i] - mean[0]) * (title_simi[i] - mean[0])
            var[1] += (detail_simi[i] - mean[1]) * \
                (detail_simi[i] - mean[1])

        for i in range(2):
            if var[i] == 0.0:
                var[i] = 0.000000001

        for i in range(2):
            stand[i] = sqrt(var[i])

        # 对title进行高斯归一，对detail进行maxmin归一
        i = 0
        for p in self.labeled_hudongList:
            title_simi[i] = (title_simi[i] - mean[0]) / stand[0]

            if detail_simi[i] == 0.0:  # 对于没有出现的，赋予平均值
                detail_simi[i] = mean[1]

            detail_simi[i] = (detail_simi[
                i] - mean[1]) / stand[1]

            i += 1

        i = 0
        count = 0
        for p in self.labeled_hudongList:  # 计算各项相似度的加权和
            s = self.weight[0] * title_simi[i] + \
                self.weight[1] * detail_simi[i]
            count += 1
            if count < 2:
                pass
            #	print(str(title_simi[i])+" "+str(openTypeList_simi[i])+" "+str(baseInfoKeyList_simi[i])+" "+str(baseInfoValueList_simi[i]))
            i += 1
            l = p.label
            t = p.title
            curList.append(Node(s, l, t))

        # 将训练集按照相对item的相似度进行排序
        curList.sort(key=lambda obj: obj.simi, reverse=True)

        count = [0., 0., 0., 0., 0., 0., 0., 0.,
                 0., 0., 0., 0., 0., 0., 0., 0., 0.]
        for i in range(self.k):
            label = int(curList[i].label)
            count[label] += curList[i].simi
            # print(curList[i].title+"----"+str(curList[i].simi)+'
            # '+str(label)) # 打印这k个

        maxx = -233
        answer = 0
        for i in range(17):
            if count[i] > maxx:
                maxx = count[i]
                answer = i
        return answer
