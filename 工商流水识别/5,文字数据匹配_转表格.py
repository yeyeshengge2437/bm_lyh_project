import os

from 夸克识别.quark_text_本地 import quark_text
import re
from datetime import datetime
import pandas as pd

def is_valid_date_format(s, start_year=2019, end_year=2024):
    # 正则表达式匹配格式为YYYYMMDD的日期
    pattern = r'^\d{4}\d{2}\d{2}'
    # 使用re.match检查字符串是否匹配该模式
    match = re.match(pattern, s)

    if match:
        time_str = match.group()
        # 尝试将字符串转换为日期
        try:
            time_value = datetime.strptime(time_str, '%Y%m%d')
            if time_value.year >= start_year and time_value.year <= end_year:
                return time_str, True
            else:
                return 0, False
        except ValueError:
            # 如果转换失败，说明日期不合法
            return 0, False
    else:
        return 0, False
data_list = []
# 遍历文件夹
for filename in os.listdir("pdf_images_width_plus"):
    print("---------------------", filename)
    value = quark_text("pdf_images_width_plus/" + filename)
    print(value)
    text = value["data"]["OcrInfo"][0]["Text"]
    print(text)
    # 通过换行符分割
    lines = text.split('\n')

    # 判断开头是不是日期数据
    for line in lines:
        value_dict = {}
        data_dict = {}
        time_str, value = is_valid_date_format(line)
        if value:
            pass
            # 去除字符串中的空格
            line = line.replace(" ", "")
            date_str = time_str
            print("日期：", date_str)
            # 匹配日期和金额之间的备注
            try:
                log_str = re.findall(fr'{time_str}(.*?)-?\d+', line)[0]
            except:
                log_str = "无"
            # 使用findall方法查找所有匹配项
            matches = re.findall(r'[\u4e00-\u9fa5](-?\d+,?\d+.?\d+,?\d+.?\d+[\u4e00-\u9fa5]*)', line)
            try:
                # 打印匹配结果
                for match in matches:
                    # print(match)
                    # 以.分割
                    parts = match.split('.')
                    # 第一部分 + 第二部分的前两个
                    part1 = parts[0] + '.' + parts[1][0:2]
                    print("交易金额：", part1)
                    # 第二部分去除前两个 + 第三部分的前两个
                    part2 = parts[1][2:] + '.' + parts[2][0:2]
                    print("余额：", part2)
                    # 第三部分去除前两个
                    part3 = parts[2][2:]
                    print("交易地点：", part3)
                    data_dict["日期"] = date_str
                    data_dict["摘要"] = log_str
                    data_dict["交易金额"] = part1
                    data_dict["余额"] = part2
                    data_dict["交易地点"] = part3
            except:
                print("_____________________", line)
            # break
        else:
            print("附言：", line)
            data_dict["附言"] = line

        data_dict.get("日期", date_str)
        data_dict.get("摘要", log_str)
        data_dict.get("交易金额", part1)
        data_dict.get("余额", part2)
        data_dict.get("交易地点", part3)
        data_dict.get("附言", line)


        if data_dict:
            data_list.append(data_dict)
    # print(data_list)
# 将数据转换为DataFrame
df = pd.DataFrame(data_list)
# 将DataFrame写入Excel文件
excel_path = 'output_2.xlsx'  # 你想要保存的Excel文件路径
df.to_excel(excel_path, index=False)  # index=False表示不将行索引写入Excel文件

print(f'数据已写入{excel_path}')


