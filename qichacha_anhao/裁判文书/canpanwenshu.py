"""
裁判文书下载, https://wenshu.court.gov.cn/website/wenshu/181029CR4M5A62CH/index.html
"""
import re
import time
from lxml import etree
from DrissionPage import ChromiumPage, ChromiumOptions


co = ChromiumOptions()
co = co.set_user_data_path(r'D:\chome_data\data_one')
co.set_paths(local_port=9136)

# anhao_set = {'（2023）甘01民终7998号', '（2019）辽01执异461号', '（2016）甘民初91号', '（2017）甘03民终352号', '（2021）甘0802民初3216号', '（2018）甘0302民初3123号', '（2015）沪高民四（海）终字第99号', '（2019）甘03民终80号', '（2018）甘0302民初1181号', '（2016）甘0302民初2594号', '（2018）甘0302民初179号', '（2018）甘0302民初229号', '（2020）甘0302民初912号', '（2015）金中民一初字第14号', '（2022）甘03民终115号', '（2020）甘03民特1号', '（2023）甘0302民初866号', '（2019）甘0302民初308号', '（2017）甘0302民初80号', '（2023）甘0302民初723号', '（2020）甘民终132号', '（2019）桂0602民初167号', '（2021）沪7101民初1542号', '（2016）最高法民终254号', '（2023）甘03民终596号', '（2020）甘03执23号之五', '（2015）普民二（商）初字第951号', '（2017）甘0302民初2764号', '（2020）沪7101破172号', '（2021）甘0302民初281号', '（2015）普民二（商）初字第961号', '（2019）甘执83号', '（2018）甘03民终33号', '（2019）甘03民终67号', '（2021）甘0102民初14761号', '（2017）甘03民终312号', '（2017）沪0107执294号', '（2017）甘03民终216号', '（2016）陕民初31号', '（2016）沪02民特398号', '（2016）甘03民终309号', '（2024）甘01民终7331号', '（2012）兰法民二初字第95号', '（2018）甘0302民初444号', '（2021）甘0302民初2431号', '（2018）浙0102民初6515号', '（2021）甘03民终22号', '（2019）甘03民初28号', '（2016）甘民初37号', '（2020）甘0321民初2052号', '（2017）甘民终453号', '（2023）甘0302民初994号', '（2016）甘0302民初2475号', '（2020）甘01民初711号之一', '(2023)甘0123民初2513号'}
anhao_set = {'（2023）甘01民终7998号', '（2019）辽01执异461号', '（2016）甘民初91号', '（2017）甘03民终352号', '（2021）甘0802民初3216号', '（2018）甘0302民初3123号', '（2015）沪高民四（海）终字第99号', '（2019）甘03民终80号', '（2018）甘0302民初1181号', '（2016）甘0302民初2594号', '（2018）甘0302民初179号', '（2018）甘0302民初229号', '（2020）甘0302民初912号', '（2015）金中民一初字第14号', '（2022）甘03民终115号', '（2020）甘03民特1号', '（2023）甘0302民初866号', '（2019）甘0302民初308号',  '（2020）甘01民初711号之一', '(2023)甘0123民初2513号'}
# 连接浏览器
page = ChromiumPage()
tab = page.get_tab()
# 访问网页
tab.get('https://account.court.gov.cn/app?back_url=https%3A%2F%2Faccount.court.gov.cn%2Foauth%2Fauthorize%3Fresponse_type%3Dcode%26client_id%3Dzgcpwsw%26redirect_uri%3Dhttps%253A%252F%252Fwenshu.court.gov.cn%252FCallBackController%252FauthorizeCallBack%26state%3D421fc4a4-5cc2-4ecd-bb44-257b1a17ee98%26timestamp%3D1732779592364%26signature%3DA4C212AFA550EFA5E27D9A3E094A741A7A14BCE6873A632A4CF587CF76474838%26scope%3Duserinfo#/login')
# print(tab.html)
time.sleep(3)

login = tab.ele("@class=phone-number-input",).input('15938554242', by_js=True)
time.sleep(2)
# login.click(by_js=True)
# login
password = tab.ele("@class=password",).input('Liyongheng10!', by_js=True)
time.sleep(2)
# password.click(by_js=True)
# password
tab.ele("@class=button button-primary").click(by_js=True)
time.sleep(8)
tab.refresh()
# print(tab.html)
# tab.ele("@id=loginLi").click(by_js=True)
tab.ele("@class=searchKey search-inp").input("开始123", by_js=True)
time.sleep(1)
tab.ele("@class=search-rightBtn search-click").click(by_js=True)
time.sleep(7)
for anhao in anhao_set:
    # try:
    tab.ele("@class=searchKey search-inp").input(anhao, by_js=True)
    time.sleep(1)
    tab.ele("@class=search-rightBtn search-click").click(by_js=True)
    time.sleep(7)
    wen_html = tab.html
    # tab.back(1)
    # print(wen_html)
    print("----------------------------------------------------------")
    html = ""
    # 如果没有该案号信息，需处理一下数据
    htmls = tab.eles("@class=LM_list")
    for i in htmls:
        html += i.html
    if not html:
        tab.back(1)
        break
    # print(html)
    html = etree.HTML(html)
    wen_href = html.xpath("//a[@class='caseName']/@href")
    base_url = "https://wenshu.court.gov.cn/website/wenshu"
    for href in wen_href:
        href = ''.join(href)
        href = re.sub(r"\.\.", "", href)
        url = base_url + href
        print(anhao)
        print(url)
    tab.back(1)
    #     new_tab = page.new_tab()
    #     new_tab.get(url)
    #     time.sleep(2)
    #     wen_html = new_tab.html
    #     print(wen_html)
    # break



page.close()
