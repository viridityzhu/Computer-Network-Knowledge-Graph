#-*-coding:utf-8-*-
import csv
import json
import sys
import codecs


def trans(path):
    jsonData = codecs.open(path + '.json', 'r', 'utf-8')

    csvfile = open(path + '.csv', 'w', newline='')  # python3下
    writer = csv.writer(csvfile)
    flag = True
    for line in jsonData:
        # print(line)
        dic = json.loads(line[1:])
        if flag:
            # 获取属性列表
            keys = list(dic.keys())
            print(keys)
            writer.writerow(keys)  # 将属性列表写入csv中
            flag = False
        dic['detail'].replace(',', '，').replace('\n', ' ')
        # 读取json数据的每一行，将values数据一次一行的写入csv中
        writer.writerow(list(dic.values()))
    jsonData.close()
    csvfile.close()


def title(path):
    jsonData = codecs.open(path + '.json', 'r', 'utf-8')

    csvfile = open('labels.txt', 'w', newline='')  # python3下
    writer = csv.writer(csvfile)
    flag = True
    for line in jsonData:
        # print(line)
        dic = json.loads(line[1:])

        # 读取json数据的每一行，将values数据一次一行的写入csv中
        writer.writerow([dic['title'] + ' 0'])
    jsonData.close()
    csvfile.close()

if __name__ == '__main__':
    path = 'hudong_pedia'  # 获取path参数
    print(path)
    title(path)
    print('ok')
