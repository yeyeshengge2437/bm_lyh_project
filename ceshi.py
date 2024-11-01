from DrissionPage import ChromiumPage
page = ChromiumPage()
page.get('https://kimi.moonshot.cn/')
page.wait(2)
print(page.cookies())
page.close()
