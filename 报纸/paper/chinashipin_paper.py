import re

import requests
from lxml import etree
from DrissionPage import ChromiumPage, ChromiumOptions
co = ChromiumOptions()
co = co.set_paths(local_port=9249)
co = co.set_argument('--no-sandbox')  # 关闭沙箱模式, 解决`$DISPLAY`报错
co = co.headless(True)  # 开启无头模式, 解决`浏览器无法连接`报错
def get_paper_url_cookies(url):
    cookie_dict = {}
    page = ChromiumPage(co)
    page.get(url)
    value_cookies = page.cookies()
    for key in value_cookies:
        cookie_dict[key['name']] = key['value']
    page.close()
    return cookie_dict
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'showSite=false; Hm_lvt_17eda52a3d3058c30393dc2b9451760b=1728548160,1728958789,1730790102; HMACCOUNT=FDD970C8B3C27398; Hm_lpvt_17eda52a3d3058c30393dc2b9451760b=1730884536',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

params = {
    'qdate': '2024-08-14',
    'index': '0',
}
# cookies = get_paper_url_cookies('https://www.cnfood.cn/electronic')
response = requests.get('https://www.cnfood.cn/electronic', params=params, headers=headers)
html = response.content.decode('utf-8')
data_html = re.findall(r'list:(.*)}],extra:aK}', html)[0]
data_html = re.sub(r'\\u002F', '/', data_html)
article_list = re.findall(r'title:"(.*?)",href:"(.*?)",width', data_html)
for article in article_list:
    article_name, article_url = article
    # print(article_name, article_url)
    article_response = requests.get(article_url, params=params, headers=headers)
    article_html = article_response.content.decode('utf-8')
    print(article_html)
    article_list = re.findall(r'config:\{}}}(.*)\);</script>', article_html)[0]
    article_list = article_list.split(',')
    max_num = 0
    for article in article_list:
        if len(article) > max_num:
            max_num = len(article)
            index_list = article_list.index(article)
    html = article_list[index_list]
    html = re.sub(r'\\u003C', '<', html)
    html = re.sub(r'\\u003E', '>', html)
    html = re.sub(r'\\u002F', '/', html)
    html = re.sub(r'\\u3000', '', html)
    html = re.sub(r'&nbsp;', ' ', html)
    html = etree.HTML(html)
    content = ''.join(html.xpath('//text()'))
    print(content)
    # break




