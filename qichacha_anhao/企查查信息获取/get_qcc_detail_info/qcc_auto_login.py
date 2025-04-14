import base64
import time
from yunma_api import verify_tap, verify_slider
from PIL import Image
from DrissionPage import ChromiumPage, ChromiumOptions


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


def auto_login(page, account, password):
    page.wait(2)
    page.ele("xpath=//div[@class='qcc-login-type-change']").click()
    time.sleep(2)
    page.ele("xpath=//div[@class='qcc-login-phone-tabs-item'][2]/a[@class='active']").click()
    time.sleep(2)
    page.ele(
        "xpath=//input[@class='qccd-input qccd-input-lg qcc-login-quick-login-phone qcc-login-quick-login-password']").input(account)
    time.sleep(1)
    page.ele("xpath=//input[@class='qccd-input qccd-input-lg']").input(password)
    page.ele(
        "xpath=//div[@class='qcc-login-quick-login'][2]/button[@class='qccd-btn qccd-btn-primary qccd-btn-lg qccd-btn-block']").click()
    time.sleep(3)
    sliding_diagram = page.ele("xpath=//div[contains(@class, 'geetest_box_wrap')]/div[contains(@class, 'geetest_box')]")
    image_loc = sliding_diagram.rect.corners
    left_top = image_loc[0]
    right_bottom = image_loc[2]
    image_value = page.get_screenshot(as_base64=True, left_top=left_top, right_bottom=right_bottom)
    with open("./captcha.png", "wb") as f:
        f.write(base64.b64decode(image_value))

    captcha_img_loc = sliding_diagram.rect.viewport_location  # 元素在屏幕中左上角的坐标
    raw_x, raw_y = captcha_img_loc
    captcha_img_size = sliding_diagram.rect.size

    # 右下角坐标
    right_x = raw_x + captcha_img_size[0]
    right_y = raw_y + captcha_img_size[1]

    width, height = get_image_size("./captcha.png")


    captcha_text = sliding_diagram.text
    if "拖动滑块" in captcha_text:
        # pass
        value = verify_slider(image_value)
        ident_data = value["data"]["data"]
        slider = page.ele(f"xpath=//div[contains(@class, 'geetest_track')]/div[contains(@class, 'geetest_btn')]")
        move_num = int(ident_data) / 2
        # 获取滑块位置
        slider_loc = slider.rect.midpoint
        page.actions.move_to(slider_loc)
        page.actions.hold(slider).move_to((slider_loc[0] + move_num, slider_loc[1]), duration=0.45).release()
    elif "依次点击" in captcha_text:
        # pass
        # 获取元素位置
        value = verify_tap(image_value)
        ident_data = value["data"]["data"]
        data_list = ident_data.split("|")
        for coordinate in data_list:
            x, y = coordinate.split(",")
            x = int(x)
            y = int(y)
            x_percent, y_percent = point_to_percentage(width, height, x, y)
            print(x_percent, y_percent)
            page.actions.move_to((raw_x, raw_y))
            x_last = (right_x - raw_x) * (x_percent / 100) + raw_x
            y_last = (right_y - raw_y) * (y_percent / 100) + raw_y
            print(x_last, y_last)
            page.actions.move_to((x_last, y_last)).click()
            print(f'左上角位置为：{(raw_x, raw_y)}, 右下角的位置为：{(right_x, right_y)}')
            print(f"点击位置:{(x_last, y_last)}")
            # page.actions.move_to((raw_x, raw_y))
            time.sleep(0.5)
        # 点击确定按钮
        page.ele("确定").click(by_js=True)
    time.sleep(4)
    try:
        sign_in_status = page.ele("xpath=//button[@class='qccd-btn qccd-btn-primary qcc-header-login-btn']")
        if "登录" in sign_in_status.text:
            return False
        elif '0' in sign_in_status.text:
            return True
    except:
        return True

