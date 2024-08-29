from datetime import datetime

import mysql.connector
import requests
from DrissionPage import ChromiumPage, ChromiumOptions
import redis
from lxml import etree

# 连接redis数据库
redis_conn = redis.Redis()

co = ChromiumOptions()

co = co.set_paths(local_port=9121)
co = co.set_argument('--no-sandbox')  # 关闭沙箱模式, 解决`$DISPLAY`报错
co = co.headless(True)
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'https://dkjgfw.mnr.gov.cn',
    'Pragma': 'no-cache',
    'Referer': 'https://dkjgfw.mnr.gov.cn/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


def get_quanguoyichangminglu_data():
    json_data = {
        'dwGuid': None,
    }

    abnormal_response = requests.post(
        'https://dkjgfw.mnr.gov.cn/dks-webapi/site/DzkcAbnormalList/listNoLand',
        headers=headers,
        json=json_data,
    )
    all_datas = abnormal_response.json()
    if all_datas["succeed"] == "yes":
        for data in all_datas["result"]:
            target_url = f'https://dkjgfw.mnr.gov.cn/#/detail/dwxxxq/2/1/{data["dwGuid"]}/{data["dwUnifiedCode"]}/ycml'
            # 行业监督信息---------------------------------
            json_data = {
                'dwGuid': data["dwGuid"],
            }
            abnormal_response = requests.post(
                'https://dkjgfw.mnr.gov.cn/dks-webapi/site/DzkcAbnormalList/listNoLand',
                headers=headers,
                json=json_data,
            )
            vision_info = abnormal_response.json()
            if vision_info["result"]:
                for vision in vision_info["result"]:
                    name = vision["dwUnitName"]
                    abnormalReason = vision["abnormalReason"]  # 认定依据
                    abnormalRecDept = vision["abnormalRecDept"]  # 认定部门
                    abnormalDate = vision["abnormalDate"]  # 认定日期
                    unAbnormalDate = vision['unAbnormalDate']  # 移出日期
                    # 将时间戳转化为年月日格式
                    abnormalDate = datetime.fromtimestamp(int(abnormalDate) / 1000).strftime('%Y-%m-%d')
                    print(name, abnormalReason, abnormalRecDept, abnormalDate, unAbnormalDate)
            else:
                print('无行业监督信息')

            # 地勘活动情况
            json_data = {
                'dwBodytypeCodes': [],
                'dwGuid': data["dwGuid"],
                'dwOperstateCodes': [],
                'dwRegionCode': '',
                'manageTypes': [],
                'moneyTypes': [],
                'projectTypes': [],
                'searchValue': '',
            }

            dikan_response = requests.post('https://dkjgfw.mnr.gov.cn/dks-webapi/site/listDzkcResult', headers=headers,
                                     json=json_data)
            dikan_info = dikan_response.json()
            if dikan_info["result"]:
                for dikan in dikan_info["result"]:
                    projectName = dikan["projectName"]  # 项目名称
                    projectCityName = dikan["projectCityName"]  # 项目工作区域
                    qualitylevel = dikan["qualitylevel"]  # 项目状态
                    mainPersons = dikan["mainPersons"]  # 项目负责人
                    print(projectName, projectCityName, qualitylevel, mainPersons)
            else:
                print("没有地勘活动情况")
            # 中标信息--------------------------
            json_data = {
                'dwBodytypeCodes': [],
                'dwGuid': data["dwGuid"],
                'dwOperstateCodes': [],
                'dwRegionCode': '',
                'manageTypes': [],
                'moneyTypes': [],
                'projectTypes': [],
                'searchValue': '',
            }

            win_response = requests.post('https://dkjgfw.mnr.gov.cn/dks-webapi/site/listDzkcWinBidPub', headers=headers,
                                     json=json_data)
            win_info = win_response.json()
            if win_info["result"]:
                for win in win_info["result"]:
                    projectName = win["projectName"]  # 中标项目名称
                    projectCityName = win["projectCityName"]  # 中标项目工作区域
                    winBidMoney = win["winBidMoney"]  # 中标金额（万元）
                    if winBidMoney:
                        winBidMoney = int(winBidMoney) * 10000
                    winBidDate = win["winBidDate"]  # 中标日期
                    winBidDate = datetime.fromtimestamp(int(winBidDate) / 1000).strftime('%Y-%m-%d')
                    print(projectName, projectCityName, winBidMoney, winBidDate)
            else:
                print("没有中标信息")

            # 单位基本信息
            url = f'https://dkjgfw.mnr.gov.cn/dks-webapi/site/readBasicInforPub/{data["dwGuid"]}'
            jiben_response = requests.get(
                url,
                headers=headers,
            )
            jiben_info = jiben_response.json()
            if jiben_info["result"]:
                for jiben in jiben_info["result"]:
                    try:
                        dwUnitName = jiben["dwUnitName"]  # 单位名称
                        dwResponsiblePerson = jiben["dwResponsiblePerson"]  # 法定代表人
                        dwPreparer = jiben["dwPreparer"]  # 单位联系人
                        dwFax = jiben["dwFax"]  # 单位电话
                        dwRegionName = jiben["dwRegionName"]  # 所在地区
                        dwAddress = jiben["dwAddress"]  # 单位地址
                        personDkTechH = jiben["personDkTechH"]  # 高级技术人
                        personDkTechS = jiben["personDkTechS"]  # 中级技术人
                        dwUnitIntro = jiben["dwUnitIntro"]  # 单位简介
                        print(dwUnitName, dwResponsiblePerson, dwPreparer, dwFax, dwRegionName, dwAddress, personDkTechH,)
                    except:
                        continue
            else:
                print("没有单位基本信息")

            # 资质信息--------------------------------------
            json_data = {
                'dwBodytypeCodes': [],
                'dwGuid': data["dwGuid"],
                'dwOperstateCodes': [],
                'dwRegionCode': '',
                'manageTypes': [],
                'moneyTypes': [],
                'projectTypes': [],
                'searchValue': '',
            }

            zizhi_response = requests.post('https://dkjgfw.mnr.gov.cn/dks-webapi/site/listCertInforPub', headers=headers,
                                     json=json_data)
            zizhi_info = zizhi_response.json()
            if zizhi_info["result"]:
                for zizhi in zizhi_info["result"]:
                    certName = zizhi["certName"]  # 资质名称
                    certNo = zizhi["certNo"]  # 资质编号
                    certLevel = zizhi["certLevel"]  # 资质等级
                    startDate = datetime.fromtimestamp(int(zizhi["startDate"]) / 1000).strftime('%Y-%m-%d')  # 发证日期
                    endDate = datetime.fromtimestamp(int(zizhi["endDate"]) / 1000).strftime('%Y-%m-%d')  # 到期日期
                    print(certName, certNo, certLevel, startDate, endDate)
            else:
                print("没有资质信息")


            # 变更信息
            json_data = {
                'dwBodytypeCodes': [],
                'dwGuid': data["dwGuid"],
                'dwOperstateCodes': [],
                'dwRegionCode': '',
                'manageTypes': [],
                'moneyTypes': [],
                'projectTypes': [],
                'searchValue': '',
            }

            change_response = requests.post('https://dkjgfw.mnr.gov.cn/dks-webapi/site/listChangeRecordrPub', headers=headers,
                                     json=json_data)
            change_info = change_response.json()
            if change_info["result"]:
                for change in change_info["result"]:
                    changeDate = datetime.fromtimestamp(int(change["changeDate"]) / 1000).strftime('%Y-%m-%d') # 变更日期
                    changeContent = change["changeContent"]  # 变更内容
                    changeAfter = change["changeAfter"]  # 变更前内容
                    changeBefore = change["changeBefore"]  # 变更后内容
                    print(changeDate, changeContent, changeAfter, changeBefore)
            else:
                print("没有变更信息")




get_quanguoyichangminglu_data()
