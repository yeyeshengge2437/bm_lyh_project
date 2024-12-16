import json
import re

import requests
import time
from lxml import etree
from DrissionPage import ChromiumPage, ChromiumOptions

co = ChromiumOptions()
co = co.set_user_data_path(r"D:\chome_data\data_one")
co.set_paths(local_port=9136)


def get_paper_url_cookies(url):
    cookie_dict = {}
    page = ChromiumPage(co)
    page.get(url)
    input()
    value_cookies = page.cookies()
    for key in value_cookies:
        cookie_dict[key['name']] = key['value']
    page.quit()
    return cookie_dict


cookies = get_paper_url_cookies('https://www.qcc.com/')

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    # 'cookie': 'qcc_did=aa80c299-a44e-4b99-bd8f-846f1f237214; UM_distinctid=191db1e9c1327b0-0fff366dedf7e-26001151-13c680-191db1e9c14297d; QCCSESSID=5faed64b046ba10b284a5d20ed; tfstk=fPcn_NTwQvyBDkWgSdPBU4PJGZvTpwN730C827EyQlr1vMCKz7ro4lhLv2FFRAixu6hpd7CuO7NyDndvMy3QN78VqQ5CA5zuouR8Uk7FEiOJDndv6WQcsf-xvXMfON47byzza98g7yU7ayPz4Fqarr6PY0or7F4brT7FakRa_r47auozaF0ZaLbav0oI_HnnTn87veGa-JqlwlfoQf5YdouUj_-Ssyxz02rGa_rCKRQoS2KhGVFIMm4xvC5nm4ujURclbnqSsVlEUVsH4PMrv5rLgp7g9XgE38l2VTo0t02qTRbPg2gUf54ZgUBbXfqK4X2wks28_je4TAp6v8F3o0lIxafr0V3xORGkmGrSprNarbTVEu2P41BN3P01NSrhhT67LPagD91bdE9O3pAkSFXqhJz_8ILMST67LPagDFYG3nwU5yRA.; acw_tc=0a47308e17328482727786483e0043d5ef0bb5e05f8700c5a77be074758c38; CNZZDATA1254842228=1515781789-1725958102-https%253A%252F%252Fwww.zsamc.com%252F%7C1732849017',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'referer': 'https://www.qcc.com/web/search?key=%E9%87%91%E5%B7%9D%E9%9B%86%E5%9B%A2%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}

response = requests.get('https://www.qcc.com/firm/6a6a2bdfcfec0102221e27582488b71f.html', cookies=cookies,
                        headers=headers)
html = response.content.decode()
# print(html)
content_json = re.findall(r'<script>window.__INITIAL_STATE__=(.*);\(function\(\)\{var s;\(s=document.currentScript.*?;</script>', html)[0]
print(content_json)
content_json = json.loads(content_json)
# -------------主要人员----------------------
print("-------------------主要人员----------------------")
main_person = content_json["company"]["companyDetail"]["Employees"]
# print(main_person)
for key in main_person:
    print(key.get("Name"))
print("------------------法代--------------------------")
legal_person = content_json["company"]["companyDetail"]["Oper"]["Name"]
print(legal_person)
print("------------------股东信息--------------------------")
shareholder = content_json["company"]["companyDetail"]["Partners"]
for key in shareholder:
    print(key.get("StockName"))




