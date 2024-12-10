from wx_ocr import identify_results
import os
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
path_list = []

for filename in os.listdir('pdf_images_width_plus'):
    path_list.append("pdf_images_width_plus/"+filename)

ident_value = identify_results(path_list)
for value in ident_value:
    # print(value)
    tager_y = []
    line_dict = {}
    sorted_line_dict = {}
    text_data = ""
    # 获取位置信息
    for item in value:
        location = item['location']
        left = location['left']
        top = location['top']
        right = location['right']
        bottom = location['bottom']
        # print(f'left: {left}, top: {top}, right: {right}, bottom: {bottom}')
        # 获取位置的中心点坐标
        center_x = (left + right) / 2
        center_y = (top + bottom) / 2
        # print(f'center_x: {center_x}, center_y: {center_y}')
        if center_x > 200 and center_x < 400:  # 位置为第一列的坐标
            # print(item['text'])
            tager_y.append(center_y)
    for item in value:
        location = item['location']
        left = location['left']
        top = location['top']
        right = location['right']
        bottom = location['bottom']
        for y_ in tager_y:
            if y_ > top and y_ < bottom:
                if y_ not in line_dict:
                    line_dict[y_] = [{'left': left, 'top': top, 'right': right, 'bottom': bottom, 'text': item['text']}]
                else:
                    line_dict[y_].append({'left': left, 'top': top, 'right': right, 'bottom': bottom, 'text': item['text']})
    for item in line_dict:
        sorted_line_dict[item] = sorted(line_dict[item], key=lambda x: x['left'])
    # print(sorted_line_dict)
    for item in sorted_line_dict:
        for i in sorted_line_dict[item]:
            text_data += i['text']
        text_data += '\n'
    print(text_data)

    lines = text_data.split('\n')

    # 判断开头是不是日期数据
    for line in lines:
        value_dict = {}
        data_dict = {}
        time_str, value = is_valid_date_format(line)
        if value:
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
            # print("附言：", line)
            data_dict["附言"] = line

        value_dict["日期"] = data_dict.get("日期")
        value_dict["摘要"] = data_dict.get("摘要")
        value_dict["交易金额"] = data_dict.get("交易金额")
        value_dict["余额"] = data_dict.get("余额")
        value_dict["交易地点"] = data_dict.get("交易地点")
        value_dict["附言"] = data_dict.get("附言")

        if data_dict:
            data_list.append(data_dict)
# print(data_list)
# 将数据转换为DataFrame
df = pd.DataFrame(data_list)
# 将DataFrame写入Excel文件
excel_path = 'output_1.xlsx'  # 你想要保存的Excel文件路径
df.to_excel(excel_path, index=False)  # index=False表示不将行索引写入Excel文件

print(f'数据已写入{excel_path}')

