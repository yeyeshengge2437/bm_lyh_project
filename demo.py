import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Content-Type': 'application/json'}


url = 'http://yapi.fadox.cn/mock/67/v1/login/login'
data = {
    "name": "liyongheng",
    "password": "123456"
}
response = requests.post(url, headers=headers, json=data)
print(response.json())