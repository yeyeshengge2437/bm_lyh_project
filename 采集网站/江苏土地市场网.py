import requests

cookies = {
    'server': '96F986AA9EEBFE5C768773CD182CF605',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    # 'Cookie': 'server=96F986AA9EEBFE5C768773CD182CF605',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://www.landjs.com/elasticSearch/goSearch/%E5%8D%97%E4%BA%AC%E8%B6%8A%E5%8D%9A%E7%94%B5%E9%A9%B1%E5%8A%A8%E7%B3%BB%E7%BB%9F%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
}
data = {
    'keyword': '南京',
    'index': '1',
    'size': '50',
    'type': '',
    'xzqDm': '',
}

response = requests.post(
    'http://www.landjs.com/elasticSearch/searchResult',
    # cookies=cookies,
    headers=headers,
    data=data,
    verify=False,
)

print(response.text)
