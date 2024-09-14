import os
import re

import mysql.connector
import requests
from lxml import etree

# 连接到测试库
conn_test = mysql.connector.connect(
    host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
    user="col2024",
    password="Bm_a12a06",
    database="col"
)

cursor_test = conn_test.cursor()

# 查询时间为2024-8-20到2024-8-21之间的数据
cursor_test.execute(
    "select id, page_url, content_url from col_paper_notice where paper = '深圳资产管理有限公司'")
rows = cursor_test.fetchall()
for id, page_url, content_url in rows:

    # html = etree.HTML(content_html)
    # #
    # title_content = "".join(html.xpath("//div[@class='wznr wow fadeInUp']//text()")).strip()
    # insert_sql = "UPDATE col_paper_notice SET content = %s WHERE id = %s"
    # cursor_test.execute(insert_sql, (title_content, id))
    # conn_test.commit()
    # insert_sql = "UPDATE col_paper_notice SET page_url = %s WHERE id = %s"
    # cursor_test.execute(insert_sql, (content_url, id))
    # conn_test.commit()
    print(id, page_url, content_url)
    delete_sql = "DELETE FROM col_paper_notice WHERE id = %s"
    cursor_test.execute(delete_sql, (id,))
    conn_test.commit()




    # title_html = html.xpath("//div[@class='info-lf']/p[@class='info-tit']")
    # info_time = html.xpath("//div[@class='info-cent']/p[@class='info-time tit-16']")
    # content_1 = html.xpath("//div[@class='info-cont tit-16']")
    #
    # content_html = ''
    # for con in title_html:
    #     content_html += etree.tostring(con, encoding='utf-8').decode()
    # for con in info_time:
    #     content_html += etree.tostring(con, encoding='utf-8').decode()
    # for con in content_1:
    #     content_html += etree.tostring(con, encoding='utf-8').decode()
    # insert_sql = "UPDATE col_paper_notice SET content_html = %s WHERE id = %s"
    # cursor_test.execute(insert_sql, (content_html, id))
    # conn_test.commit()

    # content = "山东无棣农村商业银行股份有限公司拟于2024年9月13日通过公开拍卖的方式对合法拥有的以下不良债权进行处置，详情如下：1、借款人吴中尧债权，本金余额0元，欠息合计33617.15元。2、借款人吴中尧债权，本金余额1元，欠息合计120528.03元。现催请上述主从债务人及相关责任人立即履行还款义务，并欢迎符合规定的境内外投资者购买上述债权。以上交易的对象为法人、自然人、其他组织，但农商行内部人员，曾经办上述资产的政法干警、原债务企业的管理人员和参与资产处置工作的律师、会计师等中介机构人员不得购买和变相购买该资产。地址：山东省无棣县海丰十路棣丰支行二楼。电话：0543-6680138监督电话：0543-6360358　特别提示：以上信息仅供参考，相关债权的有关情况请到债权单位进行了解。特此公告。山东无棣农村商业银行股份有限公司2024年9月3日"
    # # img_url_new = upload_file_by_url(original_img, f"{id}", "img", "paper")
    # insert_sql = "UPDATE col_paper_notice SET paper = %s WHERE id = %s"
    # cursor_test.execute(insert_sql, ('浙江省浙商资产管理有限公司', id))
    # conn_test.commit()

cursor_test.close()
conn_test.close()
