import time
from datetime import datetime
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat, judging_bm_criteria
import mysql.connector
import requests
from lxml import etree


paper = "中国纪检监察报"
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': '_trs_uv=m1n0z125_4878_bybu; HMF_CI=b51b612efcab0fb27c3cf129d01b6f576d0c929838ef33795b2a3248fab5cf3237ef343d0a656219569221d9889767da80671c1052806a443aae5a45b359153801; HMY_JC=f6f9f9e6a776ad6dd02c5f174cc16239c12b1284c52b1b70ba92b6e29abf042b99,; _trs_ua_s_1=m38eku50_4878_gp9q; HBB_HC=2fb6398e78d26d4b706c0faf01fbc63721f86a2f053bb16556f753954d8ba4e8708b940ee59f108da3033049bef438097a',
    'Origin': 'https://jjjcb.ccdi.gov.cn',
    'Pragma': 'no-cache',
    'Referer': 'https://jjjcb.ccdi.gov.cn/epaper/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

cookies = {
    '_trs_uv': 'm1n0z125_4878_bybu',
    'HMF_CI': 'b51b612efcab0fb27c3cf129d01b6f576d0c929838ef33795b2a3248fab5cf3237ef343d0a656219569221d9889767da80671c1052806a443aae5a45b359153801',
    'HMY_JC': 'f6f9f9e6a776ad6dd02c5f174cc16239c12b1284c52b1b70ba92b6e29abf042b99,',
    '_trs_ua_s_1': 'm38eku50_4878_gp9q',
    'HBB_HC': '2fb6398e78d26d4b706c0faf01fbc63721f86a2f053bb16556f753954d8ba4e8708b940ee59f108da3033049bef438097a',
}

def get_chuxiong_paper(paper_time, queue_id, webpage_id):
    # 将today的格式进行改变
    day = paper_time
    paper_time = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%Y/%m/%d')
    for i in range(1, 8 + 1):
        data = f'bc={i}&docpubtime={paper_time}'
        base_url = f'https://jjjcb.ccdi.gov.cn/reader/layout/getBmDetail.do'
        url = base_url
        response = requests.get(url, headers=headers, cookies=cookies, data=data)
        # if response.status_code == 200:
        content = response.content
        print(content)
        return




get_chuxiong_paper('2024-08-22', 111, 1111)
