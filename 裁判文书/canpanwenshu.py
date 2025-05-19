"""
裁判文书下载, https://wenshu.court.gov.cn/website/wenshu/181029CR4M5A62CH/index.html
"""
import base64
import re
import time
import ddddocr
from lxml import etree
from lxml import html as html_import
from DrissionPage import ChromiumPage, ChromiumOptions
import tempfile
from a_mysql_connection_pool import up_instrument


def del_style(content_html):
    tree = etree.HTML(content_html)
    # 删除所有 <style> 标签
    for style_tag in tree.xpath("//style"):
        style_tag.getparent().remove(style_tag)

    # 输出处理后的 HTML
    up_content_html = html_import.tostring(tree, encoding="unicode")
    return up_content_html


def del_script(content_html):
    tree = etree.HTML(content_html)
    # 删除所有 <style> 标签
    for style_tag in tree.xpath("//script"):
        style_tag.getparent().remove(style_tag)

    # 输出处理后的 HTML
    up_content_html = html_import.tostring(tree, encoding="unicode")
    return up_content_html


def del_link(content_html):
    tree = etree.HTML(content_html)
    # 删除所有 <style> 标签
    for style_tag in tree.xpath("//link"):
        style_tag.getparent().remove(style_tag)

    # 输出处理后的 HTML
    up_content_html = html_import.tostring(tree, encoding="unicode")
    return up_content_html


def compress_html(html):
    # 移除 <!-- ... --> 注释（可选）
    html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)

    # 移除换行符(\n)、制表符(\t)、连续空格(保留单个空格)
    html = re.sub(r'\s+', ' ', html)

    # 移除 > 和 < 之间的空格（避免破坏HTML标签结构）
    html = re.sub(r'>\s+<', '><', html)

    html = re.sub(r'<div class="right-list clearfix"><h3>猜你喜欢</h3>.*', '', html)

    return html.strip()


"""
裁判文书账号
# 18507196517	YZfdiW9486!
# 18507146596	YDQJOK2449!
# 18507140732	kSxZQy5877@
# 18571520338	sUPLBn4395!
# 18507137814	jcEQQD5154.
"""
iphone = '15938554242'
password_str = 'Liyongheng10!'
ocr = ddddocr.DdddOcr(show_ad=False)
co = ChromiumOptions()
# co = co.set_user_data_path(r'D:\chome_data\data_one')
co.set_argument('--incognito')
# co.set_argument(f'--user-data-dir={tempfile.TemporaryFile()}')
co.set_paths(local_port=9247)

# anhao_set = {'（2023）甘01民终7998号', '（2019）辽01执异461号', '（2016）甘民初91号', '（2017）甘03民终352号', '（2021）甘0802民初3216号', '（2018）甘0302民初3123号', '（2015）沪高民四（海）终字第99号', '（2019）甘03民终80号', '（2018）甘0302民初1181号', '（2016）甘0302民初2594号', '（2018）甘0302民初179号', '（2018）甘0302民初229号', '（2020）甘0302民初912号', '（2015）金中民一初字第14号', '（2022）甘03民终115号', '（2020）甘03民特1号', '（2023）甘0302民初866号', '（2019）甘0302民初308号', '（2017）甘0302民初80号', '（2023）甘0302民初723号', '（2020）甘民终132号', '（2019）桂0602民初167号', '（2021）沪7101民初1542号', '（2016）最高法民终254号', '（2023）甘03民终596号', '（2020）甘03执23号之五', '（2015）普民二（商）初字第951号', '（2017）甘0302民初2764号', '（2020）沪7101破172号', '（2021）甘0302民初281号', '（2015）普民二（商）初字第961号', '（2019）甘执83号', '（2018）甘03民终33号', '（2019）甘03民终67号', '（2021）甘0102民初14761号', '（2017）甘03民终312号', '（2017）沪0107执294号', '（2017）甘03民终216号', '（2016）陕民初31号', '（2016）沪02民特398号', '（2016）甘03民终309号', '（2024）甘01民终7331号', '（2012）兰法民二初字第95号', '（2018）甘0302民初444号', '（2021）甘0302民初2431号', '（2018）浙0102民初6515号', '（2021）甘03民终22号', '（2019）甘03民初28号', '（2016）甘民初37号', '（2020）甘0321民初2052号', '（2017）甘民终453号', '（2023）甘0302民初994号', '（2016）甘0302民初2475号', '（2020）甘01民初711号之一', '(2023)甘0123民初2513号'}
anhao_set = {'（2016）甘民初91号'}
# 连接浏览器
page = ChromiumPage()
tab = page.get_tab()
taget_url = 'https://account.court.gov.cn/app?back_url=https%3A%2F%2Faccount.court.gov.cn%2Foauth%2Fauthorize%3Fresponse_type%3Dcode%26client_id%3Dzgcpwsw%26redirect_uri%3Dhttps%253A%252F%252Fwenshu.court.gov.cn%252FCallBackController%252FauthorizeCallBack%26state%3D421fc4a4-5cc2-4ecd-bb44-257b1a17ee98%26timestamp%3D1732779592364%26signature%3DA4C212AFA550EFA5E27D9A3E094A741A7A14BCE6873A632A4CF587CF76474838%26scope%3Duserinfo#/login'
# 访问网页
tab.get(taget_url)
tab.refresh()
tab.wait.doc_loaded()
# print(tab.html)
time.sleep(3)

tab.ele("@class=phone-number-input", ).input(iphone)  # 1
time.sleep(2)
# login.click(by_js=True)
# login
tab.ele("@class=password", ).input(password_str)  # 1
time.sleep(2)
tab.ele("@class=captcha-img").click()  # 1
time.sleep(8)
image_captcha = tab.ele("xpath=//img[@class='captcha-img']")
image_value = image_captcha.get_screenshot(as_base64=True)
value_captcha = base64.b64decode(image_value)
captcha = ocr.classification(value_captcha)
captcha = captcha.lower()
# print(f'验证码是{captcha}')
tab.ele("@class=answer").input(captcha)
time.sleep(4)
tab.ele("@class=button button-primary").click()  # 1
time.sleep(8)
tab.refresh()
tab.wait.doc_loaded()
if tab.url == taget_url:
    time.sleep(3)

    tab.ele("@class=phone-number-input", ).input(iphone)  # 1
    time.sleep(2)
    # login.click(by_js=True)
    # login
    tab.ele("@class=password", ).input(password_str)  # 1
    time.sleep(2)
    tab.ele("@class=captcha-img").click()  # 1
    time.sleep(5)
    image_captcha = tab.ele("xpath=//img[@class='captcha-img']")
    image_value = image_captcha.get_screenshot(as_base64=True)
    value_captcha = base64.b64decode(image_value)
    captcha = ocr.classification(value_captcha)
    captcha = captcha.lower()
    # print(f'验证码是{captcha}')
    tab.ele("@class=answer").input(captcha)
    time.sleep(4)
    tab.ele("@class=button button-primary").click()  # 1
    tab.wait.doc_loaded()
    time.sleep(8)
# print(tab.html)
# tab.ele("@id=loginLi").click(by_js=True)
login_text = tab.ele("@id=loginLi")

tab.ele("@class=searchKey search-inp").input("开始123")  # 1
time.sleep(5)
tab.ele("@class=search-rightBtn search-click").click()  # 1
tab.wait.doc_loaded()
time.sleep(7)
for anhao in anhao_set:
    # try:
    tab.ele("@class=searchKey search-inp").input(anhao)  # 1
    time.sleep(1)
    tab.ele("@class=search-rightBtn search-click").click()  # 1
    tab.wait.doc_loaded()
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
        new_tab = page.new_tab()
        new_tab.get(url)
        time.sleep(10)
        wen_html = new_tab.html
        wen_html = del_script(wen_html)
        wen_html = del_style(wen_html)
        wen_html = del_link(wen_html)
        wen_html = compress_html(wen_html)
        wen_html_tree = etree.HTML(wen_html)
        case_number = ''  # 案号从输入项
        wen_url = url
        title = ''.join(wen_html_tree.xpath("//div[@class='PDF_title']/text()"))
        court = ''.join(wen_html_tree.xpath("//h4[@class='clearfix'][1]//text()"))
        case_type = ''.join(wen_html_tree.xpath("//h4[@class='clearfix'][2]//text()"))
        cause = ''.join(wen_html_tree.xpath("//h4[@class='clearfix'][3]//text()"))
        procedure_type = ''.join(wen_html_tree.xpath("//h4[@class='clearfix'][4]//text()"))
        judgment_date_str = ''.join(wen_html_tree.xpath("//h4[@class='clearfix'][5]//text()"))
        parties = ''.join(wen_html_tree.xpath("//h4[@class='clearfix'][6]//text()"))
        legal_basis = ''.join(wen_html_tree.xpath("//div[@class='del_right'][1]//ul/li[2]//text()"))
        content = ''.join(wen_html_tree.xpath("//div[@class='PDF_pox']/div//text()"))
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
        from_queue = 1234
        webpage_id = 1234
        up_instrument(case_number, wen_url, title, court, case_type, cause, procedure_type, judgment_date, parties,
                      legal_basis, content, publish_date, from_queue, webpage_id)

        print(value)

    tab.back(1)

page.close()
