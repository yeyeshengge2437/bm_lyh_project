import time

from DrissionPage import ChromiumPage, ChromiumOptions
page = ChromiumPage()
page.get('https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzI5ODk2MTY1Mg==&action=getalbum&album_id=3421134606546747396#wechat_redirect')
for i in range(20):
    page.scroll.to_bottom()
    time.sleep(1)
time.sleep(10)
print(page.html)
page.close()