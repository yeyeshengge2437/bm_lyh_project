import re

# 定义一个包含汉字的字符串
title = "这是一sf个测qe试s字符串，包含汉e字和英文字母123。"

# 使用正则表达式匹配所有汉字字符
chinese_chars = re.findall(r'[\u4e00-\u9fff]', title)

# 计算汉字的数量
chinese_count = len(chinese_chars)

print(f"字符串中的汉字数量是：{chinese_count}")