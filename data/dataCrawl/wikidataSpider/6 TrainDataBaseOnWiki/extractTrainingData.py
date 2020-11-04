# -*- coding: utf-8 -*-

import os
import thulac
import sys
sys.path.append("..")
from toolkit.pre_load import pre_load_thu, neo_con  # , predict_labels
from toolkit.NER import get_NE, temporaryok, get_explain, get_detail_explain
import json
# 分句标识符号
stopToken = "。！？"


def CutStatements(line):
    statements = []
    tokens = []
    for token in line:
        tokens.append(token)
        # 如果是句子停止词
        if(token in stopToken):
            statements.append(''.join(tokens))
            tokens = []
    if(len(tokens) > 2):
        statements.append(''.join(tokens) + "。")
    return statements

thu = pre_load_thu  # 预先加载好
# 连接数据库
db = neo_con
print('toolkit ok.')
corpusPath = os.path.abspath(os.path.join(
    os.getcwd(), "../5 wikiextractor/extracted/"))
# 获取已经处理过得文件
print(corpusPath)
fileReadedList = []
with open("fileReaded.txt", "r") as fileReaded:
    for line in fileReaded:
        fileReadedList.append(line.strip())
        print(line.strip())
# 递归遍历语料库文件夹
print('start!')
with open("train_data.txt", 'w') as fw:
    with open("fileReaded.txt", "a") as filereaded:
        fw.write('entity1Pos\tentity1\tentity2Pos\tentity2\tstatement\trelation\n')

        for root, dirs, files in os.walk(corpusPath):
            for file in files:
                print(file)
                filePath = os.path.join(root, file)
                if(filePath in fileReadedList):
                    continue
                if(len(file) > 7 and file[-7:] == 'zh_hans'):
                    with open(filePath, 'r') as fr:

                        count = 0
                        for line in fr:
                            count += 1

                            if(count % 100 == 0):
                                print(filePath + "  " + str(count))
                            # 过滤掉<doc >  </doc> 等无用行
                            if(len(line) < 2 or line[0:4] == '<doc' or line[0:6] == "</doc>"):
                                continue
                            # 分句
                            statements = CutStatements(line)
                            # print('statements', statements)
                            for statement in statements:
                                # print(statement.strip())
                                # 分词
                                cutResult = get_NE(
                                    statement.strip())
                                # print('cutResult', cutResult)
                                # 得到每句话的实体列表后，两两匹配查询是否具有某种关系,如果有的话就写到文件中
                                # entityList
                                # 存储实体列表和实体出现的位置,entity1存储实体名称，entity1Index存储实体位置
                                entityList = []
                                nowIndex = -1
                                for word in cutResult:
                                    if(word[1] != 0 and not temporaryok(word[1])):
                                        entity1Index = statement.index(
                                            word[0], nowIndex + 1)
                                        entityList.append(
                                            {'entity1': word[0], 'entity1Index': entity1Index})
                                        nowIndex = entity1Index + \
                                            len(word[0]) - 1

                                entityNumber = len(entityList)
                                # print(entityList)
                                # print('num', entityNumber)
                                for i in range(entityNumber):
                                    answer = None
                                    # answer = entityRelationDict.get(entityList[i].get('entity1'))
                                    # if(entityRelationDict.get(entityList[i].get('entity1'))
                                    # is None):
                                    answer = db.findRelationByEntity(
                                        entityList[i].get('entity1'))
                                    # entityRelationDict[entityList[i].get('entity1')]
                                    # = answer
                                    for relation in answer:
                                        # print(relation)
                                        # 对neo4j的返回值进行处理，原来的返回值中包含一些没用的字符，最终得到的关系是rel,实体是entity2
                                        if(len(str(relation['rel']).split("\"")) < 2):
                                            continue
                                        rel = str(relation['rel']).split(
                                            "\"")[1]
                                        # print(rel)
                                        n2 = str(relation['n2'])
                                        index = n2.find('title')
                                        # print(n2, index, n2[index])
                                        flag = 0
                                        entity2 = str()
                                        while(flag < 2):
                                            if((n2[n2.find('title')] == '\"') and (flag == 0)):
                                                flag += 1
                                            elif((n2[n2.find('title')] == '\"') and (flag == 1)):
                                                flag += 1
                                            elif(flag == 1):
                                                entity2 = entity2 + \
                                                    n2[n2.find('title')]
                                            flag += 1
                                            # print('?')
                                        # 与entity1相关联的实体也出现在同一句话中，则可以制造一条训练样本
                                        nowIndex = -1
                                        for item in entityList:
                                            # print(item)
                                            if(entity2 == item.get('entity1') and item.get('entity1Index') != entityList[i].get('entity1Index')):
                                                print('有了！！！！！！！！')
                                                fw.write(str(entityList[i].get('entity1Index')) + '\t' + entityList[i].get('entity1') + '\t' + str(
                                                    item.get('entity1Index')) + '\t' + entity2 + '\t' + statement.strip() + '\t' + rel + '\n')

                    filereaded.write(filePath + '\n')
