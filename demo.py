from DrissionPage import ChromiumPage

page = ChromiumPage()
page.get('https://www.dianxiaomi.com/pddkjProduct/add.htm')
# 定位到账号文本框，获取文本框元素
page.wait.load_start()
select1 = page.ele('#shopId')
select1.click()
page.wait.load_start()
option = page.ele('option[value="5654390"]')
option.click(by_js=True)