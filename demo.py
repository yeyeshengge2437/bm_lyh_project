import random
import time
from DrissionPage import ChromiumPage, ChromiumOptions
co = ChromiumOptions()
co = co.set_argument('--no-sandbox')
co = co.headless()
co = co.ignore_certificate_errors()  # 忽略证书错误
co.set_paths(local_port=9134)
def get_now_image(page, url):
    tab = page.new_tab()
    tab.get(url)
    time.sleep(2)
    bytes_str = tab.get_screenshot(as_bytes='png')
    # 随机的整数
    random_int = random.randint(0, 1000000)
    with open(f'{random_int}.png', 'wb') as f:
        f.write(bytes_str)
    tab.close()
    return random_int

page = ChromiumPage(co)
page.set.load_mode.none()

get_now_image(page, 'https://drissionpage.cn/ChromiumPage/screen/#%EF%B8%8F%EF%B8%8F-%E9%A1%B5%E9%9D%A2%E6%88%AA%E5%9B%BE')