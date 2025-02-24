import requests

cookies = {
    'JSESSIONID': 'DB83888F750EB45DC51B4D7D949FA945',
    '__51uvsct__3IzgAZJGzpMWGYLN': '1',
    '__51vcke__3IzgAZJGzpMWGYLN': '1a02177c-3072-5fdb-ab89-7e6c4dc7f8f9',
    '__51vuft__3IzgAZJGzpMWGYLN': '1740016677201',
    '__vtins__3IzgAZJGzpMWGYLN': '%7B%22sid%22%3A%20%22951b192b-c0d7-5e0e-917b-755001b6209c%22%2C%20%22vd%22%3A%206%2C%20%22stt%22%3A%20355643%2C%20%22dr%22%3A%204741%2C%20%22expires%22%3A%201740018832842%2C%20%22ct%22%3A%201740017032842%7D',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'http://www.qhcqjy.com',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://www.qhcqjy.com/info.do',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    # 'Cookie': 'JSESSIONID=DB83888F750EB45DC51B4D7D949FA945; __51uvsct__3IzgAZJGzpMWGYLN=1; __51vcke__3IzgAZJGzpMWGYLN=1a02177c-3072-5fdb-ab89-7e6c4dc7f8f9; __51vuft__3IzgAZJGzpMWGYLN=1740016677201; __vtins__3IzgAZJGzpMWGYLN=%7B%22sid%22%3A%20%22951b192b-c0d7-5e0e-917b-755001b6209c%22%2C%20%22vd%22%3A%206%2C%20%22stt%22%3A%20355643%2C%20%22dr%22%3A%204741%2C%20%22expires%22%3A%201740018832842%2C%20%22ct%22%3A%201740017032842%7D',
}

data = {
    'checkType': '',
    'para': 'search',
    'id': '',
    'classCode': '',
    'type': '',
    'searchType': 'item',
    'searchKeys': 'ծȨ',
}

response = requests.post('http://www.qhcqjy.com/info.do', headers=headers, data=data, verify=False)
print(response.text)