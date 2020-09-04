# -- coding: utf-8 --
# @Time: 2020/8/6 14:47
# @Author: liujianghua
# @Software: PyCharm
# @description: 正则解析数据
import re


def parse_name(content, field: list):
    for pattern in field:
        res = re.findall(pattern, content)
        if res:
            return res[0].strip()








