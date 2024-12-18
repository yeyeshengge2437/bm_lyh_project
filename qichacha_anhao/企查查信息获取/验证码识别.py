import base64
import json
import random
import time
from PIL import Image
from yunma_api import verify_tap, verify_slider  # 点选验证码识别, 滑块验证码识别
from DrissionPage import ChromiumPage, ChromiumOptions

# co = ChromiumOptions()
# co = co.set_user_data_path(r"D:\chome_data\data_one")
# co.set_paths(local_port=9136)
random_float = random.uniform(1, 5)



def get_captcha(page):
    # # 连接浏览器
    # page = ChromiumPage(co)
    tab = page.new_tab()
    # 访问网页
    tab.get("111.html")
    time.sleep(3)
    # 验证码处理
    captcha_ele = tab.get_frame(1)
    captcha_url = captcha_ele.attr("src")
    # new_tab = page.new_tab()
    # tab = new_tab
    tab.get(captcha_url)
    button = tab.ele("xpath=//div[@class='captcha-panel']/a")
    button.click(by_js=True)
    # tab.wait.ele_displayed("xpath=//div[contains(@class, 'geetest_box_wrap')]")
    time.sleep(2)
    # 获取验证码图片
    captcha_img = tab.ele(f"xpath=//div[contains(@class, 'geetest_box_wrap')]/div[contains(@class, 'geetest_box')]")
    captcha_img_size = captcha_img.rect.size
    # print(captcha_img_size)
    # captcha_img = tab.ele(f"xpath=//*")
    base_str = captcha_img.get_screenshot(as_base64=True)
    with open("../captcha.png", "wb") as f:
        f.write(base64.b64decode(base_str))

    # # 测试
    # # 获取滑块元素
    # slider = tab.ele(f"xpath=//div[contains(@class, 'geetest_track')]/div[contains(@class, 'geetest_btn')]")
    # # 获取滑块位置
    # slider_loc = slider.rect.location
    # print(slider_loc)
    # # (209.1015625, 459.08203125)
    # tab.actions.move_to(slider.rect.location)
    # tab.actions.hold(slider).move_to((210, 600), duration=2).release()

    # 返回图片的坐标
    captcha_img_loc = captcha_img.rect.location
    raw_x, raw_y = captcha_img_loc
    captcha_text = captcha_img.text
    if "拖动滑块" in captcha_text:
        # pass
        value = verify_slider(base_str)
        ident_data = value["data"]["data"]
        move_num = (int(ident_data) / 2) + 35
        # print(move_num)
        slider = tab.ele(f"xpath=//div[contains(@class, 'geetest_track')]/div[contains(@class, 'geetest_btn')]")
        # 获取滑块位置
        slider_loc = slider.rect.location
        tab.actions.move_to(slider_loc)
        tab.actions.hold(slider).move_to((slider_loc[0] + move_num, slider_loc[1]), duration=0.45).release()
        # print(f"使用滑块验证码")
        # input()
    elif "依次点击" in captcha_text:
        # pass
        # 获取元素位置
        value = verify_tap(base_str)
        # print(f"使用点选验证码:{value}")
        ident_data = value["data"]["data"]
        data_list = ident_data.split("|")
        for coordinate in data_list:
            x, y = coordinate.split(",")
            x = int(x) / 2
            y = int(y) / 2

            # print(f"点击位置:{x, y}")
            # 获取图片的元素
            # img_ele = tab.ele(f"xpath=//div[contains(@class, 'geetest_click')]/div[contains(@class, 'geetest_window')]/div[contains(@class, 'geetest_bg')]")
            tab.actions.move(x + raw_x, y + raw_y).click()
            tab.actions.move_to((0, 0))
            time.sleep(0.5)
        # 点击确定按钮
        tab.ele("确定").click(by_js=True)
    # if "您的操作过于频繁，验证后再操作" not in tab.html:
    #     tab.close()
    # else:
    #     input("请重试：")
    #     get_captcha(page)
    tab.close()



