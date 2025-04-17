import base64
import random
import time
from PIL import Image
from yunma_api import verify_tap, verify_slider  # 点选验证码识别, 滑块验证码识别


random_float = random.uniform(1, 5)

def get_image_size(image_path):
    # 打开图片
    with Image.open(image_path) as img:
        # 获取图片尺寸 (宽度, 高度)
        width, height = img.size
        return width, height


def point_to_percentage(width, height, x, y):
    # 计算水平方向和垂直方向的百分比
    x_percent = (x / width) * 100
    y_percent = (y / height) * 100
    return x_percent, y_percent

def get_captcha(page, iframe_url=None):
    time.sleep(3)
    iframe = page.get_frame(1)
    tab = iframe
    button = tab.ele("xpath=//div[@class='captcha-panel']/a")
    button.click(by_js=True)
    time.sleep(2)
    # 获取验证码图片
    captcha_img = tab.ele(f"xpath=//div[contains(@class, 'geetest_box_wrap')]/div[contains(@class, 'geetest_box')]")
    screen_loc = captcha_img.rect.corners
    left_top = screen_loc[0]
    right_bottom = screen_loc[2]
    base_str = page.get_screenshot(as_base64=True, left_top=left_top, right_bottom=right_bottom)
    with open("../captcha.png", "wb") as f:
        f.write(base64.b64decode(base_str))

    captcha_img_loc = captcha_img.rect.viewport_location  # 元素在屏幕中左上角的坐标
    raw_x, raw_y = captcha_img_loc
    captcha_img_size = captcha_img.rect.size

    # 右下角坐标
    right_x = raw_x + captcha_img_size[0]
    right_y = raw_y + captcha_img_size[1]

    width, height = get_image_size("../captcha.png")

    # 返回图片的坐标
    captcha_img_loc = captcha_img.rect.location
    raw_x, raw_y = captcha_img_loc
    captcha_text = captcha_img.text
    if "拖动滑块" in captcha_text:
        # pass
        value = verify_slider(base_str)
        ident_data = value["data"]["data"]
        move_num = (int(ident_data) / 2)
        # print(move_num)
        slider = tab.ele(f"xpath=//div[contains(@class, 'geetest_track')]/div[contains(@class, 'geetest_btn')]")
        # 获取滑块位置
        slider_loc = slider.rect.midpoint
        tab.actions.move_to(slider_loc)
        tab.actions.hold(slider).move_to((slider_loc[0] + move_num, slider_loc[1]), duration=0.45).release()
    elif "依次点击" in captcha_text:
        # 获取元素位置
        value = verify_tap(base_str)
        # print(f"使用点选验证码:{value}")
        ident_data = value["data"]["data"]
        data_list = ident_data.split("|")
        for coordinate in data_list:
            x, y = coordinate.split(",")
            x = int(x)
            y = int(y)

            x_percent, y_percent = point_to_percentage(width, height, x, y)
            page.actions.move_to((raw_x, raw_y))
            x_last = (right_x - raw_x) * (x_percent / 100) + raw_x
            y_last = (right_y - raw_y) * (y_percent / 100) + raw_y
            page.actions.move_to((x_last, y_last)).click()
            time.sleep(0.5)
        # 点击确定按钮
        tab.ele("确定").click(by_js=True)
    else:
        return False
