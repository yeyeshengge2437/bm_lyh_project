# 假设你有一个包含字符串的列表，这些字符串中包含单引号
import json

list_with_single_quotes = ['apple', 'banana', 'cherry']
list_with_single_quotes = str(list_with_single_quotes)
# 使用列表推导式替换字符串中的单引号为双引号
list_with_single_quotes = list_with_single_quotes.replace("'", '"')
json.dumps(list_with_single_quotes, ensure_ascii=False)
# 输出结果查看
print(list_with_single_quotes)