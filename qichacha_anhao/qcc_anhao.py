import time
from lxml import etree
from DrissionPage import ChromiumPage, ChromiumOptions


# co = ChromiumOptions()
# co = co.set_argument('--no-sandbox')
# co = co.headless()
# co.set_paths(local_port=9136)





co = ChromiumOptions()
co = co.set_user_data_path(r'D:\chome_data\data_one')
co.set_paths(local_port=9136)
def get_anhao(anhao_set, html):
    tree = etree.HTML(html)
    anhao_list = tree.xpath("//tr/td[2]")
    for anhao in anhao_list:
        anhao_name = ''.join(anhao.xpath(".//text()"))
        if len(anhao_name) < 7:
            break
        anhao_set.add(anhao_name)
    print(anhao_set)
# 连接浏览器
page = ChromiumPage(co)
tab = page.get_tab()
# 访问网页
tab.get('https://www.qcc.com/')
# time.sleep(3)
search_name = tab.ele("xpath=//input[@id='searchKey']")
search_name.click()
time.sleep(1)
search_name.input('金川集团股份有限公司')
# 搜索按键点击
tab.ele("xpath=//span[@class='input-group-btn']/button[@class='btn btn-primary']").click(by_js=True)
time.sleep(2)
# 获取公司列表
company_list = tab.eles("xpath=//div[@class='search-cell']//tr")
# 点击第一个公司
# tab.ele("xpath=//div[@class='search-cell']//tr[1]//a[@class='title copy-value']").click(by_js=True)
# 获取公司链接
company_url = tab.ele("xpath=//div[@class='search-cell']//tr[1]//a[@class='title copy-value']").attr('href')
new_tab = page.new_tab()
new_tab.get(company_url)
new_tab.ele('法律诉讼').click(by_js=True)
# 创建一个案号集合
anhao_set = set()
# ----------------立案信息案号-------------------
print("----------------开庭公告案号-------------------")
lian_list_html = new_tab.ele("xpath=//section[@id='lianlist']//table[@class='ntable app-ntable-expand-all']").html
# print(lian_list_html)
get_anhao(anhao_set, lian_list_html)
# 判断是否有下一页元素
target_list = new_tab.eles("xpath=//section[@id='lianlist']//ul[@class='pagination']//a")
while True:
    if target_list[-1].text == '>':
        target_list[-1].click(by_js=True)
        time.sleep(2)
        lian_list_html = new_tab.ele(
            "xpath=//section[@id='lianlist']//table[@class='ntable app-ntable-expand-all']").html
        if "无数据" in lian_list_html:
            break
        # print(lian_list_html)
        get_anhao(anhao_set, lian_list_html)
    else:
        break
# ----------------开庭公告案号-------------------
print("----------------开庭公告案号-------------------")
notice_list_html = new_tab.ele("xpath=//section[@id='noticelist']//table[@class='ntable app-ntable-expand-all']").html
# print(notice_list_html)
get_anhao(anhao_set, notice_list_html)
# 判断是否有下一页元素
target_list = new_tab.eles("xpath=//section[@id='noticelist']//ul[@class='pagination']//a")
while True:
    if target_list[-1].text == '>':
        target_list[-1].click(by_js=True)
        time.sleep(2)
        notice_list_html = new_tab.ele(
            "xpath=//section[@id='noticelist']//table[@class='ntable app-ntable-expand-all']").html
        if "无数据" in notice_list_html:
            break
        # print(notice_list_html)
        get_anhao(anhao_set, notice_list_html)
    else:
        break
# ----------------法院公告案号-------------------
print("----------------法院公告案号-------------------")
gonggao_list_html = new_tab.ele("xpath=//section[@id='gonggaolist']//table[@class='ntable app-ntable-expand-all']").html
# print(gonggao_list_html)
get_anhao(anhao_set, gonggao_list_html)
# 判断是否有下一页元素
target_list = new_tab.eles("xpath=//section[@id='gonggaolist']//ul[@class='pagination']//a")
while True:
    if target_list[-1].text == '>':
        target_list[-1].click(by_js=True)
        time.sleep(2)
        gonggao_list_html = new_tab.ele(
            "xpath=//section[@id='gonggaolist']//table[@class='ntable app-ntable-expand-all']").html
        if "无数据" in gonggao_list_html:
            break
        if not gonggao_list_html:
            break
        # print(gonggao_list_html)
        get_anhao(anhao_set, gonggao_list_html)
    else:
        break
print(anhao_set)
time.sleep(2)
input("---------------")
page.quit()
