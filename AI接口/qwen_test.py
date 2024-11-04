import requests
import json

# 服务器地址和端口
url = 'http://49.234.47.160:8000/v1/chat/completions'

# 设置请求头部
headers = {
    'Authorization': 'Bearer ggywxDKTdSsxMgJm2FHs2YXjpz7K_1vawU*obaGzpf8Gz1g_BynogsOH1apRX0qcdzyjCz$o1Bq30',
    'Content-Type': 'application/json'
}

# 设置请求数据
data = {
    "model": "qwen",
    "messages": [
        {
            "role": "user",
            "content": "你是谁？"
        }
    ],
    "stream": False
}

# 将数据转换为 JSON 格式
json_data = json.dumps(data)

# 发送 POST 请求
response = requests.post(url, headers=headers, data=json_data)

# 打印响应内容
print(response)
