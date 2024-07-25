import hashlib
import time

from DrissionPage import ChromiumPage
from DrissionPage import WebPage
from tool.chaojiying import Chaojiying_Client
import json
import pymongo
import redis

# 连接到redis数据库
redis_conn = redis.Redis()
# 连接mongo数据库
client = pymongo.MongoClient()
db = client['sxr_data']
sxr_data = db['shixin']
shixin_page = db['shixin_page']
search_key = db['search_key']


chaojiying = Chaojiying_Client('2437948121', 'liyongheng10', '961977')
page = ChromiumPage()

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


# 抓取数据
def crawl_data(key, sxr_page=1):
    page = ChromiumPage()
    # 页面最大化
    page.set.window.max()

    page.get('http://zxgk.court.gov.cn/shixin/')

    # # 开始监听， 指定获取数据包
    # page.listen.start("shixin/disDetailNew")

    # 删除干扰元素
    page.ele("#frameImg").remove_attr("style")

    ele = page.ele("#pName")

    ele.input(key)
    page.wait(2)

    click_submit_captcha()

    # 等待查询结果
    page.wait.load_start()

    if sxr_page == 1:
        pass
    else:
        page.ele("#goto").input(sxr_page)
        # 点击跳转到
        page.ele("跳转到").click()

    # 获取总页数
    fayuan_pages = page.ele("#totalPage-show").text
    print(f"总页数：{fayuan_pages}")
    # 遍历每一页
    for page_sxr in range(sxr_page, int(fayuan_pages)):
        time.sleep(1)
        # 获取查询结果
        # items = page.ele("#tbody-result")
        for i in range(-2, -11 - 1, -1):
            try:
                # 点击查看
                page.ele("查看", index=i).click()
            except:
                # 如果没有找到查看按钮
                return False

            # 如果界面上有显示验证码错误字样
            if page.ele(".layui-layer-content layui-layer-padding"):
                page.ele(".layui-layer-ico layui-layer-close layui-layer-close1").click()
                # 等待
                time.sleep(1)
                # 重新输入验证码
                input_captcha()
                page.ele("查看", index=i).click()

            # 等待元素出现
            page.ele("#partyDetail").wait(10)
            # 获取详细结果
            detailed_results = page.ele("#partyDetail")
            # 打印详细结果
            detailed_info = detailed_results.text
            # # 去除制表符
            # detailed_info = detailed_info.replace('\t', '')
            # # 以换行符分割
            # detailed_info_list = detailed_info.split('\n')

            # 数据去重
            hash_value = hashlib.md5(json.dumps(detailed_info).encode('utf-8')).hexdigest()
            # 判断唯一的哈希值是否在集合中
            if not redis_conn.sismember("sxr_data_set", hash_value):
                # 不重复哈希值添加到集合中
                redis_conn.sadd("sxr_data_set", hash_value)
                # 将详细结果存入数据库
                sxr_data.insert_one({"detailed_info": detailed_info})
            else:
                print("重复数据：", detailed_info)

            # # 等待元素出现
            # page.ele("关闭").wait(10)
            # 关闭查看
            page.ele(".btn btn-zxgk center-block").click()

        # 将当前页码存入mongo中
        # 清空数据库
        shixin_page.delete_many({})
        shixin_page.insert_one({"page": page_sxr + 1, "key": key})

        # 点击下一页
        page.ele("#next-btn").click()


def run():
    # 从数据库search_key中获取一个数据
    key = search_key.find_one({}, {"_id": 0})['province']

    # 如果crawl_data函数出错，重新调用
    max_attempts = 10  # 设置最大尝试次数
    attempts = 0

    while attempts < max_attempts:
        try:
            db_page = shixin_page.find_one({}, {"_id": 0})["page"]
            crawl_data(key, sxr_page=db_page)
            break  # 如果函数执行成功，退出循环
        except Exception as e:
            print(f"发生错误：{e}")
            attempts += 1  # 增加尝试次数
            print(f"尝试再次爬取，尝试{attempts}/{max_attempts}")

    if attempts == max_attempts:
        print("已达到最大尝试次数。退出。")

    # shixin_page.find_one({}, {"_id": 0})["page"])删除search_key中已经使用的数据
    search_key.delete_one({"key": key})


if __name__ == '__main__':
    run()
