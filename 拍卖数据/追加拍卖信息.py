import re
import time

import requests
from lxml import etree
from openpyxl import load_workbook

# 加载现有的Excel文件
wb = load_workbook('上海公拍网2.xlsx')

# 选择工作表
ws = wb.active  # 或者使用 wb.get_sheet_by_name('Sheet1') 如果你知道工作表的名称
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'Hm_lvt_263a15f1b2e57ebc22960d3fa7c5537e=1730077707; HMACCOUNT=FDD970C8B3C27398; ASPSESSIONIDAADTTRAQ=FPECAKGDCMKFJNBOPEEHHJBE; SF_cookie_67=18454395; dLwyZZHe134zS=60meDGmkLZnngmeIgHC31_S6EgC2MwM0ER9R.MSEePl6bbUJw5oWhrqZz6tVn3SQzZ9QaPbIw8TwY7fE8Wcx7Z8A; SF_cookie_8=27902555; HMF_CI=44bb12c2e90066964c919688ad52681efa202a9be20bf27acaa80d15d25f6132921721e8dcb68d7fd4b8977fcc91461ed789fe290c29d8fdaf2b4c2b9d372b5a6e; FECW=129062a52080fa364b664b2ce8aaadb5facd226ae9b41b405a519c17eb14e2fca831bd1c17c032322362715b657f4803a5f21c70acb66608539caaacc28cb0205d17e90187867435f828a63af51c23c924; HMY_JC=53caad8322c0473b5438d616cda2cb32c908ac6a4c6a6c47a8f4960451f8880f36,; HBB_HC=2a9e762744a58a1681b967af8a10b2dcae5872f23ab37961c85ec01ff8f10e661bfaa0aa26c340f60f6075cbbfc1a44690; Hm_lpvt_263a15f1b2e57ebc22960d3fa7c5537e=1730078170; dLwyZZHe134zT=0GpirNb.a6PzyJmZ2qkEjx_sgDCVhhdC4tXOYHEH0OMH2A3DuGHB0fs2Sds_wgoG8fEy6Bf03vzl40X4T4Qsi5LyAuvKhtP1.ThgNo6ddIvlLiastRwuPi4nouXd4OMrj99owxQYXNCOSJTaboGWD.lwJIjPwzzERFFRPUNxwb5Z4goV16IxEmYmx.qdUKloudxz_TOL07YuZu9Vj6nX.QIg1wWWZneApdxXeb2_uHJawc_4pWJ1Vu_KLTOmbOEe5XVFQlXIuqaapbtoJwsjrpR2OfZghmtuBbHc2xQgAv3PS.bQ0N.O.B8Jm0efHyA.KwC5RwqFSY8Gd4fAUfbVYdvN4nQXxen93KrZ5njml8gZ; FECA=eqsYOEg4Gk4cmla6h4pQkUQcwFWtxl/k9JrZmR8241PxQYKvt8bZKeLq9O2cuBUJpkFtjNE4+8YBAP3ar3wRwNwrtKkhuWuZ4WngrTooK+rhtTJsuAh+sbnAt2CBr+3jGDv2/hnPgmGC+eCjXJdYYgAgdd7EBa8B/ihCe32zgdjBxRTsJjY5Y8GIM/NSRRXJob; C3VK=f97621',
    'Pragma': 'no-cache',
    'Referer': 'https://s.gpai.net/sf/search.do?q=&pr=447&restate=1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}
xlsx_data = []

response = requests.get('https://s.gpai.net/sf/search.do?q=&pr=447&restate=1', headers=headers)
auction_data = response.content.decode()
html = etree.HTML(auction_data)
# 获取所有数据
overall_data = html.xpath("//div[@class='block-wrap notice-wrap'][1]//ul[@class='main-col-list clearfix']/li/div[@class='list-item']")
for data in overall_data:
    title = "".join(data.xpath(".//div[@class='item-tit']/a/text()"))
    title_url = "https:" + "".join(data.xpath(".//div[@class='item-tit']/a/@href"))
    starting_bid = "".join(data.xpath(".//p[2]//text()")).strip()
    appraisal_price = "".join(data.xpath(".//p[3]//text()")).strip()
    time_date = "".join(data.xpath(".//p[4]//text()")).strip()
    auction_status = "".join(data.xpath(".//span[contains(@class, 'badge-icon')]/text()"))
    if '预计结束' in time_date:
        expected_end = time_date.split('预计结束：')[1]
    elif '开始时间' in time_date:
        start_time = time_date.split('开始时间：')[1]
    elif '结束时间' in time_date:
        end_time = time_date.split('结束时间：')[1]
    if 'expected_end' not in globals():
        expected_end = ''
    if 'start_time' not in globals():
        start_time = ''
    if 'end_time' not in globals():
        end_time = ''
    if '万元' in appraisal_price:
        appraisal_price_num = re.findall(r'评估价：(.*?)万元', appraisal_price)[0]
        appraisal_price_num = float(appraisal_price_num) * 10000
    else:
        appraisal_price_num = re.findall(r'评估价：(.*?)元', appraisal_price)[0]
    if '万元' in starting_bid:
        starting_bid_num = re.findall(r'起拍价：(.*?)万元', starting_bid)[0]
        starting_bid_num = float(starting_bid_num) * 10000
    else:

        try:
            starting_bid_num = re.findall(r'[\d.]+', starting_bid)[0]
        except:
            print(starting_bid)
            break
    if float(starting_bid_num) >= 300000000:
        print(title, title_url, starting_bid, appraisal_price, time_date, auction_status)
        xlsx_data.append([title, title_url, starting_bid_num, appraisal_price_num, start_time, end_time, expected_end, auction_status])
time.sleep(2)

# 如果你要在已有数据的行后面添加新的行，可以这样做：
for data in xlsx_data:
    ws.append(data)

# 保存更改
wb.save('上海公拍网2.xlsx')