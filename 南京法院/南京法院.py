import base64
import time

from DrissionPage import ChromiumPage
from DrissionPage import WebPage
from tool.chaojiying import Chaojiying_Client

# 引入验证码模板
chaojiying = Chaojiying_Client('2437948121', 'liyongheng10', '961977')
# 构造实例
page = WebPage()
# 页面最大化
page.set.window.max()

# 打开目标网页
page.get("https://ssfw.njfy.gov.cn/#/ktggList")

# 获取验证码图片，并识别验证码
img_yzm = page.ele(".el-image__inner").attr("src")[23:]
# 将base64图片转换为图片文件
img_yzm = base64.b64decode(img_yzm)
with open("yzm.png", "wb") as f:
    f.write(img_yzm)

# captcha = chaojiying.PostPic(img_yzm, 1902)['pic_str']
# print(f"验证码：{captcha}")

# 点击验证码输入框，输入验证码
yzm_srk = page.ele('@class=el-input__inner', index=-1)
yzm_srk.input("1224")
time.sleep(1)
# 点击搜索按钮
button_ss = page.ele('@text()=查询')
button_ss.click()
print(button_ss.text)
