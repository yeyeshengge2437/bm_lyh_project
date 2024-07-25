import time

from DrissionPage import ChromiumPage
from DrissionPage import WebPage
from tool.chaojiying import Chaojiying_Client


# 获取并点击提交验证码
def click_submit_captcha():
    # 点击验证码的框
    page.ele("#yzm").click()
    # 等待1秒
    time.sleep(1)
    # 获取验证码截图
    page.ele("#captchaImg").get_screenshot("captcha.png")

    im = open("captcha.png", 'rb').read()
    captcha = chaojiying.PostPic(im, 1902)['pic_str']
    print(f"验证码为：{captcha}")
    # 清除框中的内容
    page.ele("#yzm").clear()

    # 输入验证码
    page.ele("#yzm").input(captcha)

    # 点击查询按钮
    page.ele('.col-lg-2 col-sm-2 ').click()

    # 等待页面加载
    page.wait(10)

    if page.ele("#tbody-result").text == "验证码错误或验证码已过期。":
        click_submit_captcha()
    else:
        return True


# 输入验证码但不点击提交
def input_captcha():
    # 点击验证码的框
    page.ele("#yzm").click()
    # 等待1秒
    time.sleep(1)
    # 获取验证码截图
    page.ele("#captchaImg").get_screenshot("captcha.png")

    im = open("captcha.png", 'rb').read()
    captcha = chaojiying.PostPic(im, 1902)['pic_str']
    print(f"验证码为：{captcha}")
    # 清除框中的内容
    page.ele("#yzm").clear()

    # 输入验证码
    page.ele("#yzm").input(captcha)
    # 等待加载
    page.wait(5)


chaojiying = Chaojiying_Client('2437948121', 'liyongheng10', '961977')

page = WebPage()
# 页面最大化
page.set.window.max()

page.get('http://zxgk.court.gov.cn/zhongben/')

# # 开始监听， 指定获取数据包
# page.listen.start("shixin/disDetailNew")

# # 删除干扰元素
# page.ele("#frameImg").remove_attr("style")

ele = page.ele("#pName")

ele.input("郑强")
page.wait(2)

click_submit_captcha()

# 等待查询结果
page.wait.load_start()

# 获取总页数
fayuan_pages = page.ele("#totalPage-show").text
print(f"总页数：{fayuan_pages}")
# 遍历每一页
for i in range(1, int(fayuan_pages) + 1):

    time.sleep(1)
    # 获取查询结果
    items = page.ele("#tbody-result")
    print(items.text)
    for i in range(1, 10 + 1):
        # 点击查看
        page.ele("查看", index=i).click()
        # 如果界面上有显示验证码错误字样
        if page.ele(".layui-layer-content layui-layer-padding"):
            page.ele(".layui-layer-ico layui-layer-close layui-layer-close1").click()
            # 等待
            time.sleep(1)
            # 重新输入验证码
            input_captcha()
            page.ele("@text()=查看", index=i).click()

        # 等待元素出现
        # page.ele(".Resultlist").wait(10)
        page.wait.ele_displayed(".Resultlist")
        # 获取详细结果
        detailed_results = page.ele(".Resultlist")
        # 打印详细结果
        detailed_info = detailed_results.text
        # # 去除制表符
        # detailed_info = detailed_info.replace('\t', '')
        # # 以换行符分割
        # detailed_info_list = detailed_info.split('\n')
        print(detailed_info)

        # # 等待元素出现
        # page.ele("关闭").wait(10)
        # 关闭查看
        page.ele(".btn btn-primary center-block").click()

        # 点击下一页
        page.ele("#next-btn").click()
