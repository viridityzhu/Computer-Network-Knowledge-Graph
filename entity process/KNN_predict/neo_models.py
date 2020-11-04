# coding: utf-8
# revised

from py2neo import Graph, Node, Relationship, NodeMatcher
from read_csv import readCSV2
from hudong_class import HudongItem


class Neo4j():
    graph = None

    def __init__(self):
        print("create neo4j class ...")

    def connectDB(self):
        self.graph = Graph("http://localhost:7474",
                           username="neo4j", password="111111",
                           secure=False, bolt=False,)
        self.matcher = NodeMatcher(self.graph)

    def matchItembyTitle(self, value):
        answer = self.matcher.match("HudongItem", title=value).first()
        return answer

    # 根据title值返回互动百科item
    def matchHudongItembyTitle(self, value):
        answer = self.matcher.match("HudongItem", title=value).first()
        return answer

    # 返回所有已经标注过的互动百科item   filename为labels.txt
    def getLabeledHudongItem(self, filename):
        labels = readCSV2(filename)
        llist = []
        i = 0
        for line in labels:

            ctx = self.matcher.match("HudongItem", title=line[0]).first()

            if ctx == None:
                continue
            cur = HudongItem(ctx)
            cur.label = line[1]
            llist.append(cur)

        print('load LabeledHudongItem over ...')
        print('got items: {}'.format(len(llist)))
        return llist

    # 返回限定个数的互动百科item
    def getAllHudongItem(self, limitnum):
        List = []
        ge = self.graph.find(label="HudongItem", limit=limitnum)
        for g in ge:
            List.append(HudongItem(g))

        print('load AllHudongItem over ...')
        return List


# test = Neo4j()
# test.connectDB()
# # answer = test.graph.find_one(
# #     label="HudongItem", property_key="title", property_value='火龙果')
# answer = test.matcher.match(
#     "HudongItem",  title='用户界面').first()
# print(answer)
# a = test.getLabeledHudongItem('labels.txt')
# print(a[10])
