# coding: utf-8


class HudongItem:
    title = None
    detail = None
    image = None
    openTypeList = None
    baseInfoKeyList = None
    baseInfoValueList = None
    label = None  # label值从文件中读取
    # 初始化，将字典answer赋值给类成员

    def __init__(self, answer):
        self.title = answer['title']
        self.detail = answer['detail']
        self.image = answer['image']
        label = -1
