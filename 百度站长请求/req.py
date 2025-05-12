import requests

headers = {
    'Content-Type': 'text/plain',
}

with open('zsy_url.txt', 'rb') as f:
    data = f.read()

response = requests.post(
    'http://data.zz.baidu.com/urls?site=https://www.debtop.com&token=Wm74GQabAkNQOOyh',
    headers=headers,
    data=data,
)
print(response.text)
