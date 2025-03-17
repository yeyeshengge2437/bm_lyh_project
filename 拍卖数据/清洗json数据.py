import json

try:
    with open("tb_all_url_data.json", "r") as file:
        datas = json.load(file)
except FileNotFoundError:
    print("文件不存在！")
except json.JSONDecodeError:
    print("JSON 格式错误！")
for data in datas:
    print(data['url'], data['url_name'], data['start'])

