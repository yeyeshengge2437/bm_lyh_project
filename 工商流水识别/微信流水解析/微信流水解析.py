import os

# # 指定要遍历的文件夹路径
# folder_path = '20240115-恒隆案件微信流水'
#
# # 遍历指定文件夹及其子文件夹
# for root, dirs, files in os.walk(folder_path):
#     for file in files:
#         # 检查文件扩展名是否为.txt
#         if file.endswith('.txt'):
#             # 构建完整的文件路径
#             file_path = os.path.join(root, file)
#             # 这里可以对文件进行操作，例如打印文件路径
#             # with open(file_path, 'r', encoding='utf-8') as f:
#             #     print(f.read())
#             print(file_path)


# with open("TenpayTrades.txt", 'r', encoding='utf-8') as f:
#     print(f.read())

import openpyxl

# 打开TXT文件并读取内容
with open('TenpayTrades.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 处理数据，假设每行数据以制表符分隔
data = [line.strip().split('\t') for line in lines]

# 创建一个新的Excel工作簿
wb = openpyxl.Workbook()
ws = wb.active

# 将数据写入Excel工作表
for row_data in data:
    ws.append(row_data)

# 保存Excel文件
wb.save('your_file.xlsx')
