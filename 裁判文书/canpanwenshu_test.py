"""
裁判文书下载, https://wenshu.court.gov.cn/website/wenshu/181029CR4M5A62CH/index.html
"""
import base64
import random
import re
import time
import ddddocr
from lxml import etree
from lxml import html as html_import
from DrissionPage import ChromiumPage, ChromiumOptions
import tempfile
from a_mysql_connection_pool import up_instrument
from api_queue import paper_queue_next, paper_queue_success, paper_queue_fail


def initialize(iphone, password):
    ocr = ddddocr.DdddOcr(show_ad=False)
    co = ChromiumOptions()
    # co.set_argument('--incognito')
    # co = co.set_user_data_path(r"D:\chome_data\wenshu")
    co.set_paths(local_port=9247)

    # 连接浏览器
    page = ChromiumPage(co)
    tab = page.get_tab()

    return ocr, page, tab


def login(ocr, page, tab, iphone, password_str):
    taget_url = 'https://account.court.gov.cn/app?back_url=https%3A%2F%2Faccount.court.gov.cn%2Foauth%2Fauthorize%3Fresponse_type%3Dcode%26client_id%3Dzgcpwsw%26redirect_uri%3Dhttps%253A%252F%252Fwenshu.court.gov.cn%252FCallBackController%252FauthorizeCallBack%26state%3D421fc4a4-5cc2-4ecd-bb44-257b1a17ee98%26timestamp%3D1732779592364%26signature%3DA4C212AFA550EFA5E27D9A3E094A741A7A14BCE6873A632A4CF587CF76474838%26scope%3Duserinfo#/login'
    # 访问网页
    tab.get(taget_url)
    tab.wait.doc_loaded()
    time.sleep(3)
    tab.ele("@class=phone-number-input", ).input(iphone, clear=True)  # 1
    time.sleep(2)
    tab.ele("@class=password", ).input(password_str, clear=True)  # 1
    time.sleep(2)
    tab.ele("@class=captcha-img").click()  # 1
    time.sleep(8)
    image_captcha = tab.ele("xpath=//img[@class='captcha-img']")
    image_value = image_captcha.get_screenshot(as_base64=True)
    value_captcha = base64.b64decode(image_value)
    captcha = ocr.classification(value_captcha)
    captcha = captcha.lower()
    time.sleep(3)
    tab.ele("@class=answer").input(captcha, clear=True)
    time.sleep(4)
    tab.ele("@class=button button-primary").click()  # 1
    tab.wait.doc_loaded()
    time.sleep(4)
    # tab.refresh()
    # tab.wait.doc_loaded()
    time.sleep(10)
    tager_url_login = tab.url
    return tab, taget_url, tager_url_login, page


def search_instrument(tab, page, anhao, from_queue, webpage_id):
    # 先判断一下是否登录
    # try:
    login_text = tab.ele("@id=loginLi").text
    if "登录" in login_text:
        tab.ele("@class=searchKey search-inp").input("开始123")  # 1
        time.sleep(5)
        tab.ele("@class=search-rightBtn search-click").click()  # 1
        tab.wait.doc_loaded()
        time.sleep(7)
    # except:
    #     tab.refresh()
    #     tab.wait.doc_loaded()
    # try:
    tab.ele("@class=searchKey search-inp").input(anhao, clear=True)  # 1
    time.sleep(1)
    tab.ele("@class=search-rightBtn search-click").click()  # 1
    tab.wait.doc_loaded()
    time.sleep(7)
    print("----------------------------------------------------------")
    html = ""
    # 如果没有该案号信息，需处理一下数据
    htmls = tab.eles("@class=LM_list")
    for i in htmls:
        html += i.html
    if not html:
        tab.back(1)
        return
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
        new_tab = page.new_tab()
        new_tab.get(url)
        time.sleep(15)
        wen_html = new_tab.html
        content = new_tab.ele("@class=PDF_pox").text
        new_tab.close()
        # wen_html = del_script(wen_html)
        # wen_html = del_style(wen_html)
        # wen_html = del_link(wen_html)
        # wen_html = compress_html(wen_html)
        wen_html_tree = etree.HTML(wen_html)
        case_number_str = ''.join(wen_html_tree.xpath('//*[@id="iframedfah"]//text()'))  # 案号从输入项
        case_number = re.sub(r'">.*', '', case_number_str)
        wen_url = url
        title = ''.join(wen_html_tree.xpath("//div[@class='PDF_title']/text()"))
        court_str = ''.join(wen_html_tree.xpath("//h4[@class='clearfix'][1]//text()"))
        court = re.sub(r'审理法院：', '', court_str)
        case_type_str = ''.join(wen_html_tree.xpath("//h4[@class='clearfix'][2]//text()"))
        case_type = re.sub(r'案件类型：', '', case_type_str)
        cause_str = ''.join(wen_html_tree.xpath("//h4[@class='clearfix'][3]//text()"))
        cause = re.sub(r'案由：', '', cause_str)
        procedure_type_str = ''.join(wen_html_tree.xpath("//h4[@class='clearfix'][4]//text()"))
        procedure_type = re.sub(r'审理程序： ', '', procedure_type_str)
        judgment_date_str = ''.join(wen_html_tree.xpath("//h4[@class='clearfix'][5]//text()"))
        parties_str = ''.join(wen_html_tree.xpath("//h4[@class='clearfix'][6]//text()"))
        parties = re.sub(r'当事人：', '', parties_str)
        legal_basis = ''.join(wen_html_tree.xpath("//div[@class='del_right'][1]//ul/li[2]//text()"))
        # content = ''.join(wen_html_tree.xpath("//div[@class='PDF_pox']//text()"))
        # print(content)
        publish_date_str = ''.join(wen_html_tree.xpath("//table[@class='dftable']//text()"))
        # 裁判日期处理
        judgment_date = re.findall(r'\d{4}-\d{2}-\d{2}', judgment_date_str)[0]
        # 正则匹配
        publish_date = re.findall(r'\d{4}-\d{2}-\d{2}', publish_date_str)[0]
        value = {
            "案号": case_number,
            "链接": wen_url,
            "标题": title,
            "法院": court,
            "案件类型": case_type,
            "案由": cause,
            "程序类型": procedure_type,
            "裁判日期": judgment_date,
            "当事人": parties,
            "法律依据": legal_basis,
            "内容": content,
            "发布时间": publish_date,
        }
        up_instrument(case_number, wen_url, title, court, case_type, cause, procedure_type, judgment_date, parties,
                      legal_basis, content, publish_date, from_queue, webpage_id)

        print(value)

        tab.back(1)
    page.get('https://wenshu.court.gov.cn/')
    return page


def main(iphone, password_str):
    # iphone = '15938554242'
    # password_str = "Liyongheng10!"
    ocr, page, tab = initialize(iphone, password_str)
    tab, taget_url, taget_url_login, page = login(ocr,  page, tab,  iphone, password_str)
    while taget_url == taget_url_login:
        tab, taget_url, taget_url_login, page = login(ocr,  page, tab, iphone, password_str)
    for _ in range(30):
        value = paper_queue_next(webpage_url_list=['https://wenshu.court.gov.cn'])
        from_queue = value['id']
        webpage_id = value['webpage_id']
        anhao = value['name']
        # from_queue = 11
        # webpage_id = 22
        # anhao = '（2020）苏1181财保78号'
        page = search_instrument(tab, page, anhao, from_queue, webpage_id)
        success_data = {
            'id': from_queue,
            'description': '数据获取成功',
        }
        paper_queue_success(success_data)

        time.sleep(60)
    page.quit()


if __name__ == '__main__':
    account_data = [
        {
            'iphone': '15067522585',
            'password': 'Jyls@88912981'
        },
        {
            'iphone': '19857437935',
            'password': 'Liyongheng10!'
        },
        {
            'iphone': '19957241309',
            'password': 'Jyls@88912981'
        },

    ]
    random.shuffle(account_data)
    for account in account_data:
        main(account['iphone'], account['password'])


# value = paper_queue_next(webpage_url_list=['https://wenshu.court.gov.cn'])
# print(value)
