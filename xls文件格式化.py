import xlrd
# from xlutils.copy import copy
#
# # 打开工作簿
# rb = xlrd.open_workbook('1111.xls', formatting_info=True)
#
# # 复制工作簿以避免直接修改原始文件
# wb = copy(rb)
# # 遍历所有工作表
# for sheet_index in range(rb.nsheets):
#     ws = rb.sheet_by_index(sheet_index)
#     w_ws = wb.get_sheet(sheet_index)
#
#     # 遍历所有行
#     for row_index in range(ws.nrows):
#         # 遍历所有列
#         for col_index in range(ws.ncols):
#             cell = ws.cell(row_index, col_index)
#             # 获取单元格的值
#             value = cell.value
#             # 如果单元格包含公式，则尝试计算结果
#             if cell.xf_index != -1 and isinstance(value, str) and value.startswith('='):
#                 try:
#                     # 使用xlrd的公式计算结果
#                     result = rb.get_cell_value(row_index, col_index)
#                     # 将结果写入新工作簿
#                     w_ws.write(row_index, col_index, result)
#                 except Exception as e:
#                     # 如果计算出错，则写入None
#                     w_ws.write(row_index, col_index, None)
#             else:
#                 # 直接写入值
#                 w_ws.write(row_index, col_index, value)
# # 保存处理后的工作簿
# wb.save('your_file_cleaned.xls')



import xlrd
from xlutils.copy import copy

# 打开工作簿
rb = xlrd.open_workbook('1111.xls', formatting_info=False)

# 复制工作簿以避免直接修改原始文件
wb = copy(rb)

# 遍历所有工作表
for sheet_index in range(rb.nsheets):
    ws = rb.sheet_by_index(sheet_index)
    w_ws = wb.get_sheet(sheet_index)

    # 遍历所有行
    for row_index in range(ws.nrows):
        # 遍历所有列
        for col_index in range(ws.ncols):
            cell = ws.cell(row_index, col_index)
            # 获取单元格的值
            value = cell.value
            # 直接写入值，不保留任何格式
            w_ws.write(row_index, col_index, value)

# 保存处理后的工作簿
wb.save('your_file_cleaned_1.xls')

# ["data"]["data"]["GQL_getPageModulesData"]["2004318340"]["items"]["schemeList"]