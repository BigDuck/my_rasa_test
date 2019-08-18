import re

pattern = '[0-9]{1,2}月[0-9]{1,2}[日|号]'
re_compile = re.compile(pattern)


# 用正则的方式获取句子中的日期（目前获取积月几日形式的）
def get_date(date_str):
    return re_compile.findall(date_str)


if __name__ == '__main__':
    date = get_date(u'7月5号到7月9号我要去出差')
    print(date[0])
    print(date[1])
    print(date[2])
    for tmp in date:
        print(tmp)