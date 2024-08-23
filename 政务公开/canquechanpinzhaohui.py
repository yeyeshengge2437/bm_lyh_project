from DrissionPage import ChromiumPage, ChromiumOptions
import redis
from lxml import etree
# 连接redis数据库
redis_conn = redis.Redis()

co = ChromiumOptions()
co = co.set_paths(local_port=9120)
co = co.set_argument('--no-sandbox')  # 关闭沙箱模式, 解决`$DISPLAY`报错
co = co.headless(True)  # 开启无头模式, 解决`浏览器无法连接`报错

page = ChromiumPage(co)
page.get('http://qxzh.samr.gov.cn/qxzh/qxxxcx/web.jsp')
# 等待页面加载完成
page.wait.ele_displayed('.car_ul')

page_html = etree.HTML(page.html)
# 获取共有多少页
page_num = page_html.xpath("//span[@class='totalPages']/span/text()")
print(page_num)
for i in range(1, int(page_num[0])+1):

    url_html = etree.HTML(page.html)
    all_url = url_html.xpath("//ul[@id='car_ul']/li/a")
    for url1 in all_url:
        url = ''.join(url1.xpath("./@href"))
        print(url)
    page.ele("下一页", index=1).click(by_js=True)
    page.wait.ele_displayed('.car_ul')


page.quit()