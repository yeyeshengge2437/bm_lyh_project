"""
辽宁省住房和城乡建设厅-公示公告
"""
import hashlib
import json
import re
import time
import mysql.connector
from api_chief import upload_file_by_url, judge_url_repeat
import requests
from lxml import etree

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'Path=/; aisteUv=17250052696722233225905; aisiteJsSessionId=17255075346391119988021',
    'Pragma': 'no-cache',
    'Referer': 'https://zjt.ln.gov.cn/zjt/gsgg/5dbcf8b5-9.shtml',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


def get_liaoningzfhcxjst_gonggao(queue_id, webpage_id):
    origin = "辽宁省住房和城乡建设厅公示公告"
    url_set = judge_url_repeat(origin)
    response = requests.get('https://zjt.ln.gov.cn/zjt/gsgg/5dbcf8b5-1.shtml', headers=headers)

    res = response.content.decode()
    html = etree.HTML(res)
    page_num = html.xpath("//div[@class='tp-lb-more']/div[@class='easysite-total-page']/b[1]//text()")
    page_num = re.findall(r'\d+', page_num[0])[0]
    for i in range(1, int(page_num) + 1):
        response = requests.get(f'https://zjt.ln.gov.cn/zjt/gsgg/5dbcf8b5-{i}.shtml', headers=headers)
        time.sleep(2)
        res = response.content.decode()
        html = etree.HTML(res)
        all_list = html.xpath("//ul[@class='tp-lb-mode']/li[@class='tp-lb-li']")

        origin_domain = "https://zjt.ln.gov.cn/"
        conn_test = mysql.connector.connect(
            host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
            user="col2024",
            password="Bm_a12a06",
            database='col'
        )
        cursor_test = conn_test.cursor()
        for data in all_list:
            title = "".join(data.xpath("./p[@class='tp-lb-title']/a/text()"))
            title_url = "".join(data.xpath("./p[@class='tp-lb-title']/a/@href"))
            if "http" in title_url:
                continue
            title_url = "https://zjt.ln.gov.cn" + title_url
            data_time = "".join(data.xpath("./p[@class='tp-lb-time']/text()"))
            # 使用re匹配日期
            pub_time = "".join(re.findall(r'\d{4}-\d{2}-\d{2}', data_time))

            # 解析内容
            if title_url not in url_set:
                url_set.add(title_url)
                title_res = requests.get(title_url, headers=headers)
                time.sleep(1.5)
                try:
                    res_html = title_res.content.decode()
                except:
                    print(title_url)
                    continue
                title_html = etree.HTML(res_html)
                content = "".join(title_html.xpath("//div[@class='xqy-xl-room']/p//text()")).strip()
                if not content:
                    content = "".join(title_html.xpath("//div[@class='xqy-xl-room']//p//text()")).strip()
                if not content:
                    content = "".join(title_html.xpath("//div[@class='xqy-xl-room']//text()")).strip()
                content_htmls = title_html.xpath("//div[@class='xqy-xl-cont']")
                content_html = ""
                for content_data in content_htmls:
                    content_html += etree.tostring(content_data, method='html', encoding='unicode')
                path = "".join(title_html.xpath("//div[@class='xqy-xl-dqwz']/span//text()"))
                annex_list = ''
                up_annex_list = ''
                # 附件的处理
                annexs = title_html.xpath("//div[@class='xqy-fjlist']/ul[@class='xqy-fjul']//a/@href")
                if not annexs:
                    annexs = title_html.xpath("//div[@class='xqy-xl-room']//a/@href")
                annexs_num = len(annexs)
                # print(title, title_url, content)
                if annexs_num > 0:
                    for annex in annexs:
                        if "htm" not in annex:
                            if "https" not in annex and "zjt" in annex:
                                annex = 'https://zjt.ln.gov.cn' + annex
                            elif "https" not in annex and "zjt" not in annex:
                                annex = 'https://zjt.ln.gov.cn' + '/zjt' + annex.strip("../..")
                            annex_url_type = annex.split('.')[-1]
                            annex_value = upload_file_by_url(annex, "lnzjtgg", annex_url_type,
                                                             type="other")
                            annex_list += annex + ','
                            if annex_value:
                                up_annex_list += annex_value + ','
                else:
                    annex_list = ''
                annex_list = annex_list.rstrip(',')
                up_annex_list = up_annex_list.rstrip(',')
                source = "".join(title_html.xpath("//div[@class='xqy-xl-xjs']/span[@class='xqy-xl-xjsnr'][3]//text()"))
                source = source.replace("来源：", "")
                if not source:
                    source = "辽宁省住房和城乡建设厅"
                create_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                # 进行数据的去重
                data_unique = f"文章标题：{title}, 文章内容：{content_html}, 来源：{source}, 发布时间：{pub_time}"
                # 数据去重
                hash_value = hashlib.md5(json.dumps(data_unique).encode('utf-8')).hexdigest()
                insert_sql = "INSERT INTO col_chief_public (title,title_url, content,content_html, path,  origin_annex, annex, source,pub_date, origin, origin_domain, create_date,from_queue, webpage_id,md5_key) VALUES (%s,%s, %s, %s,%s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s)"

                cursor_test.execute(insert_sql, (
                    title, title_url, content, content_html, path,
                    annex_list, up_annex_list,
                    source, pub_time,
                    origin, origin_domain, create_date, queue_id, webpage_id, hash_value))

                conn_test.commit()
        cursor_test.close()
        conn_test.close()

# get_liaoningzfhcxjst_gonggao(111,222)