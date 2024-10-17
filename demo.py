from DrissionPage import ChromiumPage, ChromiumOptions
co = ChromiumOptions()
co = co.set_paths(local_port=9242)
co = co.set_argument('--no-sandbox')  # 关闭沙箱模式, 解决`$DISPLAY`报错
co = co.headless(True)  # 开启无头模式, 解决`浏览器无法连接`报错
def get_paper_url_cookies(url):
    cookie_dict = {}
    page = ChromiumPage(co)
    page.get(url)
    value_cookies = page.cookies()
    for key in value_cookies:
        cookie_dict[key['name']] = key['value']
    page.close()
    return cookie_dict

page = ChromiumPage(co)
page.get('https://www.xyshjj.cn/newsepaper/10193_153332_1733080_zgxyjjb.html')
print(page.html)
page.close()