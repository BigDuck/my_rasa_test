import configparser
import json
import os
import re

from TimeNormalizer import TimeNormalizer

month_day_pattern = '[0-9]{1,2}月[0-9]{1,2}[日|号]'
transport_pattern = '飞机|火车|动车|的士|大巴|轮船|其他'
month_day_re = re.compile(month_day_pattern)
transport_re = re.compile(transport_pattern)
cf = configparser.ConfigParser()
tn = TimeNormalizer()

'''
# 用正则的方式获取句子中的日期（目前获取积月几日形式的）
'''


def get_date(date_str):
    return month_day_re.findall(date_str)


'''
获取配置文件ini 格式 section 模块 item 就是key

'''


def get_config(section, item):
    if len(cf.sections()) == 0:
        print("读取配置文件")
        abspath = os.path.abspath("../conf/config.ini")
        cf.read(abspath)  # 读取配置文件，如果写文件的绝对路径，就可以不用os模块
    if section is None:
        return cf.sections()
    # 获取文件中所有的section(一个配置文件中可以有多个配置，如数据库相关的配置，邮箱相关的配置，    每个section由[]
    #     包裹，即[section])，并以列表的形式返回
    else:
        if item is None:
            return cf.options(section)
        else:
            return cf.get(section, item)


# 中文的日期转换为数值的日期 如星期三转换为年月日后的日期,返回json格式如下
# {"error": "no time pattern could be extracted."}
# {"type": "timestamp", "timestamp": "2019-09-10 00:00:00"}
def chinese_date_to_date(date_str):
    return json.loads(tn.parse(date_str))


'''
以正则的方式获取交通工具
'''


def get_transport(data_str):
    return transport_re.findall(data_str)


if __name__ == '__main__':
    print(get_date("我7月4日去北京"))
    transport = get_transport("坐飞机")
    if len(transport) != 0:
        print(transport[0])
    else:
        print("没有交通工具")
    print(chinese_date_to_date("星期三"))