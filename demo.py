from DrissionPage import ChromiumPage, ChromiumOptions

co = ChromiumOptions()
co = co.set_paths(local_port=9113)
co = co.set_argument('--no-sandbox')  # 关闭沙箱模式, 解决`$DISPLAY`报错
co = co.headless(True)  # 开启无头模式, 解决`浏览器无法连接`报错

page = ChromiumPage(co)