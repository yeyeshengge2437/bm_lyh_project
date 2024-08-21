import requests
from lxml import etree
today = '2024-08-15'
def get_date_num(date):
    year = date.split('-')[0]
    month = date.split('-')[1]
    day_num = date.split('-')[2]
    day_num = int(day_num)
    headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://gsdbs.baozhanmei.net',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'nian': year,
        'yue': month,
    }

    response = requests.post('https://gsdbs.baozhanmei.net/list_news/datebd/1110', headers=headers, data=data)
    data = response.content.decode()
    html = etree.HTML(data)
    date_a = {}
    # 获取所有li标签下的内容
    list_li = html.xpath('//li')
    for li in list_li:
        # 判断li下否有a标签
        li_a = ''.join(li.xpath('./a/@href'))
        li_num = ''.join(li.xpath('.//text()'))
        # 构建字典
        date_a[li_num] = li_a
    if date_a[str(day_num)]:
        return date_a[str(day_num)]
    else:
        return False







