# -*- coding: utf-8 -*-

from math import floor
from operator import mod
import os
import struct

class DayData(object):
    """
    通达信日线*.day文件
    文件名即股票代码
    每32个字节为一天数据
    每4个字节为一个字段,每个字段内低字节在前
    00 ~ 03 字节：年月日, 整型
    04 ~ 07 字节：开盘价*100, 整型
    08 ~ 11 字节：最高价*100,  整型
    12 ~ 15 字节：最低价*100,  整型
    16 ~ 19 字节：收盘价*100,  整型
    20 ~ 23 字节：成交额（元）,float型
    24 ~ 27 字节：成交量（股）,整型
    28 ~ 31 字节：（保留）
    """
    price_date      = 0
    price_opening   = 0.0
    price_highest   = 0.0
    price_lowest    = 0.0
    price_closing   = 0.0
    turnover        = 0.0
    volume          = 0

    def __init__(self, day_data_row):

        assert len(day_data_row) == 32, "day_data_row length must be 32"

        data = struct.unpack("IIIIIfII", day_data_row)
        self.price_date     = data[0]
        self.price_opening  = data[1] / 100
        self.price_highest  = data[2] / 100
        self.price_lowest   = data[3] / 100
        self.price_closing  = data[4] / 100
        self.turnover       = data[5] / 100
        self.volume         = data[6]
        pass

    def print_log(self):
        print(self.__dict__)
        pass

class MinuteData(object):
    """
    通达信日线*.lc5/lc1文件
    文件名即股票代码
    每32个字节为一个5分钟数据, 每字段内低字节在前
    00 ~ 01 字节：日期, 整型, 设其值为num, 则日期计算方法为：
                  year=floor(num/2048)+2004;
                  month=floor(mod(num,2048)/100);
                  day=mod(mod(num,2048),100);
    02 ~ 03 字节： 从0点开始至目前的分钟数, 整型
    04 ~ 07 字节：开盘价*100, 整型
    08 ~ 11 字节：最高价*100, 整型
    12 ~ 15 字节：最低价*100, 整型
    16 ~ 19 字节：收盘价*100, 整型
    20 ~ 23 字节：成交额*100, 整型
    24 ~ 27 字节：成交量（股）, 整型
    28 ~ 31 字节：（保留）
    """
    price_date      = 0
    price_time      = 0
    price_opening   = 0.0
    price_highest   = 0.0
    price_lowest    = 0.0
    price_closing   = 0.0
    turnover        = 0.0
    volume          = 0

    def __init__(self, minute_data_row):

        assert len(minute_data_row) == 32, "minute_data_row length must be 32"

        data = struct.unpack("HHffffiif", minute_data_row)

        date    = data[0]
        year    = floor(date/2048) + 2004
        month   = floor(date % 2048 / 100)
        day     = date % 2048 % 100
        hour    = floor(data[1] / 60)
        minute  = data[1] % 60

        self.price_date     = year * 10000 + month * 100 + day
        self.price_time     = hour * 100 + minute
        self.price_opening  = data[2]
        self.price_highest  = data[3]
        self.price_lowest   = data[4]
        self.price_closing  = data[5]
        self.turnover       = data[6]
        self.volume         = data[7]
        pass

    def print_log(self):
        print(self.__dict__)
        pass

class DataFile(object):

    def __init__(self, file_path):
        self.file_path = file_path

        file_name = os.path.basename(file_path)

        self.stock_code = file_name.split(".")[0]
        self.file_type = file_name.split(".")[1]

        assert self.file_type in ["day", "lc1", "lc5"], "file_type must be day/lc1/lc5"

        self.file_handle = None
        self.file_size = 0
        self.file_pos = 0
        self.data_list = []

        pass

    def get_data_count(self):
        return len(self.data_list)

def day_file_handler(file_path):
    """
    处理通达信日线文件
    """
    day_file = DataFile(file_path)
    day_file.file_size = os.path.getsize(day_file.file_path)

    with open(day_file.file_path, "rb") as file_handle:
        raw_data = file_handle.read(32)
        while raw_data is not None and len(raw_data) == 32:
            day_data_raw = DayData(raw_data)
            day_file.data_list.append(day_data_raw)

            raw_data = file_handle.read(32)
            pass

    return day_file