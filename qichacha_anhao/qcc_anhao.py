import time

from DrissionPage import ChromiumPage, ChromiumOptions

# co = ChromiumOptions()
# co = co.set_argument('--no-sandbox')
# co = co.headless()
# co.set_paths(local_port=9136)

co = ChromiumOptions()
co = co.set_user_data_path(r'C:\Users\24379\AppData\Local\Google\Chrome\User Data')
co.set_paths(local_port=9136)
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
# ----------------开庭公告案号-------------------
new_tab.ele('法律诉讼').click(by_js=True)
lian_list = new_tab.ele("xpath=//section[@id='lianlist']//table[@class='ntable app-ntable-expand-all']").html
print(lian_list)
# 判断是否有下一页元素
target_list = new_tab.eles("xpath=//section[@id='lianlist']//ul[@class='pagination']//a")
while True:
    if target_list[-1].text == '>':
        target_list[-1].click(by_js=True)
        time.sleep(2)
        lian_list_html = new_tab.ele("xpath=//section[@id='lianlist']//table[@class='ntable app-ntable-expand-all']").html
        if "无数据" in lian_list_html:
            break
        print(lian_list_html)
    else:
        break
# ----------------开庭公告案号-------------------
time.sleep(2)
input("---------------")
page.quit()
