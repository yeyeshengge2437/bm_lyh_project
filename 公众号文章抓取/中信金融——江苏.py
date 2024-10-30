import time
from lxml import etree
from DrissionPage import ChromiumPage, ChromiumOptions
page = ChromiumPage()
page.get('https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzI5ODk2MTY1Mg==&action=getalbum&album_id=3421134606546747396#wechat_redirect')
for i in range(20):
    page.scroll.to_bottom()
    time.sleep(1)
time.sleep(10)
html = etree.HTML(page.html)
data_list = html.xpath("//li[contains(@class, 'album__list-item')]")
for data in data_list:
    title = ''.join(data.xpath("./@data-title"))
    title_url = ''.join(data.xpath("./@data-link"))
    print(title, title_url)

page.close()
