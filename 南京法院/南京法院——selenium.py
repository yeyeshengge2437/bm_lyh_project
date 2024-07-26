from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


options = Options()

# 声明浏览器对象
driver = webdriver.Chrome(options=options)

# 获取浏览器的数据
driver.get('https://ssfw.njfy.gov.cn/#/ktggList')

# 页面最大化
driver.maximize_window()
# 等待页面加载完成
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='el-date-editor el-input el-input--mini el-input--prefix el-input--suffix el-date-editor--date']/input[@class='el-input__inner']")))

# 定位搜索框
search_input = driver.find_element(By.XPATH, "//div[@class='el-date-editor el-input el-input--mini el-input--prefix el-input--suffix el-date-editor--date']/input[@class='el-input__inner']")

# 模拟用户输入行为
search_input.send_keys('2025-07-10')

# 定位搜索按钮
search_button = driver.find_element(By.XPATH, "//div/button[@class='el-button el-button--default el-button--small'][1]")

# 点击搜索按钮
driver.execute_script("arguments[0].click();", search_button)
input()