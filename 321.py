import json

value = {'id': 100004, 'name': '', 'tell_tool': 'kimi_32k', 'files': '["https://res.debtop.com/manage/live/paper/202410/24/202410240104529329079dccf34009.png"]', 'input_text': '请根据图片中的公告内容，提取信息，输出两个表格，缺失值用“-”表示。表格一提取标题、转让人全称、受让人全称、当前债权人全称、债权户数、债权总额、基准日期（一个字段为一列，共一行），表格二提取债务人、债权本金、债权利息、债权本息、其他费用、保证人、抵押物详情、诉讼案号（一个字段为一列，一笔债权为一行。对于单户债权的公告，第一个为债务人，其他为保证人，合并一行显示）'}
file = value.get('files')
file_url = json.loads(file)[0]
print(file_url)
