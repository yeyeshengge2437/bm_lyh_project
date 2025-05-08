import requests

headers = {
    'Content-Type': 'application/json',
}

json_data = {
    'model': 'deepseek-r1:14b',
    'prompt': '请介绍一下自己？',
    'stream': False,
}

response = requests.post('http://10.20.151.182:11434/api/generate', headers=headers, json=json_data)
