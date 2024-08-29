import re
import time
from datetime import datetime
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat, judging_bm_criteria
import mysql.connector
import requests
from lxml import etree


def get_date_a(date):
    year = date.split('-')[0]
    month = date.split('-')[1]
    day_num = date.split('-')[2]
    day_num = int(day_num)
    headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://gsdbs.baozhanmei.net',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'nian': year,
        'yue': month,
    }

    response = requests.post('https://gsdbs.baozhanmei.net/list_news/datebd/1110', headers=headers, data=data)
    data = response.content.decode()
    html = etree.HTML(data)
    date_a = {}
    # 获取所有li标签下的内容
    list_li = html.xpath('//li')
    for li in list_li:
        # 判断li下否有a标签
        li_a = ''.join(li.xpath('./a/@href'))
        li_num = ''.join(li.xpath('.//text()'))
        # 构建字典
        date_a[li_num] = li_a
    if date_a[str(day_num)]:
        return date_a[str(day_num)]
    else:
        return False


paper = "工商导报"
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    # 'cookie': 'PHPSESSID=jauifhfh287skj6dm738vc16t4; Hm_lvt_d69321757dcfbfbe09dbddd4dca87b28=1724140544; HMACCOUNT=FDD970C8B3C27398; Hm_lpvt_d69321757dcfbfbe09dbddd4dca87b28=1724141213',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
}

today = datetime.now().strftime('%Y-%m-%d')


def get_gongshangdao_paper(paper_time, queue_id, webpage_id):
    url = get_date_a(paper_time)
    # 将today的格式进行改变
    day = paper_time
    if url:
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code == 200:
            data = response.content.decode()
            bm_html = etree.HTML(data)
            bm_list = bm_html.xpath("//div[@id='index_f_list']/ul/li/a")
            for bm in bm_list:
                # 获取版面名称
                bm_name = ''.join(bm.xpath(".//text()"))
                # 获取版面链接
                bm_url = ''.join(bm.xpath("./@href"))
                # 获取版面下的内容
                bm_response = requests.get(bm_url, headers=headers, verify=False)
                time.sleep(2)
                bm_data = bm_response.content.decode()
                bm_html1 = etree.HTML(bm_data)
                # 获取版面图片
                bm_img = ''.join(bm_html1.xpath("//img[@id='imgmaps']/@src"))
                bm_areaList = bm_html1.xpath("//div[@id='index_a_list']/ul/li/a")
                for bm_area in bm_areaList:
                    # 获取文章名称
                    article_name = ''.join(bm_area.xpath("./text()"))
                    # 获取文章链接
                    article_url = ''.join(bm_area.xpath("./@onclick"))
                    # 使用re获取链接中的数字
                    article_url = re.findall(r'\d+', article_url)[0]
                    article_url = f'https://gsdbs.baozhanmei.net/list_news/article/1110?id={article_url}'
                    # 获取文章内容
                    article_response = requests.get(article_url, headers=headers, verify=False)
                    article_data = article_response.content.decode()
                    time.sleep(2)
                    article_html = etree.HTML(article_data)
                    content = ''.join(article_html.xpath('//*[@id="Zoom"]/p//text()'))
                    pdf_set = set()

                    create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    create_date = datetime.now().strftime('%Y-%m-%d')

                    # 上传到测试数据库
                    conn_test = mysql.connector.connect(
                        host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
                        user="col2024",
                        password="Bm_a12a06",
                        database="col",
                    )
                    cursor_test = conn_test.cursor()
                    if bm_img not in pdf_set and (
                            "分类信息" in article_name or judging_bm_criteria(article_name)) and judge_bm_repeat(paper,
                                                                                                                 bm_url):
                        # 将报纸img上传
                        up_img = upload_file_by_url(bm_img, paper, "img", "paper")
                        pdf_set.add(bm_img)
                        # 上传到报纸的图片或PDF
                        insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_img, page_url, img_url, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s, %s,%s, %s, %s, %s, %s, %s)"

                        cursor_test.execute(insert_sql,
                                            (day, paper, bm_name, bm_img, bm_url, up_img, create_time, queue_id,
                                             create_date, webpage_id))
                        conn_test.commit()

                    if judging_criteria(article_name, content):
                        # 上传到报纸的内容
                        insert_sql = "INSERT INTO col_paper_notice (page_url, day, paper, title, content, content_url,  create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)"

                        cursor_test.execute(insert_sql,
                                            (bm_url, day, paper, article_name, content, article_url, create_time,
                                             queue_id,
                                             create_date, webpage_id))
                        conn_test.commit()

                    cursor_test.close()
                    conn_test.close()

            success_data = {
                'id': queue_id,
                'description': '数据获取成功',
            }
            paper_queue_success(success_data)

        else:
            raise Exception(f'该日期没有报纸')
    else:
        raise Exception(f'该日期没有报纸')

# paper_queue = paper_queue_next(
#             webpage_url_list=['https://epaper.lnd.com.cn'])
# webpage_name = paper_queue['webpage_name']
# queue_day = paper_queue['day']
# queue_id = paper_queue['id']
# webpage_id = paper_queue["webpage_id"]
# queue_id = 1111
# webpage_id = 1111
# time = '2020-01-21'
# get_gongshangdao_paper(time, queue_id, webpage_id)
