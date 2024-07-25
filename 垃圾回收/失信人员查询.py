# 网站可能检测selenium信息  需要进行隐藏
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import undetected_chromedriver as uc
from PIL import Image
from tool.chaojiying import Chaojiying_Client

chaojiying = Chaojiying_Client('2437948121', 'liyongheng10', '961977')

# 绕过selenium检测
chrome_options = Options()
# s = Service(r"C:\Users\24379\.cache\selenium\chromedriver\win64\126.0.6478.182\chromedriver.exe")
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
url = "http://zxgk.court.gov.cn/shixin/"
driver.get(url=url)

# 网站响应比较慢 有可能验证码没有刷新出来 会有弹窗提示 需要处理
time.sleep(10)

# 获取验证码图片
# 剪裁验证码
checkCodeImg = driver.find_element(by=By.XPATH,value="//img[@id='captchaImg']")
driver.save_screenshot("full_page.png")
left = checkCodeImg.location["x"]
top = checkCodeImg.location["y"]
right = left + checkCodeImg.size["width"]
bottom = top + checkCodeImg.size["height"]
logo = Image.open("full_page.png")
res = logo.crop((left,top,right,bottom))
res.save("code.png")

im = open('code.png', 'rb').read()
result = chaojiying.PostPic(im, 1902)['pic_str']


# 搜索失信人数据
driver.find_element(by=By.XPATH,value="//input[@id='pName']").send_keys("张伟")
driver.find_element(by=By.XPATH,value="//input[@id='yzm']").send_keys(result)
driver.find_element(by=By.XPATH,value="//button[contains(text(),'查询')]").click()

# 需要判断页面是否显示验证码过期 重新识别 重新查询
# # 网站响应比较慢 可以循环识别 一旦和上一次识别结构不一致 可以认为新的验证码已经刷新
time.sleep(15)


# 查询数据
time.sleep(5)
driver.save_screenshot("数据页面.png")
# "//table[@id='result-table']/tbody[@id='tbody-result']/tr"
input("按任意键退出")