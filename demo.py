import os

import requests
from fontTools.ttLib import TTFont
from lxml import etree
import re

import requests

cookies = {
    'JSESSIONID': '43EFB4E145C2A3156620F46911CDBF08',
    '__FT10000056': '2024-8-30-17-3-57',
    '__NRU10000056': '1725008637552',
    'spjc': '44061709',
    '__REC10000056': '1',
    '__RT10000056': '2024-9-4-17-10-49',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': 'JSESSIONID=43EFB4E145C2A3156620F46911CDBF08; __FT10000056=2024-8-30-17-3-57; __NRU10000056=1725008637552; spjc=44061709; __REC10000056=1; __RT10000056=2024-9-4-17-10-49',
    'Origin': 'https://spjc.mwr.gov.cn',
    'Pragma': 'no-cache',
    'Referer': 'https://spjc.mwr.gov.cn/spjc/hallg/results.jsp?mindex=4',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

woff_headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'JSESSIONID=43EFB4E145C2A3156620F46911CDBF08; __FT10000056=2024-8-30-17-3-57; __NRU10000056=1725008637552; spjc=44061709; __REC10000056=1; __RT10000056=2024-9-4-17-10-49',
    'Pragma': 'no-cache',
    'Referer': 'https://spjc.mwr.gov.cn/spjc/hallg/results.jsp?mindex=4',
    'Sec-Fetch-Dest': 'font',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

data = {
    'PAGE': 'p1',
    'RS': '10',
}

response = requests.post(
    'https://spjc.mwr.gov.cn/spjc/spjc/OTMtriar/OTMyalma!wjhXrMastseXrJasb.do',
    headers=headers,
    data=data,
)

res = response.json()

res_data = res['data']
woff_name = ''
for item in res_data:
    woff_data = item['WCODE']
    woff_name = re.findall(r'#(.*?)otltag', woff_data)[0]
    break

if woff_name:
    # https://spjc.mwr.gov.cn/spjc/hallg/ttf/klHTxQ9B60_1725500283709.woff
    ttf_url = 'https://spjc.mwr.gov.cn/spjc/hallg/ttf/' + woff_name + ".woff"
    ttf_response = requests.get(url=ttf_url, headers=woff_headers)
    if os.path.exists("shuili1.ttf"):
        os.remove("shuili1.ttf")
    with open('shuili1.ttf', 'wb') as f:
        f.write(ttf_response.content)
    font_file = TTFont('shuili1.ttf')
    font_list = font_file.getGlyphOrder()
    for value in font_list:
        try:
            # 字形名称
            glyph_name = value
            # 提取Unicode编码
            unicode_code = int(glyph_name[3:], 16)  # 从第4个字符开始取，转换为十六进制数
            # 将编码转换为字符
            character = chr(unicode_code)
            print("对应的汉字是:", character)
        except:
            pass

