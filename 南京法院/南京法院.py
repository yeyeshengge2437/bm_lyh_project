import base64
import time

from DrissionPage import ChromiumPage, ChromiumOptions
# from DrissionPage import WebPage
from DrissionPage.common import Keys
from tool.chaojiying import Chaojiying_Client
import pymongo

# 连接数据库
client = pymongo.MongoClient()
db = client['spider']
collection = db['南京法院']


def get_captcha():
    time.sleep(3)
    # 获取验证码图片，并识别验证码
    img_yzm = page.ele(".el-image__inner").attr("src")[23:]
    # 将base64图片转换为图片文件
    img_yzm = base64.b64decode(img_yzm)
    with open("yzm.png", "wb") as f:
        f.write(img_yzm)

    captcha = chaojiying.PostPic(img_yzm, 1902)['pic_str']
    print(f"验证码：{captcha}")

    # 点击验证码输入框，输入验证码
    yzm_srk = page.ele("xpath=//div[@class='el-input el-input--mini']/input[@class='el-input__inner']", index=-1)
    # 清空输入框
    yzm_srk.clear()
    yzm_srk.click()
    yzm_srk.input(captcha)


def click_Inquire():
    """
    点击查询按钮
    :return:
    """
    value = page.ele("查询").parent()
    page.run_js("arguments[0].click();", value)


def error_dispose():
    """
    错误处理
    :return:
    """
    message = page.ele('@class:el-message')
    if message:
        # 获取元素文本
        print(message.text)
        # 再次获取验证码
        get_captcha()
        # 点击查询
        click_Inquire()

        return True
    else:
        return False


def jump_to_page(num):
    """
    跳转到指定页面
    :return:
    """
    jump = page.ele(".el-input__inner", index=8)
    jump.click()
    jump.clear()
    jump.input(num)
    # 回车
    jump.tab.actions.key_down('ENTER')


# 引入验证码模板
chaojiying = Chaojiying_Client('2437948121', 'liyongheng10', '961977')
# co = ChromiumOptions().headless()
# 构造实例
page = ChromiumPage()
# 页面最大化
page.set.window.max()

# 打开目标网页
page.get("https://ssfw.njfy.gov.cn/#/ktggList")
# 点击日期
date = page.ele(".el-input__inner", index=5)
date.clear()
date.input("2025-7-27")
# 点击回车
date.tab.actions.key_down('ENTER')

page.wait(2)

get_captcha()

# 点击搜索按钮
click_Inquire()

# 如果提示元素出现
error_dispose()

# 获取数据
# 等待页面加载完成
page.wait.ele_displayed('.el-table__row')
elements = page.eles('.el-table__row')

# 获取共多少页
total_page = int(page.ele(".el-pagination__total").text.split("共")[1].split("条")[0])
total_page = int(total_page / 10) + 1
print(f"共{total_page}页")

# # 遍历元素
# for element in elements:
#     # 获取到的数据
#     # print(element.text)
#     # 存储到数据库
#     collection.insert_one({"data": element.text})



# page_now = 1

for page_now in range(1, total_page):
    # 等待页面加载完成
    page.wait.ele_displayed('.el-table__row')
    elements = page.eles('.el-table__row')
    # 遍历元素
    for element in elements:
        # 获取到的数据
        # print(element.text)
        # 存储到数据库
        collection.insert_one({"data": element.text})


    # try:
    #     # 获取下一页的状态
    #     next_page_state = page.ele(".el-icon el-icon-arrow-right").parent().attr("disabled")
    #     # 获取当前页数
    #     # page_now = int(page.ele(".number active").text)
    # except Exception as e:
    #     print(f"获取下一页状态发生错误：{e}")
    #     # 再次获取验证码
    #     get_captcha()
    #     click_Inquire()
    #     get_captcha()
    #     jump_to_page(page_now)

    # 再次获取验证码
    get_captcha()
    try:
        # 点击下一页
        page.ele(".el-icon el-icon-arrow-right").click()
    except Exception as e:
        print(f"点击下一页发生错误：{e}")
        get_captcha()
        click_Inquire()
        get_captcha()
        jump_to_page(page_now)

    # 错误处理
    value_error = error_dispose()
    # 跳转到当前爬取界面
    if value_error:
        jump_to_page(page_now)

    print(page_now)


# 关闭浏览器
page.quit()
