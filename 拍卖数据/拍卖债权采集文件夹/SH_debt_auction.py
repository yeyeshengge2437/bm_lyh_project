import time
from datetime import datetime
from api_paimai import judge_repeat
from a_mysql_connection_pool import get_connection
import requests
import json


def get_shanghai_debt_auction(from_queue):
    cookies = {
        'pids': '5994603',
        'Hm_lvt_263a15f1b2e57ebc22960d3fa7c5537e': '1742349542,1742785191',
        'HMACCOUNT': 'FDD970C8B3C27398',
        'HWWAFSESTIME': '1742785201457',
        'HWWAFSESID': 'a69c173ba6d111fb8a',
        'Hm_lpvt_263a15f1b2e57ebc22960d3fa7c5537e': '1742785200',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Referer': 'https://zc.gpai.net/zc/zc_auction?productIndex=4',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        # 'Cookie': 'pids=5994603; Hm_lvt_263a15f1b2e57ebc22960d3fa7c5537e=1742349542,1742785191; HMACCOUNT=FDD970C8B3C27398; HWWAFSESTIME=1742785201457; HWWAFSESID=a69c173ba6d111fb8a; Hm_lpvt_263a15f1b2e57ebc22960d3fa7c5537e=1742785200',
    }

    params = {
        'info': '{"channelId":43,"itemType":4,"auctionModeList":null,"assetClass":null,"minPrice":"","maxPrice":"",'
                '"pageNumber":1,"pageSize":10}',
    }

    response = requests.get('https://zc.gpai.net/zc/api/item/list', params=params, headers=headers)
    data_count = response.json()["data"]["pageCount"]
    page_num = data_count // 200 + 1
    for num in range(1, page_num + 1):
        info_data = {
            "channelId": 43,
            "itemType": 4,
            "auctionModeList": None,
            "assetClass": None,
            "minPrice": "",
            "maxPrice": "",
            "pageNumber": num,  # 动态赋值
            "pageSize": 200
        }
        params = {
            'info': json.dumps(info_data, ensure_ascii=False)  # 序列化为JSON字符串
        }
        response = requests.get('https://zc.gpai.net/zc/api/item/list', params=params, headers=headers)
        value_list = response.json()["data"]["list"]
        time.sleep(2)
        for value in value_list:
            value_id = value["id"]
            auction_id = value['auctionId']
            url = f'https://zc.gpai.net/zc/detail?id={value_id}'
            state, id = judge_repeat(url)
            if state:
                continue
            title = value["itemName"]
            state = value["value"]
            # if state != '已成交' or state != '流标':
            #     continue
            start_time = value["beginTime"]
            end_time = value["endTime"]
            start_bid = value["startPrice"]  # 起拍价
            sold_price = value["finalPrice"]   # 成交价
            subject_annex = ''
            subject = value["itemPicture"]   # 项目图片
            subject_list = subject.split('|')
            for subject_ in subject_list:
                subject_ = subject_.split('?')[0]
                subject_annex += subject_ + ','
            # print(f'链接:{url}, 标题：{title}, 状态：{state}, 开始时间：{start_time}, 结束时间：{end_time}, 成交价：{sold_price}, 附件：{subject_annex}')
            json_data = {
                'id': auction_id,
            }
            # print(json_data)
            try:
                response_announcement = requests.post('https://zc.gpai.net/zc/api/auction/info', headers=headers, json=json_data)
                announcement_json = response_announcement.json()
            except:
                continue
            # print(announcement_json)
            try:
                auction_html = announcement_json["data"]["noticeContent"]  # 公告html
            except:
                auction_html = ''
            params = {
                "info": f'{{"id":"{value_id}"}}'  # 双外层{}需转义为单{}
            }
            try:
                response_detail = requests.get(
                    f'https://zc.gpai.net/zc/api/item/item', params,
                    headers=headers
                )
            except:
                continue
            value_detail = response_detail.json()
            annex_list = value_detail["data"]["item"]["itemAccessory"]  # 附件列表
            subject_info = value_detail["data"]["itemDescribe"]  # 标的信息
            if annex_list:
                annex_list = json.loads(annex_list)
                for annex in annex_list:
                    print(annex)
                    annex_url = annex["url"]
                    subject_annex += annex_url + ','
            address = value_detail["data"]["item"]["addressDetail"]    # 位置
            disposal_unit = value_detail["data"]["company"]["name"]    # 处置单位
            params = {
                "info": f"{{\"id\":\"{value_id}\",\"pageNumber\":1,\"pageSize\":200}}"
            }
            try:
                res_record = requests.get(
                    "https://zc.gpai.net/zc/api/item/bidRecord", params=params,
                    headers=headers
                )
            except:
                continue
            response_record = res_record.json()
            auction_history = ''
            people_num = 0
            if response_record.get('data'):
                if response_record.get('data').get('realData'):
                    response_record_ = response_record.get('data').get('realData')
                    state_record = response_record_.get('value')
                    bid_num = response_record_.get('currentLicenseKey')   # 竞价号牌
                    bidding_price = response_record_.get('currentPrice')  # 竞价价格
                    time_record = response_record_.get('endTime')   # 竞价时间
                    auction_history += f'状态：{state_record}, 竞价号牌：{bid_num}, 竞价价格：{bidding_price}, 竞价时间：{time_record}'
                if response_record.get('data').get('list'):
                    peo_num = set()
                    record_list = response_record.get('data').get('list')
                    for record in record_list:
                        peo_num.add(record.get('licenseKey'))
                    people_num += len(peo_num)
                    auction_history += f'参与人数：{len(peo_num)}'
            value_dict = {
                "链接": url,
                "标题": title,
                "状态": state,
                "地址": address,
                "起拍价": start_bid,
                "成交价": sold_price,
                "拍卖结果": state,
                "结束时间": end_time,
                "处置单位": disposal_unit,
                "竞价记录": auction_history,
                "报名人数": people_num,
                "附件以及图片": subject_annex,
                "拍卖公告": auction_html,
                "标的信息": subject_info,
            }
            subject_annex_up = subject_annex
            create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            create_date = datetime.now().strftime('%Y-%m-%d')
            # 上传到测试数据库
            conn_test = get_connection()

            cursor_test = conn_test.cursor()
            # 上传文件
            update_sql = "INSERT INTO col_judicial_auctions (url, title, state, address, start_bid, sold_price, outcome, end_time, auction_html, subject_annex_up, subject_info, disposal_unit, auction_history, people_num, subject_annex, from_queue, create_time, create_date, start_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            cursor_test.execute(update_sql,
                                (url, title, state, address, start_bid, sold_price,
                                 state,
                                 end_time,
                                 auction_html, subject_annex_up, subject_info,
                                 disposal_unit,
                                 auction_history, people_num, subject_annex,
                                 from_queue, create_time, create_date, start_time))
            conn_test.commit()

            cursor_test.close()
            conn_test.close()
            print(value_dict)


get_shanghai_debt_auction(6789)





