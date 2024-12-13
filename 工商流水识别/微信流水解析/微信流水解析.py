import os
import re

import openpyxl
# 指定要遍历的文件夹路径
folder_path = 'E-1707212050543_(2024)苏0281调查令21号'
bank_statements = ['用户ID', '交易单号', '大单号', '用户侧账号名称', '借贷类型', '交易业务类型', '交易用途类型', '交易时间', '交易金额(分)', '账户余额(分)', '用户银行卡号', '用户侧银行名称', '用户侧网银联单号', '网联/银联', '第三方账户名称', '对手方ID', '对手侧账户名称', '对手方银行卡号', '对手侧银行名称', '对手侧网银联单号', '网联/银联', '第三方账户名称', '对手方接收时间', '对手方接收金额(分)', '备注1', '备注2']
binding_history = ['账号', '银行卡号', '银行名称', '证件号', '证件类型', '手机号', '绑定状态', '绑定时间', '解绑时间']
data_statements = []
data_history = []
# 遍历指定文件夹及其子文件夹, 长度27
now_table = ['用户ID', '交易单号', '大单号', '用户侧账号名称', '借贷类型', '交易业务类型', '交易用途类型', '交易时间', '交易金额(分)', '账户余额(分)', '用户银行卡号', '用户侧银行名称', '用户侧网银联单号', '网联/银联', '第三方账户名称', '对手方ID', '对手侧账户名称', '对手方银行卡号', '对手侧银行名称', '对手侧网银联单号', '网联/银联', '第三方账户名称', '对手方接收时间', '对手方接收金额(分)', '备注1', '备注2', '身份证号']
data_statements.append(now_table)
data_history.append(binding_history)
for root, dirs, files in os.walk(folder_path):
    for file in files:
        # 检查文件扩展名是否为.txt
        if file.endswith('.txt'):
            # 构建完整的文件路径
            file_path = os.path.join(root, file)
            # 获取各个文件的表头
            # 这里可以对文件进行操作，例如打印文件路径
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                line_1 = lines[0]
                table_top = line_1.strip().split('\t')
                if table_top == bank_statements:
                    bank_card_number = ''.join(re.findall(r'\\IDCARD\\(\d+)\\', file_path))
                    if len(lines) > 1:
                        for line in lines[1:]:
                            list_line = line.strip().split('\t')
                            add_num = 26 - len(list_line)
                            for i in range(add_num):
                                list_line.append('')
                            list_line.append(bank_card_number)
                            data_statements.append(list_line)
                elif table_top == binding_history:
                    if len(lines) > 1:
                        for line in lines[1:]:
                            list_line = line.strip().split('\t')
                            data_history.append(list_line)

print(data_history)

# 创建一个新的Excel工作簿
wb_1 = openpyxl.Workbook()
ws_1 = wb_1.active

# 将数据写入Excel工作表
for row_data in data_statements:
    ws_1.append(row_data)

# 保存Excel文件
wb_1.save(f'{folder_path}微信流水.xlsx')

# 创建一个新的Excel工作簿
wb_2 = openpyxl.Workbook()
ws_2 = wb_2.active

# 将数据写入Excel工作表
for row_data in data_history:
    ws_2.append(row_data)

# 保存Excel文件
wb_2.save(f'{folder_path}绑定历史.xlsx')
